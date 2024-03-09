import pygame

def start_game(screen,base,background):
    screen.blit(background.get_image(), (0,  0))
    screen.blit(base.get_image(), (0,  850))
    screen.blit(pygame.transform.scale_by(pygame.image.load('UI\message.png').convert_alpha(), (2, 2)),((screen.get_width()/2)-190, (screen.get_height()/2)-300))
    pygame.display.update()