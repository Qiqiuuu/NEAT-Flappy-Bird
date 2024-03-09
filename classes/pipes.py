import pygame
from .pipe import Pipe

#Class of pipe row (top and bottom)
class Pipes(pygame.sprite.Group):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.pipe_up = Pipe(x_pos, y_pos, 'Game Objects/pipe-green.png')
        self.pipe_down = Pipe(x_pos, y_pos -   850, 'Game Objects/pipe-green.png')
        self.pipe_down.image = pygame.transform.rotate(self.pipe_down.image,  180)
        self.add(self.pipe_up, self.pipe_down)
