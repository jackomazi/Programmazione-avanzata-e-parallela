// Andrea Giacomazzi SM3201257

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <math.h>

#include "mandelbrot.h"
#include "complex.h"
#include "pgm.h"
#include "omp.h"

// Funzione che, per ogni pixel dell'immagine, colora in base alla presenza o meno del pixel nel frattale di mandelbrot.
// Richiede in input un puntatore ad una struttura pgm, il numero massimo di iterazioni, e i valori min e max 
// per la parte reale e immaginaria del piano complesso.
// Alla fine della funzione l'immagine sarà colorata perchè verrà colorato direttamente il colore del pixel attraverso il puntatore
// ad esso.

// La funzione è stata parallelizzata con OpenMP, utilizzando #pragma omp parallel for collapse(2) per parallelizzare i due cicli
// for annidati. 

void compute_mandelbrot(pgm_ptr image, int max_iter, double real_min, double real_max, double imag_min, double imag_max){
    
    double real_step = (real_max - real_min) / (image->width-1);
    double imag_step = (imag_max - imag_min) / (image->height-1);

    #pragma omp parallel for collapse(2)
    for (int i = 0; i < image->width; i++){
        for (int j = 0; j < image->height; j++){
            
            double real = real_min + i * real_step;
            double imag = imag_min + j * imag_step;
            double complex c = real + imag * I; // definisco c = x + yi
    
            double complex z = 0; // definisco z_0 = 0

            int iter = 0; // inizializzo il contatore delle iterazioni
            
            while (cabs(z) < 2 && iter < max_iter){ // finchè |z| < 2 e iter < max_iter continuo a calcolare la successione
                z = z*z + c; // calcolo z_{n+1} = z_n^2 + c
                iter++;
            }

            if (iter == max_iter){ // se iter = max_iter coloro il pixel di bianco
                unsigned char * pixel = pixel_at(image, i , j );
                * pixel = 255;
            } else { // altrimenti coloro il pixel in base al numero di iterazioni
                unsigned char * pixel = pixel_at(image, i, j); ;
                float color = 255 * ((log(iter) / log(max_iter)));
                * pixel = (int)floor(color);
            }

        }
    }
}
