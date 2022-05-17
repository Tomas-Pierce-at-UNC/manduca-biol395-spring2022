check: checkmedian.o libcine_median.so
	gcc checkmedian.o libcine_median.so -o check

checkmedian.o: checkmedian.c cine_median.h libcine_median.so
	gcc checkmedian.c -c -o checkmedian.o libcine_median.so