import pygame

import constants


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Define img
        self.image = pygame.Surface((70, 70))
        self.image.fill("red")

        # Define and configure rect
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Jumping and Gravity
        self.delta_y = 0
        self.jumping = False

    def jump(self):
        self.delta_y = -constants.JUMPING_VELOCITY

    def set_jump(self):
        self.jumping = True

    def gravity(self):
        self.delta_y += constants.GRAVITY

        # Max velocity 10 px/sec
        self.rect.y += min(self.delta_y, 10)

    def draw(self, window):
        pygame.draw.rect(window, "red", self.rect)

    def update(self):
        self.gravity()

