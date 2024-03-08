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