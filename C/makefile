CC = gcc
CFLAGS = -fopenmp -O3 -Wall -std=c17 -pedantic

all:main

main: main.o pgm.o mandelbrot.o mandelbrot.h pgm.h
	${CC} ${CFLAGS} main.o pgm.o mandelbrot.o -o $@ -lm

pgm.o: pgm.c pgm.h
	${CC} ${CFLAGS} -c $^ -lm

mandelbrot.o: mandelbrot.c mandelbrot.h pgm.h
	${CC} ${CFLAGS} -c $^ -lm

.PHONY: clean main

clean: rm -rf *.o