#Current game state that feeds NEAT algorythm
def game_state_neat_feed(bird,pipes,score):
    bird_position = bird.rect.y/ 1024
    closest_pipe = min(pipes, key=lambda pipe: abs(pipe.rect.x-bird.rect.x))
    closest_pipe = closest_pipe.rect.y/1024
    return [bird_position,closest_pipe,score.score,bird.get_dis()]