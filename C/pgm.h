// Andrea Giacomazzi SM3201257

#ifndef PGM_H
#define PGM_H

#include <stdio.h>

struct _pgm_image{
    int width;
    int height;
    int offset;
    int size;
    FILE * fd;
    char * data;
};

typedef struct _pgm_image pgm;
typedef struct _pgm_image * pgm_ptr;

int open_image(char * path, pgm_ptr image);

int create_image(char * path, pgm_ptr image, int width, int height);

char * pixel_at(pgm_ptr image, int x, int y);

int close_image(pgm_ptr image);


#endif