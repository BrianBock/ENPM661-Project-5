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

world.window.redrawGameWindow(game,world.WorldSize_px)
path='world_files/'+game.gameMode+'.png'
pygame.image.save(world.window.win,path)
print("Image saved to '"+path+"'")

pygame.quit()
