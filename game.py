import pygame
from sys import exit

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image_path):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.transform.scale_by(pygame.image.load(image_path).convert(), (2, 2))
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Pipes(pygame.sprite.Group):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.pipe_up = Pipe(x_pos, y_pos, 'Game Objects/pipe-green.png')
        self.pipe_down = Pipe(x_pos, y_pos -   850, 'Game Objects/pipe-green.png')
        self.pipe_down.image = pygame.transform.rotate(self.pipe_down.image,  180)
        self.add(self.pipe_up, self.pipe_down)

def create_pipes(positions):
    pipes_group = pygame.sprite.Group()
    for x_pos, y_pos in positions:
        pipes_group.add(Pipes(x_pos, y_pos))
    return pipes_group
pygame.init()
screen = pygame.display.set_mode((576,1024))
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(pygame.image.load('Game Objects\yellowbird-downflap.png'))

background = pygame.image.load('Game Objects/background-day.png').convert()
background = pygame.transform.scale(background, (576,  1024))
base = pygame.image.load('Game Objects/base.png').convert()
base = pygame.transform.scale(base, (576,  250))

pipes_positions = [(800,  600), (1200,  800), (1600,  370)]
pipes = create_pipes(pipes_positions)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background, (0,  0))

    for pipe in pipes:
        pipe.rect.x -=  2
        if pipe.rect.x < -500:
            pipe.rect.x =  700
        pipes.draw(screen)

    screen.blit(base, (0,  850))

    pygame.display.update()
    clock.tick(144)
