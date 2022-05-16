
#include "video_median.h"

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
	int fd = open("/home/tomas/Projects/BIOL395/CineFilesOriginal/moth26_2022-02-15_freeflight.cine", O_RDONLY);
	int32_t size = 0;
	uint8_t *med_image = video_median(fd, &size);
	FILE* med = fopen("bytes", "w");
	fwrite(med_image, 1, size, med);
	fclose(med);
	free(med_image);
	return 0;
}
