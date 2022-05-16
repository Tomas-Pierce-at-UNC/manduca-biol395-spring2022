
#ifndef VIDEO_MEDIAN_HEADER
#define VIDEO_MEDIAN_HEADER

#include <stdint.h>

uint8_t* video_median(int32_t file_descriptor, int32_t *size);

void release_median_image(uint8_t *image);

#endif

