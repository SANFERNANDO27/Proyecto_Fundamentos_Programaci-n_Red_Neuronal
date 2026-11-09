import pygame

def draw_text(text, color, size, position, window):
    font = pygame.font.Font("assets/font/Flappybird_Number_Font.otf", size)
    img = font.render(text, True, color)
    window.blit(img, position)

class Timer():
    def __init__(self):
        self.time = 0
        self.update_time = pygame.time.get_ticks()

    def update(self):
        self.time = pygame.time.get_ticks() - self.update_time

    def reset(self):
        self.update_time = pygame.time.get_ticks()

    def get_millie_seconds(self):
        return self.time

    def get_deci_seconds(self):
        return self.time/100

    def get_seconds(self):
        return self.time/1000