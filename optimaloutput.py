import numpy as np
import random
#for vector stuff
import pygame
import math

#program makes it move around, records the power output at each point, and locates the highest output point

#this function may prove obsolete
def get_output():
    """would put opm's get output here"""
    return random.randint(1,10)

size = 10
grid = [random.sample(range(1,11),size) for i in range(size)]

def sim_move(curr_pos, fin_pos, speed):
    direction = fin_pos - curr_pos
    distance = direction.length()
    if distance == 0:
        return curr_pos
    direction.normalize_ip()
    step = min(speed, distance) 

    return curr_pos + direction * step


#size of movement area
def find_optimal():
    global grid
    max_point = pygame.math.Vector2(0,0)
    max_val = grid[0][0]
    pos = pygame.math.Vector2(0,0)
    #i is x val, j is y val, that thing moves to, finding the power output at that spot
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            """change to while opm pos func"""
            fin_pos = pygame.math.Vector2(i,j)
            while pos.distance_to(fin_pos) > 0:
                """insert real move func here"""
                pos = sim_move(pos, fin_pos, speed=0.1)
                print(pos)
            """change to opm reading"""
            #max_point = max(grid[int(max_point.x)][int(max_point.y)],grid[int(pos.x)][int(pos.y)])
            if grid[i][j] > max_val:
                max_val = grid[i][j]
                max_point = fin_pos
    return max_point

print(grid)
print(find_optimal())