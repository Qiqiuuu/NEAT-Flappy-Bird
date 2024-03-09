import pygame

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

    #Player control
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -3

    #Neat space control
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
        self.player_input()

    #Check collisions
    def collision(self, pipes):
        return pygame.sprite.spritecollideany(self, pipes) is not None
    #Distance getter
    def get_dis(self):
        return self.distance_traveled