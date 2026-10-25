/* Playback and develop defaults for the EOS 50D (firmware 1.0.9). */
#ifndef SOUP_CAM_H
#define SOUP_CAM_H

/* The 50D only plays back its own Small JPEG size. */
#define FILM_PLAY_W         2352
#define FILM_PLAY_H         1568
#define FILM_MIN_CR2        (6u * 1024 * 1024)
#define FILM_MODEL_FALLBACK "Canon EOS 50D"
#define FILM_PROGRESS_Y     (480 - 48)

#endif
