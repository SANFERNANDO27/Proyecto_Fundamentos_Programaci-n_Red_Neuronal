import pygame

import constants

class Dynamic_Object(pygame.sprite.Sprite):
    def __init__(self, x, y, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = (x, y)

    def move(self):
        self.rect.x -= constants.DELTA_X

        # kill the object if  pass through window
        if self.rect.right < 0:
            self.kill()

    def draw(self, window, draw_hitbox = False):
        #draw image
        window.blit(self.image, self.rect)
        # Draw hitbox
        if draw_hitbox:
            pygame.draw.rect(window, pygame.Color("red"), self.rect, 1)

    def update(self):
        self.move()