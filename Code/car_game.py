# Import Python functions
import pygame
import pickle
from time import time
import math
import random

# Import our own functions
from classes.car_class import car
from classes.window_class import Window
from classes.world_class import World
from classes.game_class import car_game
import statespace
import motionplanning
import logResults

difficulty="Easy" #Easy, Medium, Hard, Extreme, Random


print("Starting game")
game=car_game(difficulty) # Instantiate game

print("Generating world")
world=World(game) # Generate world

# print("Generating roadmap for solver")
# Map = statespace.RoadMap(game, world)
# print("Attempting to solve")
# planner = motionplanning.SamplingPlanner(Map,game)
# t0 = time()
# solved, plan, exploredNodes, _ = planner.RRT(game)
# t1 = time() 
# if solved: 
#     print(f'Path found in {t1-t0} s\n')
# else:
#     print('Path not found')

# motionplanning.Simulation(Map, game, plan, exploredNodes)
# # logResults(plan, Map) 

actions = [] # L for left lane change, R for right lane change, number for seconds going straight

for i in range(10):
    act = random.randint(0,2)
    if act == 0:
        actions.append('L')
    if act == 1:
        actions.append('R')
    if act == 2:
        t = random.randint(1,5)
        actions.append(t)

print(actions)

busy = False
angle = 0
turn_increment = 15

# Run the game
while game.run:
    game.clock.tick(100)

    # Update green cars
    for active_car in game.active_list:
        active_car.spritex+=active_car.vel
        active_car.updateCarOrigin()

    # Get new events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False

    keys = pygame.key.get_pressed()

    t = pygame.time.get_ticks()

    if not busy and actions:
        action = actions.pop(0)
        start_time = t
        busy = True

        if action == 'L':
            angle = turn_increment
            lane_change_time = 1.32
        elif action == 'R':
            angle = -turn_increment
            lane_change_time = 1.4
        else:
            angle = 0

    if angle != 0:
        if t-start_time <= ((lane_change_time)*1000)/2:
            game.orange_car.turnCar(angle)  
        elif game.orange_car.theta*(angle/abs(angle)) > 0:
            game.orange_car.turnCar(-angle)
        else:
            game.orange_car.theta = 0
            busy = False 

    elif angle == 0:
        if t-start_time <= action*1000:
            game.orange_car.turnCar(angle)
        else:
            busy = False

    world.updateWinPos(game)
    world.window.redrawGameWindow(game,world.WorldSize_px) 
        
    if keys[pygame.K_q]:
        pygame.quit()
        game.run=False

pygame.quit()
