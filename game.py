import pygame
from sys import exit


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image_path):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.transform.scale_by(pygame.image.load(image_path).convert(), (2, 2))
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
    def draw(self):
        screen.blit(self.image, self.rect)

class Pipes(pygame.sprite.Group):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.pipe_up = Pipe(x_pos, y_pos, 'Game Objects/pipe-green.png')
        self.pipe_down = Pipe(x_pos, y_pos -   850, 'Game Objects/pipe-green.png')
        self.pipe_down.image = pygame.transform.rotate(self.pipe_down.image,  180)
        self.add(self.pipe_up, self.pipe_down)

class Bird(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        bird_fly_1 = pygame.transform.scale_by(pygame.image.load('Game Objects\yellowbird-upflap.png').convert(), (2, 2))
        bird_fly_2 = pygame.transform.scale_by(pygame.image.load('Game Objects\yellowbird-midflap.png').convert(), (2, 2))
        bird_fly_3 = pygame.transform.scale_by(pygame.image.load('Game Objects\yellowbird-downflap.png').convert(), (2, 2))
        self.bird_fly = [bird_fly_1,bird_fly_2,bird_fly_3]
        self.brid_index = 0
        self.screen = screen

        self.image = self.bird_fly[self.brid_index]
        self.rect = self.image.get_rect(topleft=(80,450))
        self.last_update = pygame.time.get_ticks()  
        self.animation_speed =  150
        self.gravity = 0

    def draw(self):
        self.screen.blit(self.image,self.rect)

    def animation_state(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed:
            self.last_update = current_time
            self.brid_index = (self.brid_index +  1) % len(self.bird_fly)
            self.image = self.bird_fly[self.brid_index]

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -3
    
    def apply_gravity(self):
        self.gravity +=0.1
        self.rect.y += self.gravity


    def update(self):
        self.animation_state()
        self.apply_gravity()
        self.player_input()

    def collision(self, pipes):
        return pygame.sprite.spritecollideany(self, pipes) is not None

class BackGround():
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('Game Objects/background-day.png').convert(), (576,1024))
    def get_image(self):
        return self.image

class Base():
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('Game Objects/base.png').convert(), (576,  250))
    def get_image(self):
        return self.image

class ScoreDisplay:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0.0
        self.digit_images = {}
        for i in range(10):
            self.digit_images[i] = pygame.transform.scale_by(pygame.image.load(r'UI\Numbers\{}.png'.format(i)).convert_alpha(), (2, 2))

    def draw(self, screen):
        score_str = "{:03}".format(int(self.score))
        for i, digit in enumerate(score_str):
            digit_image = self.digit_images[int(digit)]
            if digit == '1':
                x = self.x + (i * (digit_image.get_width() + 21))
            else:
                x = self.x + (i * (digit_image.get_width()))
            screen.blit(digit_image, (x, self.y))
        

    def increase_score(self):
        self.score += 0.5

    def reset_score(self):
        self.score = 0 


def EndGame(screen):
    pygame.time.delay(100)
    pygame.mixer.init()
    pygame.mixer.music.load('Sound Efects\die.wav') 
    pygame.mixer.music.play() 
    endgame_surf = pygame.transform.scale_by(pygame.image.load('UI\gameover.png').convert_alpha(), (2, 2))
    screen.blit(endgame_surf,((screen.get_width()/2)-190, (screen.get_height()/2)-100))
    pygame.display.update()
    pygame.time.wait(2000)
    return "start"


def StartGame(screen,base,background):
    screen.blit(background.get_image(), (0,  0))
    screen.blit(base.get_image(), (0,  850))
    screen.blit(pygame.transform.scale_by(pygame.image.load('UI\message.png').convert_alpha(), (2, 2)),((screen.get_width()/2)-190, (screen.get_height()/2)-300))
    pygame.display.update()

def reset_game():
    global pipes
    bird.rect.x =  80
    bird.rect.y =  450
    bird.gravity =  0
    bird.brid_index =  0

    pipes.empty()
    pipes_positions = [(800,  500), (1200,  300), (1600,  700)]
    pipes = create_pipes(pipes_positions) 
    score.reset_score()

def create_pipes(positions):
    pipes_group = pygame.sprite.Group()
    for x_pos, y_pos in positions:
        pipes_group.add(Pipes(x_pos, y_pos))
    return pipes_group
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
        StartGame(screen,base,background)
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
            game_state = EndGame(screen)
            reset_game()


    pygame.display.update()
    clock.tick(144)
