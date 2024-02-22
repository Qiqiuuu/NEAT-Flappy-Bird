import pygame
from sys import exit
import os
print(os.getcwd())


pygame.init()
#iniciate gamescreen
screen = pygame.display.set_mode((1080,720))
#name and icon
pygame.display.set_caption('Flappy Bird')
# pygame.display.set_icon(pygame.image.load('Qiqiuuu/flappy-bird-ai/orzel.jpg'))

background = pygame.image.load('Game Objects/background-day.png')
base = pygame.image.load('Game Objects/base.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background,(0,0))
    screen.blit(base, (365, 495))

    #update screen
    pygame.display.update()
    pygame.clock.tick(60)
