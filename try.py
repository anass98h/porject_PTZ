import pygame
import sys

def init_pygame():
    pygame.init()
    global panorama, viewport_size, screen
    viewport_size = (1920, 1080)
    screen = pygame.display.set_mode(viewport_size, pygame.DOUBLEBUF)
    pygame.display.set_caption('360 Panorama Viewer')
    image_path = 'vignaioli_night.jpg'
    panorama = pygame.image.load(image_path).convert()

class Viewport:
    def __init__(self, panorama, view_size, x_offset=0, y_offset=0, zoom_level=1.0):
        self.panorama = panorama
        self.view_size = view_size
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.zoom_level = zoom_level

    def zoom_in(self, mouse_pos=None):
        if mouse_pos:
            self.adjust_view_zoom(mouse_pos, 'in')
        else:
            self.adjust_view_zoom((self.view_size[0]//2, self.view_size[1]//2), 'in')

    def zoom_out(self, mouse_pos=None):
        if mouse_pos:
            self.adjust_view_zoom(mouse_pos, 'out')
        else:
            self.adjust_view_zoom((self.view_size[0]//2, self.view_size[1]//2), 'out')

    def adjust_view_zoom(self, mouse_pos, direction):
        old_zoom_level = self.zoom_level
        if direction == 'out':
            self.zoom_level = max(0.1, self.zoom_level - 0.1)
        elif direction == 'in':
            self.zoom_level = min(2.0, self.zoom_level + 0.1)

        zoomed_width = int(self.view_size[0] / self.zoom_level)
        zoomed_height = int(self.view_size[1] / self.zoom_level)
        mouse_x, mouse_y = mouse_pos

        self.x_offset = (self.x_offset + mouse_x / old_zoom_level) - zoomed_width / 2
        self.y_offset = (self.y_offset + mouse_y / old_zoom_level) - zoomed_height / 2

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

    def render(self, target_surface, position):
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

def handle_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click to zoom in on main view
                main_view.zoom_in(event.pos)
            elif event.button == 3:  # Right click to zoom out on main view
                main_view.zoom_out(event.pos)

def update_views():
    keys = pygame.key.get_pressed()
    main_view.update_position(keys, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN})
    camera_view.update_position(keys, {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s})
    if keys[pygame.K_q]:
        camera_view.zoom_out()
    if keys[pygame.K_e]:
        camera_view.zoom_in()

def render():
    screen.fill((0, 0, 0))
    main_view.render(screen, (0, 0))
    camera_view.render(screen, (viewport_size[0] - camera_view.view_size[0] - 10, 10))  # Position the camera view in the top right corner
    pygame.display.flip()

# Main program setup
init_pygame()
main_view = Viewport(panorama, viewport_size)
camera_view = Viewport(panorama, (320, 180))
running = True
clock = pygame.time.Clock()

while running:
    handle_events()
    update_views()
    render()
    clock.tick(60)  # Maintain 60 FPS

pygame.quit()
sys.exit()
