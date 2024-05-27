import pygame
import sys
import random
def init_pygame():
    pygame.init()
    global panorama, viewport_size, screen
    viewport_size = (1920, 1080)
    screen = pygame.display.set_mode(viewport_size, pygame.DOUBLEBUF)
    pygame.display.set_caption('360 Panorama Viewer')
    image_path = 'model and synchronization/vignaioli_night.jpg'
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
        
        # Button labels
        font = pygame.font.Font(None, 30)
        plus_text = font.render('-', True, (255, 255, 255))
        minus_text = font.render('+', True, (255, 255, 255))
        surface.blit(plus_text, (self.position[0] +7 , self.position[1] - 20))
        surface.blit(minus_text, (self.position[0] + 5, self.position[1] + self.size[1]))
        
        # Slider label
        label = font.render('Zoom Level', True, (255, 255, 255))
        surface.blit(label, (self.position[0] -70, self.position[1] -40 ))

    def set_zoom(self, new_zoom):
        if self.min_zoom <= new_zoom <= self.max_zoom:
            for camera in [camera_1, camera_2, camera_3, camera_4, camera_5]:
                # Calculate the center of the current view
                center_x = camera.x_offset + (camera.view_size[0] * camera.zoom_level) / 2
                center_y = camera.y_offset + (camera.view_size[1] * camera.zoom_level) / 2

                # Update the zoom level
                camera.zoom_level = new_zoom

                # Adjust the offsets based on the new zoom level to keep the same center
                camera.x_offset = max(0, min(camera.panorama.get_width() - camera.view_size[0] * new_zoom, center_x - (camera.view_size[0] * new_zoom) / 2))
                camera.y_offset = max(0, min(camera.panorama.get_height() - camera.view_size[1] * new_zoom, center_y - (camera.view_size[1] * new_zoom) / 2))
            # Update camera 2 offsets to maintain panoramic alignment
            adjust_camera_offsets()

            self.zoom = new_zoom


def get_camera_field_of_view(camera):
    # Calculate the visible width of the panorama based on the camera's zoom level
    return int(camera.view_size[0] / camera.zoom_level)

def handle_mouse_click(mouse_x, mouse_y):
    # Calculate the width occupied by all cameras and their starting x-coordinate
    calculate_camera_directions()

    # Calculate panorama coordinates considering the zoom level
    click_x = int(mouse_x * main_view.panorama.get_width() / main_view.view_size[0])
    click_y = int(mouse_y * main_view.panorama.get_height() / main_view.view_size[1])

    # Center camera_1 on the clicked point, considering the zoom level
    camera_1.x_offset = click_x - camera_1.view_size[0] * camera_1.zoom_level / 2
    camera_1.y_offset = click_y - camera_1.view_size[1] * camera_1.zoom_level / 2

    # Clamp the offsets to avoid going out of bounds and wrap horizontally if necessary
    camera_1.x_offset = max(0, min(camera_1.panorama.get_width() - camera_1.view_size[0] * camera_1.zoom_level, camera_1.x_offset)) % camera_1.panorama.get_width()
    camera_1.y_offset = max(0, min(camera_1.panorama.get_height() - camera_1.view_size[1] * camera_1.zoom_level, camera_1.y_offset))

    adjust_camera_offsets()
    # Set the zoom level to the minimum of the current zoom level and the slider's max zoom
    new_zoom = min(zoom_slider.max_zoom, zoom_slider.zoom)
    zoom_slider.set_zoom(new_zoom)

    # Ensure the wrapping around for camera_2 is handled correctly
    if camera_2.x_offset + camera_2.view_size[0] * camera_2.zoom_level > camera_2.panorama.get_width():
        camera_2.x_offset -= camera_2.panorama.get_width()

def calculate_camera_directions():
    # Determine each camera's pointing direction based on its x_offset and y_offset
    for i in range(1, number_of_cameras_active + 1):
        camera = globals()[f'camera_{i}']
        # Calculate the camera's horizontal and vertical angle based on its x_offset and y_offset
        camera_horizontal = (camera.x_offset / panorama.get_width()) * 360
        camera_vertical = (camera.y_offset / panorama.get_height()) * 180 - 90  # Assuming full vertical panning is possible

        print(f"Camera {i} is pointing at approximately {camera_horizontal:.2f}° horizontally and {camera_vertical:.2f}° vertically.")


