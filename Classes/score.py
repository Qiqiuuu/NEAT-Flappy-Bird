import pygame

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

    #Score reset
    def reset_score(self):
        self.score = 0 

    #Increase Score
    def increase_score(self):
        self.score += 0.5