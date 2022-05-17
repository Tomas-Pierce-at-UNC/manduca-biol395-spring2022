
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#include "cine_median.h"

int main() {
	const char * filename = "/home/tomas/Projects/BIOL395/CineFilesOriginal/moth26_2022-02-21_Cine1.cine";
	int fd = open(filename, O_RDONLY);
	int32_t im_size = image_size(fd);
	if(im_size == -1) {
		return -1;
	}
	uint8_t *med = video_median(fd);

	FILE* out = fopen("thing", "w");
	fwrite(med, sizeof(uint8_t), (size_t)im_size, out);
	fclose(out);
	close(fd);
	return 0;
}