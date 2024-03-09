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