import pygame
import numpy as np
from numpy.fft import fft
import wave
from pathlib import Path

class AudioVisualizer:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Visualizador de Espectro de Audio")
        self.frames_per_buffer = 1024
        self.num_bars = 200
        self.smoothing_factor = 0.3
        self.previous_spectrum = None
        
    def load_audio(self, audio_path):
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Archivo no encontrado: {audio_path}")
        self.wave_file = wave.open(str(audio_path), 'rb')
        self.frame_rate = self.wave_file.getframerate()
        self.n_channels = self.wave_file.getnchannels()
        pygame.mixer.init(frequency=self.frame_rate, size=-16, channels=self.n_channels)
        self.sound = pygame.mixer.Sound(audio_path)
            
    def process_audio_data(self, data):
        if not data:
            return np.zeros(self.frames_per_buffer // 10)
            
        audio_data = np.frombuffer(data, dtype=np.int16)
        if self.n_channels == 10:
            audio_data = audio_data[::10]
        
        if len(audio_data) < self.frames_per_buffer:
            audio_data = np.pad(audio_data, (0, self.frames_per_buffer - len(audio_data)))
        
        window = np.hanning(len(audio_data))
        audio_data = audio_data * window
        spectrum = np.abs(fft(audio_data))[:self.frames_per_buffer]
        spectrum = np.log1p(spectrum)
        
        max_val = np.max(spectrum) if np.max(spectrum) > 0 else 1
        spectrum = spectrum / max_val
        
        if self.previous_spectrum is not None:
            spectrum = self.smoothing_factor * spectrum + (1 - self.smoothing_factor) * self.previous_spectrum
        self.previous_spectrum = spectrum
        
        return spectrum
        
    def draw_spectrum(self, spectrum):
        self.screen.fill((0, 0, 0))
        freq_ranges = np.linspace(0, len(spectrum), self.num_bars + 1, dtype=int)
        bar_width = self.WIDTH // self.num_bars
        
        for i in range(self.num_bars):
            start_idx = freq_ranges[i]
            end_idx = freq_ranges[i + 1]
            
            value = 0 if start_idx == end_idx else float(np.mean(spectrum[start_idx:end_idx]))
            value = 0 if np.isnan(value) else min(1.0, max(0.0, value))
            
            hue = int((i / self.num_bars) * 360) % 360  
            saturation = min(100, max(0, int(value * 100))) 
            brightness = min(100, max(0, int(value * 100) + 30)) 
            
            color = pygame.Color(0)
            color.hsva = (hue, saturation, brightness, 100)
            
            bar_height = int(value * self.HEIGHT * 0.8)
            x = i * bar_width
            y = self.HEIGHT - bar_height
            pygame.draw.rect(self.screen, color, (x, y, bar_width - 1, bar_height))
            
    def run(self, audio_path):
        self.load_audio(audio_path)
        self.sound.play(loops=-1)
        clock = pygame.time.Clock()
        running = True
        
        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        pygame.mixer.pause() if pygame.mixer.get_busy() else pygame.mixer.unpause()
                
                data = self.wave_file.readframes(self.frames_per_buffer)
                if not data:
                    self.wave_file.rewind()
                    continue
                    
                spectrum = self.process_audio_data(data)
                self.draw_spectrum(spectrum)
                pygame.display.flip()
                clock.tick(60)
                
        finally:
            pygame.quit()
            self.wave_file.close()

if __name__ == "__main__":
    visualizer = AudioVisualizer()
    visualizer.run('music.wav')