// Andrea Giacomazzi SM3201257

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>

#include "pgm.h"

// Funzione per creare un file pgm, richiede in input il path (il nome del file), un puntatore ad una struttura pgm,
// la larghezza e l'altezza dell'immagine.
// Restituisce 0 se tutto è andato a buon fine, -1 se c'è stato un errore nell'apertura del file e -2 se c'è stato 
// un errore nella mappatura del file.

int create_image(char * path, pgm_ptr image, int width, int height){
    FILE * fd = fopen(path, "w+");
    if (fd == NULL){
        perror("Errore apertura file");
        return -1;
    }

    int written = fprintf(fd, "P5\n%d %d\n255\n", width, height);
    
    ftruncate(fileno(fd), written + width * height); // Setta la dimensione del file
    
    image->fd = fd;
    if (image->fd == NULL){
        perror("Errore apertura file");
        return -1;
    }

    image->width = width;
    image->height = height;
    image->offset = ftell(fd);
    
    struct stat sbuf;
    stat(path, &sbuf);
    image->size = sbuf.st_size;

    image->data = mmap((void *)0, image->size, PROT_READ | PROT_WRITE, MAP_SHARED, fileno(fd), 0);
    if (image->data == MAP_FAILED){
        perror("Errore mappatura file");
        fclose(fd);
        return -2;
    }
    return 0;
}

// Funzione che ritorna un puntatore ad un pixel dell'immagine, richiede in input un puntatore ad una struttura pgm, e le 
// coordinate del pixel. Verrà utilizzata per colorare direttamente il pixel.

char * pixel_at(pgm_ptr image, int x, int y){
    if (image == NULL){
        return NULL;
    }
    return &image->data[y * image->width + x + image->offset];
}

// Funzione per chiudere un file pgm, richiede in input un puntatore ad una struttura pgm e chiiude il file e la mappatura.
int close_image(pgm_ptr image){
    if (image == NULL){
        return -1;
    }
    munmap(image->data, image->size);
    fclose(image->fd);
    return 0;
}

