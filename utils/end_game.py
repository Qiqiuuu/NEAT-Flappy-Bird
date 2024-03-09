import pygame

def end_game(screen):
    pygame.time.delay(100)
    pygame.mixer.init()
    pygame.mixer.music.load('Sound Efects\die.wav') 
    pygame.mixer.music.play() 
    endgame_surf = pygame.transform.scale_by(pygame.image.load('UI\gameover.png').convert_alpha(), (2, 2))
    screen.blit(endgame_surf,((screen.get_width()/2)-190, (screen.get_height()/2)-100))
    pygame.display.update()
    pygame.time.wait(2000)
    return "start"