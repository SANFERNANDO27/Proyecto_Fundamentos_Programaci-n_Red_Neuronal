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

class BackgroundDynamicImage(Dynamic_Object):
    def __init__(self, image: pygame.Surface):
        image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.x = 0
        self.y = constants.WINDOW_HEIGHT - self.height / 2

        super().__init__(self.x, self.y, image)

        self.rect2 = image.get_rect()
        self.rect2.center = (self.rect.x + self.width * 1.5, self.y)
        self.rect_list = [self.rect, self.rect2]
        self.rect_index = 0

    def draw(self, window):
        window.blit(self.image, self.rect)
        window.blit(self.image, self.rect2)

        if self.rect_list[self.rect_index].right < 0:
            self.rect_list[self.rect_index].x = self.rect_list[self.rect_index - 1].x + self.width
            self.rect_index += 1

        if self.rect_index >= len(self.rect_list):
            self.rect_index = 0

    def move(self):
        self.rect.x -= constants.DELTA_X
        self.rect2.x -= constants.DELTA_X