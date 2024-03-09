import pygame

#Base Class
class Base():
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('Game Objects/base.png').convert(), (576,  250))
    def get_image(self):
        return self.image