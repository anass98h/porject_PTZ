import pygame
import sys
import random
def init_pygame():
    pygame.init()
    global panorama, viewport_size, screen
    viewport_size = (1920, 1080)
    screen = pygame.display.set_mode(viewport_size, pygame.DOUBLEBUF)
    pygame.display.set_caption('360 Panorama Viewer')
    image_path = 'vignaioli_night.jpg'
    panorama = pygame.image.load(image_path).convert()

class Viewport:
    def __init__(self, panorama, view_size, x_offset=0, y_offset=0, zoom_level=1.0, is_static=False):
        self.panorama = panorama
        self.view_size = view_size
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.zoom_level = zoom_level
        self.is_static = is_static

    def zoom_in(self, mouse_pos):
        self.adjust_view_zoom(mouse_pos, 'in')

    def zoom_out(self, mouse_pos):
        self.adjust_view_zoom(mouse_pos, 'out')

    def adjust_view_zoom(self, mouse_pos, direction):
        old_zoom_level = self.zoom_level
        if direction == 'out':
            self.zoom_level = max(0.1, self.zoom_level - 0.1)
        elif direction == 'in':
            self.zoom_level = min(2.0, self.zoom_level + 0.1)

        zoomed_width = int(self.view_size[0] / self.zoom_level)
        zoomed_height = int(self.view_size[1] / self.zoom_level)
        mouse_x, mouse_y = mouse_pos

        # Adjust the offsets based on the mouse position
        self.x_offset = (self.x_offset + (mouse_x - self.view_size[0] / 2) / old_zoom_level) * old_zoom_level / self.zoom_level
        self.y_offset = (self.y_offset + (mouse_y - self.view_size[1] / 2) / old_zoom_level) * old_zoom_level / self.zoom_level

        self.x_offset %= self.panorama.get_width()  # Wrap-around horizontally
        self.y_offset = max(0, min(self.panorama.get_height() - zoomed_height, self.y_offset))  # Clamp vertically

    def update_position(self, keys, key_map):
        step_size = 10  # pixels per frame
        if keys[key_map['left']]: self.x_offset -= step_size / self.zoom_level
        if keys[key_map['right']]: self.x_offset += step_size / self.zoom_level
        if keys[key_map['up']]: self.y_offset -= step_size / self.zoom_level
        if keys[key_map['down']]: self.y_offset += step_size / self.zoom_level

        self.x_offset %= self.panorama.get_width()  # Wrap-around horizontally
        self.y_offset = max(0, min(self.panorama.get_height() - int(self.view_size[1] / self.zoom_level), self.y_offset))  # Clamp vertically
    

    def render(self, target_surface, position=(0, 0)):
        if self.is_static:
            # Render the panorama stretched across the entire viewport size
            stretched_image = pygame.transform.scale(self.panorama, self.view_size)
            target_surface.blit(stretched_image, position)
            
        else:
            visible_width = int(self.view_size[0] / self.zoom_level)
            visible_height = int(self.view_size[1] / self.zoom_level)
            if self.x_offset + visible_width > self.panorama.get_width():
                # Handle wrapping the view
                part_width = self.panorama.get_width() - self.x_offset
                part_remainder = visible_width - part_width

                part_surface1 = self.panorama.subsurface((int(self.x_offset), int(self.y_offset), part_width, visible_height))
                part_surface1_scaled = pygame.transform.scale(part_surface1, (int(part_width * self.view_size[0] / visible_width), self.view_size[1]))
                target_surface.blit(part_surface1_scaled, position)

                part_surface2 = self.panorama.subsurface((0, int(self.y_offset), part_remainder, visible_height))
                part_surface2_scaled = pygame.transform.scale(part_surface2, (int(part_remainder * self.view_size[0] / visible_width), self.view_size[1]))
                target_surface.blit(part_surface2_scaled, (position[0] + int(part_width * self.view_size[0] / visible_width), position[1]))
            else:
                visible_part = self.panorama.subsurface((int(self.x_offset), int(self.y_offset), visible_width, visible_height))
                visible_part_scaled = pygame.transform.scale(visible_part, self.view_size)
                target_surface.blit(visible_part_scaled, position)
                
                
                
