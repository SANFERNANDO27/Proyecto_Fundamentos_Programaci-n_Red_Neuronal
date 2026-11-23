'''
This class includes a timer that helps us measure time, a function that makes it easier to draw text on the screen, and
a function for scaling images. It only imports one library: pygame. This library is used for tracking execution time,
scaling images, and handling text.
'''

import pygame

# Draw text on a window
def draw_text(text, color, size, position, window):
    font = pygame.font.Font("assets/font/Flappybird_Number_Font.otf", size)
    img = font.render(text, True, color)
    window.blit(img, position)

# Adjust the size of an image with a factor
def scale_image(image: pygame.surface.Surface, scale: float) -> pygame.surface.Surface:
    return pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

class Timer():
    def __init__(self):
        self.time = 0
        self.update_time = pygame.time.get_ticks()

    # Update the time
    # You always need to call this function for the timer to work
    def update(self):
        self.time = pygame.time.get_ticks() - self.update_time

    # Reset the time to 0
    def reset(self):
        self.update_time = pygame.time.get_ticks()

    # Get the measure in millis
    def get_millie_seconds(self):
        return self.time

    # Get the measure in deci seconds
    def get_deci_seconds(self):
        return self.time/100

    # Get the measure in seconds
    def get_seconds(self):
        return self.time/1000