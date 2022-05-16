#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        let result = 2 + 2;
        assert_eq!(result, 4);
    }
}

extern crate libc;

use std::os::unix::io::FromRawFd;
use std::fs;
use std::ptr;
use std::io::{
    Seek,
    Read,
    self,
};

mod histogram;
mod headers;

use headers::CineRecord;
use histogram::Histogram;

/** Takes a median across the time dimension in a CINE video file.
The first parameter is a linux-style file descriptor, this is our input.
The second parameter is an i32 pointer that acts as an out parameter for
the size of the resulting median image in bytes.
The function returns a pointer to the resultant median image.
**/
#[no_mangle]
pub unsafe extern "C" fn video_median(file_descriptor :i32, size :*mut i32) -> *const u8 {
    if size.is_null() {
        return ptr::null();
    }
    let mut file :fs::File = fs::File::from_raw_fd(file_descriptor);
    let cfh = match headers::CineFileHeader::transcribe_record(&mut file) {
        Some(head) => head,
        None => {return ptr::null();},
    };
    let bih= match headers::BitmapInfoHeader::transcribe_record(&mut file) {
        Some(head) => head,
        None => {return ptr::null();},
    };
    *size = bih.sizeof_image() as i32;

    let img_size = bih.sizeof_image() as usize;
    let median :Vec<u8> = get_median(&mut file, &cfh, &bih);
    let median_ptr = median.as_ptr();
    let output :*mut u8 = libc::malloc(bih.sizeof_image() as usize) as *mut u8;
    libc::memcpy(output as *mut libc::c_void, median_ptr as *mut libc::c_void, img_size);
    output
}

#[no_mangle]
pub unsafe extern "C" fn release_median_image(image :*const u8) {
    libc::free(image as *mut libc::c_void);
}

fn get_median(file :&mut fs::File, cfh :&headers::CineFileHeader, bih :&headers::BitmapInfoHeader) -> Vec<u8> {
    let image_size = bih.sizeof_image();
    let mut histograms :Vec<Histogram> = Vec::with_capacity(image_size as usize);
    for _i in 0..image_size {
        let hist = Histogram::new();
        histograms.push(hist);
    }
    let image_offsets = cfh.get_image_offsets(file);
    for offset in image_offsets {
        let mut buffer :Vec<u8> = vec![0u8; image_size as usize];
        let place = skip_to_pixels(file, offset);
        load_image(file, place, &mut buffer[..]);
        for (i, val) in buffer.into_iter().enumerate() {
            histograms[i].update(val);
        }
    }
    let mut medians :Vec<u8> = Vec::with_capacity(image_size as usize);
    for histogram in histograms {
        medians.push(histogram.median());
    }

    medians.shrink_to_fit();
    medians

}

fn skip_to_pixels(file :&mut fs::File, offset :i64) -> u64 {
    let place = io::SeekFrom::Start(offset as u64);
    file.seek(place).unwrap();
    let mut arena :[u8;4] = [0,0,0,0];
    file.read_exact(&mut arena).unwrap();
    let annotation_size :u64 = u32::from_le_bytes(arena).into();
    let new_position = (offset as u64) + annotation_size;
    /*
    let new_place = io::SeekFrom::Start(new_position);
    file.seek(new_place).unwrap();
    */
    new_position
}

fn load_image(file :&mut fs::File, pixel_array_offset :u64, arena :&mut [u8]) {
    file.seek(io::SeekFrom::Start(pixel_array_offset)).unwrap();
    file.read_exact(arena).unwrap();
}