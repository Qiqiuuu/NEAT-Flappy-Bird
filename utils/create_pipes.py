import pygame
from classes import Pipes

#Pipes function
def create_pipes(positions):
    pipes_group = pygame.sprite.Group()
    for x_pos, y_pos in positions:
        pipes_group.add(Pipes(x_pos, y_pos))
    return pipes_group