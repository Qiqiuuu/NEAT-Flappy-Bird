from .create_pipes import create_pipes

def reset_game(bird,score,pipes):
    bird.rect.x =  80
    bird.rect.y =  450
    bird.gravity =  0
    bird.brid_index =  0
    pipes.empty()
    score.reset_score()