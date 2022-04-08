
#include <sys/types.h>
#include <unistd.h>

#include <stdlib.h>
#include <stdint.h>
#include <stdint.h>

struct Histogram {
	int bins[256];
	int count;
};

int get_median(const struct Histogram *histogram) {

	int index = 0;
	int middle = histogram->count / 2;
	int bin = 0;

	for(int i = 0; i < 256; i++) {
		bin = i;
		int count = histogram->bins[bin];
		for(int j = 0; j < count; j++) {
			index += 1;
			if(index == middle) {
				goto FINISH;
			}
		}
	}

	FINISH: return bin;

}

off_t img_strt_from_offset(int fd, off_t offset) {
	lseek(fd, offset, SEEK_SET);
	uint32_t annote_size;
	read(fd, (void*)&annote_size, 4);
	offset += (off_t) annote_size;
	return offset;
}

uint8_t* vmedian(int fd, int imSize, int imCnt, off_t offImgOff) {
	lseek(fd, offImgOff,SEEK_SET);
	uint64_t *offsets = malloc(sizeof(uint64_t) * imCnt);
	read(fd, offsets, imCnt);
	struct Histogram *histograms = calloc(imSize, sizeof(struct Histogram));
	uint8_t *frame_arena = malloc(sizeof(uint8_t) * imSize);
	for(int i = 0; i < imCnt; i++) {
		off_t pos = offsets[i];
		off_t imagePos = img_strt_from_offset(fd, pos);
		lseek(fd, imagePos, SEEK_SET);
		read(fd, frame_arena, imSize);
		for(int j = 0; j < imSize; j++) {
			uint8_t pval = frame_arena[j];
			histograms[j].bins[pval] += 1;
			histograms[j].count += 1;
		}
	}
	for(int k = 0; k < imSize; k++) {
		uint8_t median = (uint8_t)get_median(histograms + k);
		frame_arena[k] = median;
	}
	free(offsets);
	free(histograms);
	return frame_arena;
}

/* TODO: take median of subslice image sequence of video */
