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
    def __init__(self):
        self.azimuth = 0  # Horizontal movement; left/right
        self.elevation = 0  # Vertical movement; up/down
        self.zoom = 1  # Zoom level
        self.fov_width = 100  # Field of View width
        self.fov_height = 50  # Field of View height
        self.last_command_time = time.time()

    def move(self, azimuth_change, elevation_change, zoom_change):
        current_time = time.time()
        if current_time - self.last_command_time >= 0.25:  # 250 ms response time
            self.azimuth += azimuth_change * 5  # Increase sensitivity for demonstration
            self.elevation += elevation_change * 5  # Increase sensitivity for demonstration
            self.zoom += zoom_change
            self.zoom = max(self.zoom, 0.1)  # Prevent zoom from going negative
            self.fov_width = max(100 / self.zoom, 50)  # Zoom affects FOV width
            self.fov_height = max(50 / self.zoom, 25)  # Zoom affects FOV height
            self.last_command_time = current_time

# Drawing function adjusted for pan and tilt
def draw(camera):
    screen.fill(black)
    # Adjust FOV position based on azimuth and elevation
    fov_x = (screen_width / 2 - camera.fov_width / 2) + camera.azimuth
    fov_y = (screen_height / 2 - camera.fov_height / 2) + camera.elevation
    # Draw FOV with pan and tilt adjustments
    pygame.draw.rect(screen, green, [fov_x, fov_y, camera.fov_width, camera.fov_height], 2)
    # Draw center point
    pygame.draw.circle(screen, red, (screen_width // 2, screen_height // 2), 5)
    pygame.display.flip()

# Main function
def main():
    running = True
    camera = PTZCamera()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            camera.move(-1, 0, 0)  # Move left
        if keys[pygame.K_RIGHT]:
            camera.move(1, 0, 0)  # Move right
        if keys[pygame.K_UP]:
            camera.move(0, -1, 0)  # Move up
        if keys[pygame.K_DOWN]:
            camera.move(0, 1, 0)  # Move down
        if keys[pygame.K_a]:
            camera.move(0, 0, -0.1)  # Zoom out
        if keys[pygame.K_d]:
            camera.move(0, 0, 0.1)  # Zoom in

        draw(camera)

    pygame.quit()

if __name__ == "__main__":
    main()
