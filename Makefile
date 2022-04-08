all: vmedian.so cymods

vmedian.so: vmedian.c
	gcc vmedian.c -o vmedian.so -shared -fPIC -Werror -Wall -Wpedantic

cymods: cine.pyx common.pyx align.pyx tester.pyx tube.pyx
	python3 setup.py build_ext --inplace

clean:
	rm align.c cine.c common.c tester.c tube.c
	rm *.so
