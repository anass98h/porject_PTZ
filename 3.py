import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PTZ Camera Control with Overlap Detection")

# Colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)  # Color for overlaps

# Frame rate control
clock = pygame.time.Clock()

class PTZCamera:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.zoom = 1
        self.fov_width, self.fov_height = 200, 100  # Initial FOV size

    def adjust_zoom(self, change):
        self.zoom = max(0.1, self.zoom + change)  # Avoid too small zoom
        self.fov_width = max(200 / self.zoom, 50)
        self.fov_height = max(100 / self.zoom, 25)

    def move(self, dx, dy):
        self.x += dx + random.uniform(-0.5, 0.5)  # Add some randomness to movement
        self.y += dy + random.uniform(-0.5, 0.5)

    def get_fov(self):
        return [self.x - self.fov_width / 2, self.y - self.fov_height / 2, self.fov_width, self.fov_height]

def calculate_overlap(fov1, fov2):
    x1, y1, w1, h1 = fov1
    x2, y2, w2, h2 = fov2
    overlap_x = max(x1, x2)
    overlap_y = max(y1, y2)
    overlap_w = min(x1+w1, x2+w2) - overlap_x
    overlap_h = min(y1+h1, y2+h2) - overlap_y
    if overlap_w > 0 and overlap_h > 0:
        return (overlap_x, overlap_y, overlap_w, overlap_h)
    return None

def draw(cameras):
    screen.fill(black)
    # Draw FOVs
    for camera in cameras:
        pygame.draw.rect(screen, green, camera.get_fov(), 2)
    
    # Check for and draw overlaps
    for i, cam1 in enumerate(cameras):
        for cam2 in cameras[i+1:]:
            overlap_area = calculate_overlap(cam1.get_fov(), cam2.get_fov())
            if overlap_area:
                pygame.draw.rect(screen, red, overlap_area)

def main():
    # create two cameras side by side
    cameras = [PTZCamera(300, 300), PTZCamera(500, 300)]
    move_speed = 5  # Pixels per frame movement speed

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for camera in cameras:
                    camera.x, camera.y = mouse_pos
        keys = pygame.key.get_pressed()
        zoom_change = 0
        dx, dy = 0, 0

        if keys[pygame.K_a]: dx = -move_speed
        if keys[pygame.K_d]: dx = move_speed
        if keys[pygame.K_w]: dy = -move_speed
        if keys[pygame.K_s]: dy = move_speed
        if keys[pygame.K_q]: zoom_change = -0.05
        if keys[pygame.K_e]: zoom_change = 0.05

        # Apply movement and zoom to all cameras
        for camera in cameras:
            camera.move(dx, dy)
            camera.adjust_zoom(zoom_change)

        draw(cameras)
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
