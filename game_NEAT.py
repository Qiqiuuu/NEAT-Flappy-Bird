import pygame
from sys import exit
import neat

#Class of single pipe
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image_path):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.transform.scale_by(pygame.image.load(image_path).convert(), (2, 2))
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
    def draw(self,screen):
        screen.blit(self.image, self.rect)

#Class of pipe row (top and bottom)
class Pipes(pygame.sprite.Group):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.pipe_up = Pipe(x_pos, y_pos, 'Game Objects/pipe-green.png')
        self.pipe_down = Pipe(x_pos, y_pos -   850, 'Game Objects/pipe-green.png')
        self.pipe_down.image = pygame.transform.rotate(self.pipe_down.image,  180)
        self.add(self.pipe_up, self.pipe_down)

#Bird Class
class Bird(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        #Load bird image
        self.bird_fly = [
            pygame.transform.scale_by(pygame.image.load('Game Objects\yellowbird-upflap.png').convert(), (2, 2)),
            pygame.transform.scale_by(pygame.image.load('Game Objects\yellowbird-midflap.png').convert(), (2, 2)),
            pygame.transform.scale_by(pygame.image.load('Game Objects\yellowbird-downflap.png').convert(), (2, 2))
            ]
        self.brid_index = 0
        self.screen = screen
        
        self.image = self.bird_fly[self.brid_index]
        self.rect = self.image.get_rect(topleft=(80,450))
        self.last_update = pygame.time.get_ticks()  
        self.animation_speed =  150
        self.gravity = 0
        self.distance_traveled = 0
        self.score = 0

    #Increase birds score
    def increase_score(self):
        self.score += 0.5

    #Score getter
    def get_sc(self):
        return self.score
    
    #draw function
    def draw(self):
        self.screen.blit(self.image,self.rect)

    #Update animation
    def animation_state(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed:
            self.last_update = current_time
            self.brid_index = (self.brid_index +  1) % len(self.bird_fly)
            self.image = self.bird_fly[self.brid_index]

    #Neat space controll
    def neat_space(self):
        self.gravity = -3

    #Bird gravity
    def apply_gravity(self):
        self.gravity +=0.1
        self.rect.y += self.gravity
    
    #Distance updater
    def distance(self):
        self.distance_traveled+=1
    
    #Update function
    def update(self):
        self.animation_state()
        self.apply_gravity()
        self.distance()

    #Check collisions
    def collision(self, pipes):
        return pygame.sprite.spritecollideany(self, pipes) is not None
    #Distance getter
    def get_dis(self):
        return self.distance_traveled

#Background(sky) Class
class BackGround():
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('Game Objects/background-day.png').convert(), (576,1024))
    def get_image(self):
        return self.image

#Base Class
class Base():
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('Game Objects/base.png').convert(), (576,  250))
    def get_image(self):
        return self.image

#ScoreDisplay Class
class ScoreDisplay:
    def __init__(self, x, y,):
        self.x = x
        self.y = y
        self.score = 0
        self.digit_images = {}
        #image loader
        for i in range(10):
            self.digit_images[i] = pygame.transform.scale_by(pygame.image.load(r'UI\Numbers\{}.png'.format(i)).convert_alpha(), (2, 2))

    #Gets score and draws it
    def draw(self, screen):
        score_str = "{:03}".format(int(self.score))
        for i, digit in enumerate(score_str):
            digit_image = self.digit_images[int(digit)]
            if digit == '1':
                x = self.x + (i * (digit_image.get_width() + 21))
            else:
                x = self.x + (i * (digit_image.get_width()))
            screen.blit(digit_image, (x, self.y))

    #Score Setter
    def score_set(self,new_score):
        self.score = new_score
        
#Current game state that feeds NEAT algorythm
def game_state_neat_feed(bird,pipes,score):
    bird_position = bird.rect.y/ 1024
    closest_pipe = min(pipes, key=lambda pipe: abs(pipe.rect.x-bird.rect.x))
    closest_pipe = closest_pipe.rect.y/1024
    return [bird_position,closest_pipe,score.score,bird.get_dis()]

#Pipes function
def create_pipes(positions):
    pipes_group = pygame.sprite.Group()
    for x_pos, y_pos in positions:
        pipes_group.add(Pipes(x_pos, y_pos))
    return pipes_group

#Function that takes score,distance,colliison and returns run score to fitness algorythm
def calculate_fitness(bird,pipes,score):
    fitness = 0
    sn = 0
    if score.score > sn:
        fitness+=200
        sn = score.score
    
    if bird.rect.bottom >=  850 or bird.rect.bottom<0:
        fitness -=  1000
    if bird.collision(pipes):
        fitness -= 50

    fitness+=bird.get_dis()
    return fitness

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
