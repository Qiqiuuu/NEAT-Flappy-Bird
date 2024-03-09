import pygame
import neat

from sys import exit


from classes import Bird, BackGround, Base, ScoreDisplay
from utils import create_pipes, calculate_fitness, game_state_neat_feed


#Game running function
def run_game(genomes,config):
    global GENERATION,SC

    
    pygame.init()

    #Game start and overlay
    screen = pygame.display.set_mode((576,1024))
    pygame.display.set_caption('Flappy Bird')
    pygame.display.set_icon(pygame.image.load('Game Objects\yellowbird-downflap.png'))
    font = pygame.font.SysFont("Arial",  24)
    text = font.render("Current generation: {}      Highest Score: {}".format(GENERATION, int(SC)), True, (255,  255,  255))

    #Create background
    background = BackGround()
    base = Base()

    #Creates pipes
    pipes_positions = [(800,  500), (1300,  300), (1800,  700)]
    pipes = create_pipes(pipes_positions)

    #Create score
    score = ScoreDisplay((screen.get_width()/2-76), (screen.get_height()/2)+406)
    

    clock = pygame.time.Clock()

    #Multi birds storage
    models_list = []
    genomes_list = []
    birds_list = []

    #Each genome in a run
    for genome_id, genome in genomes:
        birds_list.append(Bird(screen))
        genome.fitness = 0 
        genomes_list.append(genome) 
        model = neat.nn.FeedForwardNetwork.create(genome, config) 
        models_list.append(model)

    GENERATION+=1

    #Main Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        #Background visualization
        screen.blit(background.get_image(), (0,  0))

        #Pipe movement and visualization
        for pipe in pipes:
            pipe.rect.x -=  2
            if pipe.rect.x < -500:
                pipe.rect.x =  1000
            pipes.draw(screen)

        #Score and base visualization
        screen.blit(base.get_image(), (0,  850))
        score.draw(screen)

        #Each bird action
        for index, bird in enumerate(birds_list):
            #NEAT Update
            net_input = game_state_neat_feed(bird,pipes,score)
            output = models_list[index].activate(net_input)
            if output[0]>0.5:
                bird.neat_space()
            
            #Pipe score check
            for pipe in pipes:
                if pipe.rect.x == bird.rect.x:
                    bird.increase_score()
                    if SC<bird.get_sc():
                        SC = bird.get_sc()
                    score.score_set(bird.get_sc())
                    score.draw(screen)

            #Bird collision check
            if bird.collision(pipes) or bird.rect.bottom >=  850 or bird.rect.bottom<0:
                genomes_list[index].fitness = calculate_fitness(bird,pipes,score)
                if score.score>SC:
                    SC = score.score
            
                models_list.pop(index)
                genomes_list.pop(index)
                birds_list.pop(index)

            #Bird draw and update
            bird.draw()
            bird.update()
        
        #Checks if theres any bird left
        if  len(birds_list) == 0:
            break

        #Generation and Score Display
        screen.blit(text, (0,0))

        # Update the window
        pygame.display.update()
        clock.tick(144)



#NEAT Config, post results and runner
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'neat-config.txt')
pop = neat.Population(config)
pop.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
pop.add_reporter(stats)

GENERATION = 0
SC = 0

pop.run(run_game,100)