class ZoomSlider:
    def __init__(self, min_zoom, max_zoom, init_zoom, position, size):
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.zoom = init_zoom
        self.position = position
        self.size = size  # size is a tuple (width, height)

    def draw(self, surface):
        # Draw the slider background
        pygame.draw.rect(surface, (200, 200, 200), pygame.Rect(self.position, self.size))
        # Calculate the slider handle position
        handle_height = 20
        handle_y = self.position[1] + (self.size[1] - handle_height) * (self.zoom - self.min_zoom) / (self.max_zoom - self.min_zoom)
        # Draw the slider handle
        pygame.draw.rect(surface, (100, 100, 250), (self.position[0], handle_y, self.size[0], handle_height))

    def set_zoom(self, new_zoom):
        if self.min_zoom <= new_zoom <= self.max_zoom:
            for camera in [camera_1, camera_2]:
                # Calculate the center of the current view
                center_x = camera.x_offset + (camera.view_size[0] * camera.zoom_level) / 2
                center_y = camera.y_offset + (camera.view_size[1] * camera.zoom_level) / 2
                
                # Update the zoom level
                camera.zoom_level = new_zoom

                # Adjust the offsets based on the new zoom level to keep the same center
                camera.x_offset = max(0, min(camera.panorama.get_width() - camera.view_size[0] * new_zoom, center_x - (camera.view_size[0] * new_zoom) / 2))
                camera.y_offset = max(0, min(camera.panorama.get_height() - camera.view_size[1] * new_zoom, center_y - (camera.view_size[1] * new_zoom) / 2))

            # Ensure camera 2 remains aligned to the right of camera 1 for panoramic alignment
            camera_2.x_offset = (camera_1.x_offset + get_camera_field_of_view(camera_1)) % camera_2.panorama.get_width()
            camera_2.y_offset = camera_1.y_offset

            self.zoom = new_zoom


def get_camera_field_of_view(camera):
    # Calculate the visible width of the panorama based on the camera's zoom level
    return int(camera.view_size[0] / camera.zoom_level)

def handle_mouse_click(mouse_x, mouse_y):
    # Calculate panorama coordinates considering the zoom level
    click_x = int(mouse_x * main_view.panorama.get_width() / main_view.view_size[0])
    click_y = int(mouse_y * main_view.panorama.get_height() / main_view.view_size[1])

    # Center camera_1 on the clicked point, considering the zoom level
    camera_1.x_offset = click_x - camera_1.view_size[0] * camera_1.zoom_level / 2
    camera_1.y_offset = click_y - camera_1.view_size[1] * camera_1.zoom_level / 2

    # Clamp the offsets to avoid going out of bounds and wrap horizontally if necessary
    camera_1.x_offset = max(0, min(camera_1.panorama.get_width() - camera_1.view_size[0] * camera_1.zoom_level, camera_1.x_offset)) % camera_1.panorama.get_width()
    camera_1.y_offset = max(0, min(camera_1.panorama.get_height() - camera_1.view_size[1] * camera_1.zoom_level, camera_1.y_offset))

    # Sync camera_2's offsets to follow camera_1
    camera_2.x_offset = (camera_1.x_offset + camera_1.view_size[0] * camera_1.zoom_level) % camera_2.panorama.get_width()
    camera_2.y_offset = camera_1.y_offset
    new_zoom = min(zoom_slider.max_zoom, zoom_slider.zoom)
    zoom_slider.set_zoom(new_zoom)

    # Ensure the wrapping around for camera_2 is handled correctly
    if camera_2.x_offset + camera_2.view_size[0] * camera_2.zoom_level > camera_2.panorama.get_width():
        camera_2.x_offset -= camera_2.panorama.get_width()

def handle_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                new_zoom = min(zoom_slider.max_zoom, zoom_slider.zoom + 0.1)
                zoom_slider.set_zoom(new_zoom)
            elif event.key == pygame.K_DOWN:
                new_zoom = max(zoom_slider.min_zoom, zoom_slider.zoom - 0.1)
                zoom_slider.set_zoom(new_zoom)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if event.button == 1:  # Left click to center cameras and adjust for panoramic view
                handle_mouse_click(mouse_x, mouse_y)


def update_views():
    keys = pygame.key.get_pressed()
    camera_1.update_position(keys, {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s})
    camera_2.update_position(keys, {'left': pygame.K_j, 'right': pygame.K_l, 'up': pygame.K_i, 'down': pygame.K_k})


def render():
    screen.fill((0, 0, 0))  # Clear the screen by filling it with black
    
    # Calculate the x and y position for the main view
    main_view.render(screen)  # Render the main view at the computed position
    
    # Calculate the x and y positions for the camera views
    camera_1_x = (viewport_size[0] // 2 - camera_1.view_size[0])
    camera_1_y = (viewport_size[1] - camera_1.view_size[1]) // 1.3 
    camera_1.render(screen, (camera_1_x, camera_1_y))  # Adjust the y position as needed
    
    camera_2_x = (viewport_size[0] // 2 )
    camera_2_y = (viewport_size[1] - camera_2.view_size[1]) // 1.3
    camera_2.render(screen, (camera_2_x, camera_2_y))  # Adjust the y position as needed
    zoom_slider.draw(screen)  # Draw the slider on the screen

    pygame.display.flip()  # Update the screen with what we've drawn

# Main program setup
init_pygame()
main_view = Viewport(panorama, viewport_size, is_static=True)
camera_1 = Viewport(panorama, (320, 180))
camera_2 = Viewport(panorama, (320, 180))
zoom_slider = ZoomSlider(0.1, 2.0, 1.0, (viewport_size[0] - 50, 50), (20, 200))
running = True
clock = pygame.time.Clock()

while running:
    handle_events()
    update_views()
    render()
    clock.tick(60)  # Maintain 60 FPS

pygame.quit()
sys.exit()
