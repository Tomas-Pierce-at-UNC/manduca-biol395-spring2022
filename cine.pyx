# Module to support opening .cine video files
import array
import ctypes
import numpy

_vmedian = ctypes.cdll.LoadLibrary("./vmedian.so")
BytePtr = ctypes.POINTER(ctypes.c_ubyte)
_vmedian.vmedian.restype = BytePtr


class Cine:
    # represents a .cine file

    ENDIAN = "little"

    def __init__(self, filename):

        self.filename = filename
        self.handle = open(filename, "rb")
        self.image_count = self.__image_count()
        self.image_width = self.__get_image_width()
        self.image_height = self.__get_image_height()
        self.image_size = self.__get_image_size()
        self.__image_offsets = self.__get_image_offsets()
        self.__to = self.__to_images_offset()

    def __image_count(self):

        self.handle.seek(0x14)
        mybytes = self.handle.read(4)
        return int.from_bytes(mybytes, self.ENDIAN, signed=False)

    def __to_images_offset(self):
        self.handle.seek(0x20)
        mybytes = self.handle.read(4)
        return int.from_bytes(mybytes, self.ENDIAN, signed=False)

    def __get_image_offsets(self):
        to = self.__to_images_offset()
        self.handle.seek(to)
        offsets = array.array('Q')
        offsets.fromfile(self.handle, self.image_count)
        return offsets

    def __get_image_width(self):
        self.handle.seek(0x30)
        mybytes = self.handle.read(4)
        return int.from_bytes(mybytes, self.ENDIAN, signed=True)

    def __get_image_height(self):
        self.handle.seek(0x34)
        mybytes = self.handle.read(4)
        return int.from_bytes(mybytes, self.ENDIAN, signed=False)

    def __get_image_size(self):
        self.handle.seek(0x40)
        mybytes = self.handle.read(4)
        return int.from_bytes(mybytes, self.ENDIAN, signed=False)

    def __get_ith_bytes(self, i):
        offset = self.__image_offsets[i]
        self.handle.seek(offset)
        annote_sz_bytes = self.handle.read(4)
        annot_size = int.from_bytes(annote_sz_bytes, self.ENDIAN, signed=False)
        offset += annot_size
        self.handle.seek(offset)
        mybytes = array.array('B')
        mybytes.fromfile(self.handle, self.image_size)
        return mybytes

    def __get_ith_image(self, i):
        mybytes = self.__get_ith_bytes(i)
        data = numpy.array(mybytes, dtype=numpy.uint8)
        shape = (self.image_height,self.image_width)
        shaped = numpy.reshape(data, shape)
        flip = numpy.flip(shaped,0)
        return flip

    def frames_between(self, start, end, step=1):
        for i in range(start, end, step):
            yield (i,self.__get_ith_image(i))

    def close(self):
        self.handle.close()

    def get_fileno(self):
        return self.handle.fileno()

    def get_ith_image(self,i):
                if i < 0 or i >= self.image_count:
                        raise ValueError("image index out of range")
                return self.__get_ith_image(i)

    def get_video_median(self):
        fd = self.get_fileno()
        imsize = self.image_size
        imcount = self.image_count
        to = self.__to
        mybytes = _vmedian.vmedian(fd,imsize,imcount,to)
        data = mybytes[:imsize]
        data = numpy.array(data, dtype=numpy.uint8)
        frame = numpy.reshape(data, (self.image_height,self.image_width))
        frame = numpy.flip(frame,0)
        return frame
