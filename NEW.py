import pygame
import numpy as np
import cv2


class Viewport:
    def __init__(self, panorama, view_size, x_offset=0, y_offset=0, zoom_level=1.0):
        self.panorama = panorama
        self.view_size = view_size
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.zoom_level = zoom_level

    def capture_image(self):
        visible_width = int(self.view_size[0] / self.zoom_level)
        visible_height = int(self.view_size[1] / self.zoom_level)

        x_offset = int(self.x_offset) % self.panorama.get_width()
        y_offset = int(self.y_offset) % self.panorama.get_height()

        # Adjust for the edges to prevent subsurface error
        if x_offset + visible_width > self.panorama.get_width():
            visible_width = self.panorama.get_width() - x_offset
        if y_offset + visible_height > self.panorama.get_height():
            visible_height = self.panorama.get_height() - y_offset

        visible_part = self.panorama.subsurface(
            (x_offset, y_offset, visible_width, visible_height)
        )
        return pygame.surfarray.array3d(visible_part)

    def adjust_view_zoom(self, direction):
        if direction == "out":
            self.zoom_level = max(0.1, self.zoom_level - 0.1)
        elif direction == "in":
            self.zoom_level = min(2.0, self.zoom_level + 0.1)

    def update_position(self, keys, key_map):
        step_size = 10 / self.zoom_level
        if keys[key_map["left"]]:
            self.x_offset -= step_size
        if keys[key_map["right"]]:
            self.x_offset += step_size
        if keys[key_map["up"]]:
            self.y_offset -= step_size
        if keys[key_map["down"]]:
            self.y_offset += step_size

        self.x_offset %= self.panorama.get_width()
        self.y_offset = max(
            0,
            min(
                self.panorama.get_height() - int(self.view_size[1] / self.zoom_level),
                self.y_offset,
            ),
        )

    def render(self, target_surface, position=(0, 0)):
        visible_width = int(self.view_size[0] / self.zoom_level)
        visible_height = int(self.view_size[1] / self.zoom_level)

        # Adjusting position to ensure it is within bounds
        if self.x_offset + visible_width > self.panorama.get_width():
            visible_width = self.panorama.get_width() - int(self.x_offset)
        if self.y_offset + visible_height > self.panorama.get_height():
            visible_height = self.panorama.get_height() - int(self.y_offset)

        visible_part = self.panorama.subsurface(
            (int(self.x_offset), int(self.y_offset), visible_width, visible_height)
        )
        visible_part_scaled = pygame.transform.scale(visible_part, self.view_size)
        target_surface.blit(visible_part_scaled, position)


def main():
    pygame.init()
    screen = pygame.display.set_mode((960, 480))
    panorama = pygame.image.load("vignaioli_night.jpg").convert()
    viewports = [
        Viewport(panorama, (320, 240), x_offset=0),
        Viewport(panorama, (320, 240), x_offset=320),
        Viewport(panorama, (320, 240), x_offset=640),
    ]
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                zoom_direction = "in" if event.button == 1 else "out"
                for viewport in viewports:
                    viewport.adjust_view_zoom(zoom_direction)

        keys = pygame.key.get_pressed()
        key_map = {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "up": pygame.K_w,
            "down": pygame.K_s,
        }
        for viewport in viewports:
            viewport.update_position(keys, key_map)

        screen.fill((0, 0, 0))
        for i, viewport in enumerate(viewports):
            viewport.render(screen, (i * 320, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
