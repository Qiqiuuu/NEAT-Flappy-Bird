import pygame

#Background(sky) Class
class BackGround():
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('Game Objects/background-day.png').convert(), (576,1024))
    def get_image(self):
        return self.image