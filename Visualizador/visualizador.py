import pygame
import numpy as np
import wave
import colorsys
import random
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class VisualizerConfig:
    """Configuration settings for the visualizer"""
    width: int = 800
    height: int = 765
    chunk_size: int = 512
    fps: int = 150
    num_bright_spirals: int = 15
    num_dark_spirals: int = 15
    background_darkness: float = 0.2
    background_saturation: float = 1

class LightningBolt:
    def __init__(self, angle: float):
        self.angle = angle
        self.length = random.randint(900, 1000)  # Increased length range
        self.lifetime = random.randint(5, 15)   # Shorter lifetime for more dramatic effect
        self.width = random.uniform(0.3, 0.5)       # Increased width range
        self.alpha = 255
        self.branches = self._generate_branches()
        self.flicker_state = random.random()    # Add flickering effect
        self.color = self._generate_color()     # Randomize color slightly

    def _generate_color(self) -> Tuple[int, int, int]:
        """Generate slightly randomized lightning color"""
        base_color = (217, 217, 217)  # Base blue-white color
        variation = random.randint(-100, 100)
        return tuple(max(0, min(255, c + variation)) for c in base_color)

    def _generate_branches(self) -> List[Tuple[float, float, float]]:
        """Generate more dynamic branch patterns"""
        branches = []
        num_branches = random.randint(1, 2)  # More branches
        
        # Create primary branches
        for _ in range(num_branches):
            angle_variance = random.uniform(-360, 360)  # Increased angle variance
            branches.append((
                self.angle + angle_variance,
                self.length * random.uniform(0.7, 0.8),  # Longer branches
                random.uniform(0.1, 0.9)  # More varied start positions
            ))
        
        return branches

    def update(self) -> bool:
        """Update lightning state with flickering"""
        self.lifetime -= 1
        self.flicker_state = random.random()
        self.alpha = int((self.lifetime * 255) // 15 * (0.7 + 0.3 * self.flicker_state))
        return self.lifetime > 0

    def _draw_lightning_segment(self, surface: pygame.Surface, start_pos: Tuple[int, int], 
                              end_pos: Tuple[int, int], is_branch: bool = False):
        """Draw enhanced lightning segment with more detail"""
        points = generate_lightning_points(start_pos, end_pos, 
                                        num_segments=6 if is_branch else 10)
        
        # Core lightning
        core_color = (*self.color, self.alpha)
        
        # Multiple layers for more dramatic effect
        layers = 3 if is_branch else 4
        for layer in range(layers):
            width = (self.width * (0.6 if is_branch else 1.0)) * (5 - layer)
            alpha = int(self.alpha * (0.8 ** layer) * self.flicker_state)
            current_color = (*self.color, alpha)
            
            # Draw main segment
            for i in range(len(points) - 1):
                pygame.draw.line(surface, current_color,
                               points[i], points[i + 1],
                               int(width))
                
                # Add small random offshoots for extra detail
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
        self.spiral_rays: List[LightningBolt] = []
        self.hue_offset = 0.0
        self.time = 0
        
    def _setup_audio(self, audio_file: str):
        """Initialize audio playback and wave file reading"""
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        self.wave_file = wave.open(audio_file, 'rb')

    def get_fft_data(self) -> np.ndarray:
        """Get normalized FFT data from audio"""
        data = self.wave_file.readframes(self.config.chunk_size)
        if len(data) < self.config.chunk_size * self.wave_file.getsampwidth():
            self.wave_file.rewind()
            data = self.wave_file.readframes(self.config.chunk_size)
            
        audio_data = np.frombuffer(data, dtype=np.int16)
        fft_data = np.abs(np.fft.rfft(audio_data)) / self.config.chunk_size
        return fft_data / np.max(fft_data) if np.max(fft_data) > 0 else np.zeros_like(fft_data)

    def draw_frame(self, fft_data: np.ndarray):
        """Draw a single frame of the visualization"""
        self._draw_background()
        self._draw_glow_effect()
        self._draw_spirals(fft_data)
        self._draw_lightning_bolts(fft_data)
        
        self.hue_offset = (self.hue_offset + 0.005) % 1.0
        self.time += 0.05
        pygame.display.flip()

    def _draw_background(self):
        """Draw dynamic background"""
        background_hue = (self.hue_offset + 10) % 10.0
        bg_color = colorsys.hsv_to_rgb(
            background_hue, 
            self.config.background_saturation,
            self.config.background_darkness
        )
        bg_color = tuple(int(c * 255) for c in bg_color)
        self.screen.fill(bg_color)

    def _draw_glow_effect(self):
        """Add trailing glow effect"""
        surface = pygame.Surface((self.config.width, self.config.height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 10))
        self.screen.blit(surface, (0, 0))

    def _draw_spirals(self, fft_data: np.ndarray):
        """Draw spiral visualizations"""
        center = (self.config.width // 2, self.config.height // 2)
        max_radius = min(self.config.width, self.config.height) // 1.7
        
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
        
        glow_radius = int(15 + amplitude * 50)
        glow_color = tuple(min(c + 50, 255) for c in color) + (150,)
        pygame.draw.circle(self.screen, glow_color, pos, glow_radius, 0)

    def _draw_dark_point(self, pos: Tuple[int, int], i: int, total_points: int, 
                        amplitude: float, spiral_offset: float):
        color = colorsys.hsv_to_rgb(
            (self.hue_offset + (i / total_points) + spiral_offset * 155) % 1.0,
            0.3,
            0.2 if random.random() > 0.3 else 0
        )
        color = tuple(int(c) for c in color)
        pygame.draw.circle(self.screen, color, pos, int(5 + amplitude * 15), 0)

    def _draw_lightning_bolts(self, fft_data: np.ndarray):
        """Draw and update lightning effects"""
        intensity = np.mean(fft_data) * 1.5  # Calculate intensity from FFT data

        # Add new lightning bolts based on audio intensity
        if random.random() < intensity * 0.3:
            for _ in range(random.randint(1, 3)):  # Spawn 1 to 3 new bolts
                angle = random.uniform(0, 360)  # Random angle for the lightning
                self.spiral_rays.append(LightningBolt(angle))

        # Update and draw each lightning bolt
        center = (self.config.width // 2, self.config.height // 2)
        self.spiral_rays = [bolt for bolt in self.spiral_rays if bolt.update()]
        for bolt in self.spiral_rays:
            for branch in bolt.branches:
                branch_angle, branch_length, branch_start = branch

                # Calculate start and end positions
                start_pos = center
                branch_radians = np.radians(branch_angle)
                end_pos = (
                    int(start_pos[0] + branch_length * np.cos(branch_radians)),
                    int(start_pos[1] + branch_length * np.sin(branch_radians))
                )

                # Draw the main lightning segment
                bolt._draw_lightning_segment(self.screen, start_pos, end_pos, is_branch=True)

    def run(self):
        """Main visualization loop"""
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
        """Clean up resources"""
        self.wave_file.close()
        pygame.mixer.quit()
        pygame.quit()

def generate_lightning_points(start_pos: Tuple[int, int], end_pos: Tuple[int, int], 
                            num_segments: int = 10) -> List[Tuple[int, int]]:
    """Generate more jagged and realistic lightning points"""
    points = [start_pos]
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    
    # Calculate main direction
    dx = end_x - start_x
    dy = end_y - start_y
    dist = np.sqrt(dx*dx + dy*dy)
    
    for i in range(num_segments):
        progress = (i + 1) / (num_segments + 1)
        
        # More pronounced zigzag effect
        zigzag_amount = (1 - progress) * dist * 0.2
        
        # Main position along the line
        straight_x = start_x + dx * progress
        straight_y = start_y + dy * progress
        
        # Add randomized offset
        angle = random.uniform(0, 2 * np.pi)
        offset = random.uniform(-zigzag_amount, zigzag_amount)
        x = straight_x + np.cos(angle) * offset
        y = straight_y + np.sin(angle) * offset
        
        # Add some randomized intermediate points for more detail
        if random.random() < 0.3:
            mid_x = (points[-1][0] + x) / 2 + random.uniform(-20, 20)
            mid_y = (points[-1][1] + y) / 2 + random.uniform(-20, 20)
            points.append((int(mid_x), int(mid_y)))
            
        points.append((int(x), int(y)))
    
    points.append(end_pos)
    return points

if __name__ == "__main__":
    visualizer = AudioVisualizer("music.wav")
    visualizer.run()