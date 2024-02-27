// Andrea Giacomazzi SM3201257
#ifndef MANDELBROT_H
#define MANDELBROT_H
#include <complex.h>
#include "pgm.h"

void compute_mandelbrot(pgm_ptr image, int max_iter, double real_min, double real_max, double imag_min, double imag_max);

#endif