def handle_events():
    global running, number_of_cameras_active,selected_camera
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                new_zoom = min(zoom_slider.max_zoom, zoom_slider.zoom + 0.1)
                zoom_slider.set_zoom(new_zoom)
                calculate_camera_directions()
            elif event.key == pygame.K_DOWN:
                new_zoom = max(zoom_slider.min_zoom, zoom_slider.zoom - 0.1)
                zoom_slider.set_zoom(new_zoom)
                calculate_camera_directions()
            elif event.key == pygame.K_z:
                if number_of_cameras_active < 5:
                    number_of_cameras_active += 1
                    new_zoom = min(zoom_slider.max_zoom, zoom_slider.zoom)
                    zoom_slider.set_zoom(new_zoom)
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                selected_camera = int(event.unicode)
                
            elif event.key == pygame.K_j:
                globals()[f'camera_{selected_camera}'].x_offset -= 10
            elif event.key == pygame.K_l:
                globals()[f'camera_{selected_camera}'].x_offset += 10
            elif event.key == pygame.K_i:
                globals()[f'camera_{selected_camera}'].y_offset -= 10
            elif event.key == pygame.K_k:
                globals()[f'camera_{selected_camera}'].y_offset += 10
            
            elif event.key == pygame.K_x:
                if number_of_cameras_active > 1:
                    number_of_cameras_active -= 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if event.button == 1:  # Left click to center cameras and adjust for panoramic view
                handle_mouse_click(mouse_x, mouse_y)

def adjust_camera_offsets():
    for i in range(1, number_of_cameras_active):
        camera = globals()['camera_' + str(i + 1)]
        previous_camera = globals()['camera_' + str(i)]
        camera.x_offset = (previous_camera.x_offset + get_camera_field_of_view(previous_camera)) % camera.panorama.get_width()
        camera.y_offset = previous_camera.y_offset

def update_views():
    keys = pygame.key.get_pressed()
    cameras_moved = False  # Flag to check if any camera has moved
    for i in range(1, number_of_cameras_active + 1):
        camera = globals()[f'camera_{i}']
        initial_x = camera.x_offset
        initial_y = camera.y_offset
        
        # Update the camera's position based on the arrow keys
        camera_1.update_position(keys, {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s})
        camera_2.update_position(keys, {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s})
        camera_3.update_position(keys, {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s})
        camera_4.update_position(keys, {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s})
        camera_5.update_position(keys, {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s}) 
        
        
        # Check if the camera has moved
        if initial_x != camera.x_offset or initial_y != camera.y_offset:
            cameras_moved = True
    if cameras_moved:
        calculate_camera_directions()


def render():
    screen.fill((0, 0, 0))  # Clear the screen by filling it with black
    
    # Render the main view at the center top of the screen
    main_view.render(screen)  # Main view can occupy the full screen or be static somewhere
    
    # Calculate the width occupied by all cameras and their starting x-coordinate
    total_camera_width = camera_1.view_size[0] * number_of_cameras_active
    start_x = (viewport_size[0] - total_camera_width) // 2
    camera_y = (viewport_size[1] - camera_1.view_size[1]) // 1.3  # Common Y for alignment, adjust if needed

    for i in range (number_of_cameras_active):
        camera = globals()['camera_' + str(i + 1)]
        camera.render(screen, (start_x + i * camera.view_size[0], camera_y))

    # Draw the slider on the screen
    zoom_slider.draw(screen)
    
    # Draw the selected camera number on the screen
    font = pygame.font.Font(None, 30)
    text = font.render(f"Camera {selected_camera} selected", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    #draw the active camera number on the screen
    font = pygame.font.Font(None, 30)
    text = font.render(f"Active cameras: {number_of_cameras_active}", True, (255, 255, 255))
    screen.blit(text, (10, 50))
    
    pygame.display.flip()  # Update the screen with what we've drawn

# Main program setup
init_pygame()
main_view = Viewport(panorama, viewport_size, is_static=True)
number_of_cameras_active = 5
selected_camera = 1
camera_1 = Viewport(panorama, (320, 180))
camera_2 = Viewport(panorama, (320, 180))
camera_3 = Viewport(panorama, (320, 180))
camera_4 = Viewport(panorama, (320, 180))
camera_5 = Viewport(panorama, (320, 180))


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
