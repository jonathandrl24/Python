import pygame
import numpy as np
import wave
import colorsys
import random
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class VisualizerConfig:
    width: int = 800
    height: int = 765
    chunk_size: int = 512
    fps: int = 150
    num_bright_spirals: int = 15
    num_dark_spirals: int = 15
    background_darkness: float = 0.5
    background_saturation: float = 1
    
    beat_threshold: float = 1.3
    beat_decay: float = 0.95
    bass_freq_range: Tuple[int, int] = (0, 50)


class LightningBolt:
    def __init__(self, angle: float, intensity: float = 1.0):
        self.angle = angle
        self.length = random.randint(900, 1000)
        self.lifetime = random.randint(5, 15)
        self.width = random.uniform(0.2, 0.4) * intensity  
        self.alpha = 255 * intensity  # Brillo
        self.branches = self._generate_branches(intensity)
        self.flicker_state = random.random()
        self.color = self._generate_color(intensity)

    def _generate_color(self, intensity: float) -> Tuple[int, int, int]:
        base_color = (217, 217, 217)
        variation = random.randint(-20, 20)
        color = tuple(max(0, min(255, int((c + variation) * intensity))) for c in base_color)
        return color


    def _generate_branches(self, intensity: float) -> List[Tuple[float, float, float]]:
        branches = []
        num_branches = random.randint(2, 3 if intensity > 1.5 else 2)
        
        for _ in range(num_branches):
            angle_variance = random.uniform(-60, 60) * intensity
            branches.append((
                self.angle + angle_variance,
                self.length * random.uniform(0.7, 0.9) * intensity,
                random.uniform(0.1, 0.9)
            ))
        return branches


    def update(self) -> bool:
        self.lifetime -= 1
        self.flicker_state = random.random()
        self.alpha = int((self.lifetime * 255) // 15 * (0.7 + 0.3 * self.flicker_state))
        return self.lifetime > 0

    def _draw_lightning_segment(self, surface: pygame.Surface, start_pos: Tuple[int, int], 
                              end_pos: Tuple[int, int], is_branch: bool = False):
        points = generate_lightning_points(start_pos, end_pos, 
                                        num_segments=6 if is_branch else 10)
        
        core_color = (*self.color, self.alpha)
        
        layers = 3 if is_branch else 4
        for layer in range(layers):
            width = (self.width * (0.6 if is_branch else 1.0)) * (5 - layer)
            alpha = int(self.alpha * (0.8 ** layer) * self.flicker_state)
            current_color = (*self.color, alpha)
            
            for i in range(len(points) - 1):
                pygame.draw.line(surface, current_color,
                               points[i], points[i + 1],
                               int(width))
                
                if not is_branch and random.random() < 0.2:
                    offset = random.uniform(-20, 20)
                    offshoot_end = (
                        int(points[i][0] + offset),
                        int(points[i][1] + offset)
                    )
                    pygame.draw.line(surface, current_color,
                                   points[i], offshoot_end,
                                   int(width * 0.5))

class AudioVisualizer:
    def __init__(self, audio_file: str, config: Optional[VisualizerConfig] = None):
        self.config = config or VisualizerConfig()
        pygame.mixer.init()
        pygame.init()
        
        self.screen = pygame.display.set_mode((self.config.width, self.config.height))
        pygame.display.set_caption("Audio Visualizer")
        self.clock = pygame.time.Clock()
        
        self._setup_audio(audio_file)
        self.spiral_rays = []
        self.hue_offset = 0.0
        self.time = 0
        
        self.energy_history = []
        self.current_beat_energy = 0
        self.last_beat_time = 0
        self.beat_threshold = self.config.beat_threshold
        self.beat_decay = self.config.beat_decay
        self.bass_freq_range = self.config.bass_freq_range
        
        
    def detect_beat(self, fft_data: np.ndarray) -> Tuple[bool, float]:
        bass_range = slice(self.config.bass_freq_range[0], 
                         min(self.config.bass_freq_range[1], len(fft_data)))
        bass_energy = np.sum(fft_data[bass_range])
        
        self.energy_history.append(bass_energy)
        if len(self.energy_history) > 50:
            self.energy_history.pop(0)
            
        avg_energy = np.mean(self.energy_history) if self.energy_history else bass_energy
        
        self.current_beat_energy *= self.config.beat_decay
        
        is_beat = False
        intensity = 1.0
        if bass_energy > avg_energy * self.config.beat_threshold:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_beat_time > 100:  
                is_beat = True
                self.last_beat_time = current_time
                intensity = bass_energy / avg_energy
                self.current_beat_energy = intensity
        
        return is_beat, max(intensity, self.current_beat_energy)

        
    def _setup_audio(self, audio_file: str):
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        self.wave_file = wave.open(audio_file, 'rb')

    def get_fft_data(self) -> np.ndarray:
        data = self.wave_file.readframes(self.config.chunk_size)
        if len(data) < self.config.chunk_size * self.wave_file.getsampwidth():
            self.wave_file.rewind()
            data = self.wave_file.readframes(self.config.chunk_size)
            
        audio_data = np.frombuffer(data, dtype=np.int16)
        fft_data = np.abs(np.fft.rfft(audio_data)) / self.config.chunk_size
        return fft_data / np.max(fft_data) if np.max(fft_data) > 0 else np.zeros_like(fft_data)

    def draw_frame(self, fft_data: np.ndarray):
        self._draw_background()
        self._draw_glow_effect()
        self._draw_spirals(fft_data)
        self._draw_lightning_bolts(fft_data)
        
        self.hue_offset = (self.hue_offset + 0.005) % 1.0
        self.time += 0.05
        pygame.display.flip()

    def _draw_background(self):
        background_hue = (self.hue_offset + 10) % 10.0
        bg_color = colorsys.hsv_to_rgb(
            background_hue, 
            self.config.background_saturation,
            self.config.background_darkness
        )
        bg_color = tuple(int(c * 255) for c in bg_color)
        self.screen.fill(bg_color)

    def _draw_glow_effect(self):
        surface = pygame.Surface((self.config.width, self.config.height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 10))
        self.screen.blit(surface, (0, 0))

    def _draw_spirals(self, fft_data: np.ndarray):
        center = (self.config.width // 2, self.config.height // 2)
        max_radius = min(self.config.width, self.config.height) // 2.1
        
        self._draw_spiral_type(fft_data, center, max_radius, 
                             self.config.num_bright_spirals, bright=True)
        self._draw_spiral_type(fft_data, center, max_radius, 
                             self.config.num_dark_spirals, bright=False)

    def _draw_spiral_type(self, fft_data: np.ndarray, center: Tuple[int, int], 
                         max_radius: float, num_spirals: int, bright: bool):
        row_spacing = max_radius // (num_spirals // 2)
        for spiral in range(num_spirals):
            spiral_offset = (spiral * row_spacing * (1.5 if bright else 3))
            if not bright:
                spiral_offset += row_spacing * self.config.num_bright_spirals
            
            radius = max_radius + spiral_offset
            self._draw_single_spiral(fft_data, center, radius, spiral_offset, bright)

    def _draw_single_spiral(self, fft_data: np.ndarray, center: Tuple[int, int], 
                          radius: float, spiral_offset: float, bright: bool):
        for i, amplitude in enumerate(fft_data):
            angle = (i * (360 / len(fft_data))) + (self.hue_offset * 360) + spiral_offset * 0.5
            pos = self._calculate_point_position(center, angle, amplitude * radius)
            
            if bright:
                self._draw_bright_point(pos, i, len(fft_data), amplitude, spiral_offset)
            else:
                self._draw_dark_point(pos, i, len(fft_data), amplitude, spiral_offset)

    def _calculate_point_position(self, center: Tuple[int, int], angle: float, 
                                radius: float) -> Tuple[int, int]:
        radians = np.radians(angle)
        return (
            int(center[0] + radius * np.cos(radians)),
            int(center[1] + radius * np.sin(radians))
        )

    def _draw_bright_point(self, pos: Tuple[int, int], i: int, total_points: int, 
                      amplitude: float, spiral_offset: float):
        color = colorsys.hsv_to_rgb(
            (self.hue_offset + (i / total_points) + spiral_offset) % 1.0,
            1,
            min(amplitude * 1.5, 1)  
        )
        color = tuple(int(c * 255) for c in color)      
        
        core_color = tuple(min(c + 100, 255) for c in color)
        pygame.draw.circle(self.screen, core_color, pos, int(15 + amplitude * 50), 0)

    def _draw_dark_point(self, pos: Tuple[int, int], i: int, total_points: int, 
                        amplitude: float, spiral_offset: float):
        color = colorsys.hsv_to_rgb(
            (self.hue_offset + (i / total_points) + spiral_offset) % 1.0,
            0.3,
            0.2 if random.random() > 0.3 else 0
        )
        color = tuple(int(c * 115) for c in color)
        pygame.draw.circle(self.screen, color, pos, int(5 + amplitude * 15), 0)

    def _draw_lightning_bolts(self, fft_data: np.ndarray):
        is_beat, intensity = self.detect_beat(fft_data)
        
        if is_beat:
            num_bolts = random.randint(1, max(1, int(intensity)))
            for _ in range(num_bolts):
                angle = random.uniform(0, 360)
                self.spiral_rays.append(LightningBolt(angle, intensity))
        
        center = (self.config.width // 2, self.config.height // 2)
        self.spiral_rays = [bolt for bolt in self.spiral_rays if bolt.update()]
        
        for bolt in self.spiral_rays:
            for branch in bolt.branches:
                branch_angle, branch_length, branch_start = branch
                start_pos = center
                branch_radians = np.radians(branch_angle)
                end_pos = (
                    int(start_pos[0] + branch_length * np.cos(branch_radians)),
                    int(start_pos[1] + branch_length * np.sin(branch_radians))
                )
                bolt._draw_lightning_segment(self.screen, start_pos, end_pos, is_branch=True)

    def run(self):
        try:
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                fft_data = self.get_fft_data()
                if fft_data is None:
                    break

                self.draw_frame(fft_data)
                self.clock.tick(self.config.fps)
        finally:
            self.cleanup()

    def cleanup(self):
        self.wave_file.close()
        pygame.mixer.quit()
        pygame.quit()

def generate_lightning_points(start_pos: Tuple[int, int], end_pos: Tuple[int, int], 
                            num_segments: int = 10) -> List[Tuple[int, int]]:
    points = [start_pos]
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    
    dx = end_x - start_x
    dy = end_y - start_y
    dist = np.sqrt(dx*dx + dy*dy)
    
    for i in range(num_segments):
        progress = (i + 1) / (num_segments + 1)
        
        zigzag_amount = (1 - progress) * dist * 0.2
        
        straight_x = start_x + dx * progress
        straight_y = start_y + dy * progress
        
        # Add randomized offset
        angle = random.uniform(0, 2 * np.pi)
        offset = random.uniform(-zigzag_amount, zigzag_amount)
        x = straight_x + np.cos(angle) * offset
        y = straight_y + np.sin(angle) * offset
        
        if random.random() < 0.3:
            mid_x = (points[-1][0] + x) / 2 + random.uniform(-20, 20)
            mid_y = (points[-1][1] + y) / 2 + random.uniform(-20, 20)
            points.append((int(mid_x), int(mid_y)))
            
        points.append((int(x), int(y)))
    
    points.append(end_pos)
    return points

if __name__ == "__main__":
    visualizer = AudioVisualizer("yesterday-vs self.wav")
    visualizer.run()