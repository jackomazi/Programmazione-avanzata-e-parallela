// Andrea Giacomazzi SM3201257

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>

#include "pgm.h"
#include "mandelbrot.h"
#include "complex.h"

// Funzione main per la creazione di un file pgm contenente il frattale di mandelbrot.
// Viene richiesto da linea di comando il nome del file, il numero massimo di iterazioni M e il numero di righe.
// Poi crea l'immagine e chiama la funzione compute_mandelbrot per colorarla.
// Alla fine chiude l'immagine.

int main(int argc, char * argv[]){

    pgm image;

    char file_name[100];
    printf("Inserisci il nome del file: "); // Inserire il nome del file
    scanf("%s", file_name);
    
    int M;
    printf("Inserisci il numero massimo di iterazioni: "); // Inserire il numero massimo di iterazioni
    scanf("%d", &M);

    int height;
    printf("Inserisci il numero di righe: "); // Inserire il numero di righe (height)
    scanf("%d", &height);
    int width = height * 1.5;

	printf("Nome file: %s \nNumero max iterazioni: %d \nNumero righe: %d\nNumero colonne: %d\n", file_name ,M, height, width);

    int err = create_image(file_name, &image, width, height);
    if (err != 0){
        printf("Errore creazione immagine\n");
        printf("Errore: %d\n", err);
        return err;
    }

    compute_mandelbrot(&image, M, -2, 1, -1, 1);
    close_image(&image);


    return 0;
}



