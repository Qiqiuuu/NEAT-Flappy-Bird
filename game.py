import pygame

from sys import exit

from classes import Bird, BackGround, Base, ScoreDisplay
from utils import create_pipes,start_game,end_game,reset_game

pygame.init()

screen = pygame.display.set_mode((576,1024))

pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(pygame.image.load('Game Objects\yellowbird-downflap.png'))

background = BackGround()
base = Base()

pipes_positions = [(800,  500), (1200,  300), (1600,  700)]
pipes = create_pipes(pipes_positions)

brid = pygame.sprite.GroupSingle()
bird = Bird(screen)
brid.add(bird)

score = ScoreDisplay((screen.get_width()/2-76), (screen.get_height()/2)+406)

clock = pygame.time.Clock()

game_state = "start"
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if game_state == "start":
        start_game(screen,base,background)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = "game"
            print("Game started")
    elif game_state == "game":
        screen.blit(background.get_image(), (0,  0))

        for pipe in pipes:
            if pipe.rect.x == bird.rect.x:
                score.increase_score()
            pipe.rect.x -=  2
            if pipe.rect.x < -500:
                pipe.rect.x =  700
            pipes.draw(screen)
        screen.blit(base.get_image(), (0,  850))
        score.draw(screen)

        brid.draw(screen)
        bird.update()

        if bird.collision(pipes) or bird.rect.bottom >=  850:
            game_state = end_game(screen)
            reset_game(bird,score,pipes)
            pipes_positions = [(800,  500), (1200,  300), (1600,  700)]
            pipes = create_pipes(pipes_positions) 


    pygame.display.update()
    clock.tick(144)
