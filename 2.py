import pygame
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# PTZ Camera Class
class PTZCamera:
    def __init__(self, x, y):
        self.x = x  # Camera's X position
        self.y = y  # Camera's Y position
        self.azimuth = 0  # Pan angle
        self.elevation = 0  # Tilt angle
        self.zoom = 1  # Zoom level
        self.fov_width = 100  # Field of View width
        self.fov_height = 50  # Field of View height
        self.last_command_time = time.time()

    def adjust_zoom(self, zoom_change):
        current_time = time.time()
        if current_time - self.last_command_time >= 0.25:  # 250 ms response time
            self.zoom += zoom_change
            self.zoom = max(self.zoom, 0.1)  # Prevent zoom from going negative
            self.fov_width = max(100 / self.zoom, 50)  # Zoom affects FOV width
            self.fov_height = max(50 / self.zoom, 25)  # Zoom affects FOV height
            self.last_command_time = current_time

def find_overlap(rect1, rect2):
    x1, y1, width1, height1 = rect1
    x2, y2, width2, height2 = rect2
    
    overlap_x = max(x1, x2)
    overlap_y = max(y1, y2)
    overlap_width = min(x1 + width1, x2 + width2) - overlap_x
    overlap_height = min(y1 + height1, y2 + height2) - overlap_y
    
    if overlap_width > 0 and overlap_height > 0:
        return (overlap_x, overlap_y, overlap_width, overlap_height)
    else:
        return None

def draw(cameras):
    screen.fill(black)
    # Draw all FOVs
    for camera in cameras:
        fov_x, fov_y = camera.x - camera.fov_width / 2, camera.y - camera.fov_height / 2
        pygame.draw.rect(screen, green, [fov_x, fov_y, camera.fov_width, camera.fov_height], 2)
    
    # Check and draw overlaps in red
    for i, cam1 in enumerate(cameras):
        for cam2 in cameras[i+1:]:
            overlap = find_overlap(
                [cam1.x - cam1.fov_width / 2, cam1.y - cam1.fov_height / 2, cam1.fov_width, cam1.fov_height],
                [cam2.x - cam2.fov_width / 2, cam2.y - cam2.fov_height / 2, cam2.fov_width, cam2.fov_height]
            )
            if overlap:
                pygame.draw.rect(screen, red, overlap, 2)
    
    pygame.display.flip()

def main():
    running = True
    cameras = [PTZCamera(150, 150), PTZCamera(650, 150), PTZCamera(400, 450)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            cameras[0].adjust_zoom(-0.1)  # Zoom out camera 1
        if keys[pygame.K_d]:
            cameras[0].adjust_zoom(0.1)   # Zoom in camera 1
        if keys[pygame.K_s]:
            cameras[1].adjust_zoom(-0.1)  # Zoom out camera 2
        if keys[pygame.K_w]:
            cameras[1].adjust_zoom(0.1)   # Zoom in camera 2
        if keys[pygame.K_q]:
            cameras[2].adjust_zoom(-0.1)  # Zoom out camera 3
        if keys[pygame.K_e]:
            cameras[2].adjust_zoom(0.1)   # Zoom in camera 3

        draw(cameras)

    pygame.quit()

if __name__ == "__main__":
    main()
