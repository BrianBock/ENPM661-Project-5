# Import Python functions
import pygame
import pickle
from time import time
import math
import random
import sys
sys.path.append("../")

# Import our own functions
from classes.car_class import car
from classes.window_class import Window
from classes.world_class import World
from classes.game_class import car_game
import statespace
import motionplanning
import logResults



difficulty = "Easy" #Easy, Medium, Hard, Extreme, Random
photoMode = False


print("Starting game")
game=car_game(difficulty) # Instantiate game

print("Generating world")
world=World(game) # Generate world



world.window.width_px=world.WorldSize_px[0]
world.window.height_px=world.WorldSize_px[1]
world.window.win = pygame.display.set_mode((world.window.width_px, world.window.height_px))

world.window.x=0
world.window.y=0

game.orange_car.spritex=440
game.orange_car.spritey=320
# world.window.redrawGameWindow()

needPhoto=True




photo=Photo(world)



# Run the game
while game.run:
    game.clock.tick(100)

    # Get new events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False


    # world.updateWinPos(game)
    world.window.redrawGameWindow(game,world.WorldSize_px) 
    if needPhoto:
            pygame.image.save(world.window.win,game.gameMode+'.png')
            needPhoto=False
            game.run=False

pygame.quit()
