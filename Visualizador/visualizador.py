import pygame
import numpy as np
import wave
import colorsys
import random

AUDIO_FILE = "music.wav"

pygame.mixer.init()
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 765
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Audio Visualizer")
clock = pygame.time.Clock()

# Audio settings
pygame.mixer.music.load(AUDIO_FILE)
pygame.mixer.music.play()
wave_file = wave.open(AUDIO_FILE, 'rb')
CHUNK = 512

# Ray settings
class SpiralRay:
    def __init__(self, base_angle):
        self.base_angle = base_angle
        self.rotation_speed = random.uniform(1, 3)
        self.length = random.randint(200, 400)
        self.lifetime = random.randint(30, 60)
        self.width = random.uniform(3, 8)
        self.hue = random.random()
        self.hue_speed = random.uniform(0.01, 0.03)
        self.alpha = 255
        self.segments = 8  # Number of segments in the ray
        self.wave_amplitude = random.uniform(10, 30)
        self.wave_frequency = random.uniform(0.1, 0.3)

    def update(self):
        self.lifetime -= 1
        self.alpha = (self.lifetime * 255) // 60
        self.hue = (self.hue + self.hue_speed) % 1.0
        return self.lifetime > 0

    def draw(self, screen, center_x, center_y, intensity, time):
        if self.lifetime <= 0:
            return
        
        # Calculate points along the spiral ray
        points = []
        current_angle = self.base_angle + time * self.rotation_speed
        
        for i in range(self.segments + 1):
            segment_length = (i / self.segments) * self.length * intensity
            # Add wave effect
            wave_offset = np.sin(time * 2 + i * self.wave_frequency) * self.wave_amplitude
            angle_rad = np.radians(current_angle + wave_offset)
            
            x = center_x + np.cos(angle_rad) * segment_length
            y = center_y + np.sin(angle_rad) * segment_length
            points.append((int(x), int(y)))

        # Create surface for the ray
        ray_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Draw the main ray with gradient color
        color = colorsys.hsv_to_rgb(self.hue, 0.9, 1)
        color = tuple(int(c * 255) for c in color)
        
        # Draw segments with glow effect
        for i in range(len(points) - 1):
            start = points[i]
            end = points[i + 1]
            
            # Gradient alpha for fading towards the end
            segment_alpha = int(self.alpha * (1 - i/self.segments))
            
            # Draw multiple layers for glow effect
            for glow in range(3):
                glow_width = self.width * (3 - glow)
                glow_alpha = segment_alpha // (glow + 2)
                pygame.draw.line(ray_surface, (*color, glow_alpha),
                               start, end, int(glow_width))
        
        screen.blit(ray_surface, (0, 0))

spiral_rays = []

def get_fft_data():
    """Fetch audio data and compute FFT."""
    data = wave_file.readframes(CHUNK)
    if len(data) < CHUNK * wave_file.getsampwidth():
        wave_file.rewind()
        data = wave_file.readframes(CHUNK)
    audio_data = np.frombuffer(data, dtype=np.int16)
    fft_data = np.abs(np.fft.rfft(audio_data)) / CHUNK
    return fft_data / np.max(fft_data) if np.max(fft_data) > 0 else np.zeros_like(fft_data)

def draw_background(hue_offset):
    """Draw an even darker dynamic background that changes color gradually."""
    background_hue = (hue_offset + 0.2) % 1.0
    bg_color = colorsys.hsv_to_rgb(background_hue, 0.1, 0.02)
    bg_color = tuple(int(c * 255) for c in bg_color)
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill(bg_color)
    screen.blit(surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

def draw_spiral_rays(fft_data, time):
    """Draw and update spiral rays."""
    # Calculate overall audio intensity
    intensity = np.mean(fft_data) * 1.5
    
    # Spawn new rays based on audio intensity
    if random.random() < intensity * 0.2:  # Adjust 0.2 to control ray frequency
        # Create rays at regular angular intervals
        for angle in range(0, 360, 45):  # Adjust step for more/fewer rays
            spiral_rays.append(SpiralRay(angle))
    
    # Update and draw existing rays
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    spiral_rays[:] = [ray for ray in spiral_rays if ray.update()]
    for ray in spiral_rays:
        ray.draw(screen, center_x, center_y, intensity, time)

def draw_spirals(fft_data, num_bright_spirals, num_dark_spirals, hue_offset):
    """Draw bright and dark spirals separately with gaps between them."""
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    max_radius = min(WIDTH, HEIGHT) // 1.7

    row_spacing = max_radius // (num_bright_spirals // 2)
    
    # Bright spirals
    for spiral in range(num_bright_spirals):
        spiral_offset = spiral * row_spacing * 1.5
        radius = (max_radius + spiral_offset)

        for i in range(len(fft_data)):
            amplitude = fft_data[i] * radius
            angle = (i * (360 / len(fft_data))) + (hue_offset * 360) + spiral_offset * 0.5
            radians = np.radians(angle)
            x = int(center_x + amplitude * np.cos(radians))
            y = int(center_y + amplitude * np.sin(radians))

            color = colorsys.hsv_to_rgb(
                (hue_offset + (i / len(fft_data)) + spiral_offset) % 1.0,
                1,
                min(fft_data[i] * 1.5, 1)
            )
            color = tuple(int(c * 255) for c in color)
            
            glow_radius = int(15 + fft_data[i] * 50)
            glow_color = (
                min(color[0] + 50, 255),
                min(color[1] + 50, 255),
                min(color[2] + 50, 255),
                150
            )
            pygame.draw.circle(screen, glow_color, (x, y), glow_radius, 0)

    # Dark spirals
    dark_row_spacing = max_radius // (num_dark_spirals // 2)
    for spiral in range(num_dark_spirals):
        spiral_offset = (spiral * dark_row_spacing * 3) + (row_spacing * num_bright_spirals)
        radius = (max_radius + spiral_offset)

        for i in range(len(fft_data)):
            amplitude = fft_data[i] * radius
            angle = (i * (360 / len(fft_data))) + (hue_offset * 360) + spiral_offset * 0.5
            radians = np.radians(angle)
            x = int(center_x + amplitude * np.cos(radians))
            y = int(center_y + amplitude * np.sin(radians))

            color = colorsys.hsv_to_rgb(
                (hue_offset + (i / len(fft_data)) + spiral_offset) % 1.0,
                0.3,
                0.2 if np.random.rand() > 0.3 else 0
            )
            color = tuple(int(c * 255) for c in color)
            
            pygame.draw.circle(screen, color, (x, y), int(5 + fft_data[i] * 15), 0)

def draw_glow_effect():
    """Create a trailing glow effect."""
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 10))  # Increased alpha for longer trails
    screen.blit(surface, (0, 0))

# Main loop
running = True
hue_offset = 0.0
num_bright_spirals = 15
num_dark_spirals = 15
time = 0

try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fft_data = get_fft_data()
        if fft_data is None:
            break

        # Draw background and visualizations
        draw_background(hue_offset)
        draw_glow_effect()
        draw_spirals(fft_data, num_bright_spirals, num_dark_spirals, hue_offset)
        draw_spiral_rays(fft_data, time)

        hue_offset = (hue_offset + 0.005) % 1.0
        time += 0.05
        pygame.display.flip()
        clock.tick(150)
finally:
    wave_file.close()
    pygame.mixer.quit()
    pygame.quit()