
use std::mem;
use std::fs::File;
use std::io::{
    Read,
    Seek,
    self,
};
use std::convert::TryInto;

#[derive(Copy, Clone)]
#[repr(C)]
pub struct Time64 {
    fractions :u32,
    seconds :u32,
}

#[derive(Copy, Clone)]
#[repr(C)]
pub struct CineFileHeader {
    kind :u16,
    header_size :u16,
    compression :u16,
    version :u16,
    first_movie_image :i32,
    total_image_count :u32,
    first_image_number :i32,
    image_count :u32,
    off_image_header :u32,
    off_setup :u32,
    off_image_offsets :u32,
    trigger_time :Time64,
}

#[derive(Copy, Clone)]
#[repr(C)]
pub struct BitmapInfoHeader {
    header_size :u32,
    width :i32,
    height :i32,
    planes :u16,
    bits_per_pixel :u16,
    compression :u32,
    image_size :u32,
    pels_per_meter_x :i32,
    pels_per_meter_y :i32,
    color_used :u32,
    color_important :u32,
}

pub trait CineRecord: Sized + Copy + Clone {

    const OFFSET :u64;

    fn transcribe_record(cine :&mut File) -> Option<Self> {
        let size = mem::size_of::<Self>();
        let mut space = vec![0u8;size];
        let place = io::SeekFrom::Start(Self::OFFSET);
        cine.seek(place).ok()?;
        cine.read_exact(&mut space[..]).ok()?;
        space.shrink_to_fit();
        let bytes_ptr :*const u8 = space.as_ptr();
        let me_ptr :*const Self = bytes_ptr as *const Self;
        let output = unsafe { *me_ptr };
        Some(output)
    }

}

impl CineRecord for CineFileHeader {
    const OFFSET :u64 = 0x0;
}

impl CineRecord for BitmapInfoHeader {
    const OFFSET :u64 = 0x2C;
}

impl BitmapInfoHeader {
    pub fn sizeof_image(&self) -> u32 {
        self.image_size
    }
}

impl CineFileHeader {

    pub fn get_image_offsets(&self, cine :&mut File) -> Vec<i64> {
        let place = self.off_image_offsets;
        let seeker = io::SeekFrom::Start(place.into());
        cine.seek(seeker).unwrap();
        let mut space = vec![0u8;8 * self.image_count as usize];
        cine.read_exact(&mut space[..]).unwrap();
        let mut data :Vec<i64> = Vec::with_capacity(self.image_count as usize);
        for chunk in space.chunks(8) {
            let bytes :[u8;8] = chunk.try_into().unwrap();
            let val :i64 = i64::from_le_bytes(bytes);
            data.push(val);
        }
        data
    }
    
}