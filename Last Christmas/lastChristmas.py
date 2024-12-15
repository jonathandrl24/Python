import pygame
import numpy as np
import time

pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

def generate_tone(frequency, duration, volume=0.3, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    audio = (wave * volume * 32767).astype(np.int16)
    # convertir a estereo
    stereo_audio = np.column_stack((audio, audio))
    sound = pygame.sndarray.make_sound(stereo_audio)
    return sound

NOTAS = {
    "C5": 523.25,
    "D5": 587.33,
    "E5": 659.25,
    "F5": 698.46,
    "G5": 783.99,
    "A5": 880.00,
    "A5#": 932.33,
    "pause": 0 
}

full = 1.5
half = 0.75
quarter = 0.375
eight = 0.187

lastChristmas = [
    ("G5", quarter + eight),
    ("G5", quarter),
    ("F5", quarter),
    ("C5", eight),
    ("G5", eight),
    ("G5", eight),
    ("A5", eight),
    ("F5", quarter + eight),
    ("D5", eight),
    ("F5", eight),
    ("G5", eight),
    ("G5", eight),
    ("A5", quarter),
    ("F5", quarter + eight),
    ("D5", eight),
    ("E5", eight),
    ("F5", eight),
    ("E5", eight),
    ("D5", quarter + eight),
    ("pause", quarter),
    ("A5", quarter + eight),
    ("G5", quarter + quarter),
    ("D5", eight),
    ("A5", eight),
    ("A5#", eight),
    ("A5", eight),
    ("G5", quarter + eight),
    ("pause", eight),
    ("F5", eight),
    ("E5", eight),
    ("F5", eight),
    ("F5", eight),
    ("E5", quarter),
    ("F5", quarter),
    ("E5", quarter),
    ("C5", quarter + eight),
    ("pause", half-0.05),
]

while True:
    for notas, duracion in lastChristmas:
        if NOTAS[notas] == 0:
            time.sleep(duracion)
        else:
            tone = generate_tone(NOTAS[notas], duracion)
            tone.play()
            time.sleep(duracion)
