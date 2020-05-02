
# Import Python functions
import math
import numpy as np
import pygame
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch


# Import our own functions
from trigfunctions import*
from classes import car

class Window():
    def __init__(self,game):
        
        # Fixed width and height which do not ever change
        self.width=1000
        self.height=400
        self.win = pygame.display.set_mode((self.width, self.height))

        # Position of the upper left corner of the viewing window, in world coordinates; Moves with the orange car
        self.x=500
        self.y=500


    def redrawGameWindow(self):
        # Redraw background
        self.win.blit(self.bg, (int(self.bgX), 0))  # draws our first bg image
        self.win.blit(self.bg, (int(self.bgX2), 0))  # draws the seconf bg image

        # Redraw all cars
        for sprite in game.all_sprites:
            # only blit items on screen
                # car is to the left of the window                car is to the right of the window         car is above window             car is below window
            if (sprite.spritex+sprite.car_width_px<window.x) or (sprite.spritex>window.x+window.width) or (sprite.spritey<window.y) or (sprite.spritey+sprite.car_height_px>window.y+window.height):
                pass
            else:
                self.win.blit(sprite.car_image_new,(int(sprite.spritex),int(sprite.spritey)))

        pygame.display.update()



class World():
    def __init__(self,game):

        self.window=Window(game)
        self.width=4000
        self.height=1600
        self.generateBlueCars(game)
        self.generateGreenCars(game)
        self.showWorldMap(game)


    def generateBlueCars(self,game):
    # Create stationary cars
        print("Populating Blue cars")
        start_pos_list=[(130,220),(200,330),(500,10)]

        for start_pos in start_pos_list:
            x,y=start_pos
            new_obst=car(x,y,"obstacle")
            game.obst_list.add(new_obst)
            game.all_sprites.add(new_obst)



    def generateGreenCars(self,game):
        # Create dynamic cars
        print("Populating Green cars")
        for i in range (0,random.randint(1,3)):
            # tempcar=car(0,0,"dynamic")
            randx=random.randint(100,900)
            randy=random.randint(50,350)
            # # Eliminate cars on the lane lines
            # if (100-tempcar.car_height<=randy<=100+tempcar.car_height) or (200-tempcar.car_height<=randy<=200+tempcar.car_height) or (300-tempcar.car_height<=randy<=300+tempcar.car_height):
            #     randy=random.randint(50,350)
            game.active_list.add(car(randx,randy,"dynamic"))
            game.all_sprites.add(car(randx,randy,"dynamic"))
        # tempcar.kill()
        # obst_list=[]


    def showWorldMap(self,game):
        # plt.figure(1)
        fig, ax = plt.subplots(1)
        ax.set_xlim(0,self.width)
        ax.set_ylim(0,self.height)
        ax.invert_yaxis()
        fig.title("World Map")
        ax.grid()
        ax.set_aspect('equal')

        # Draw all cars as rectangles
        for sprite in game.all_sprites:
            a=Rectangle((sprite.spritex,sprite.spritey),sprite.car_width,sprite.car_height, fc=sprite.body_color, angle=sprite.theta,alpha=.5)
            ax.add_patch(a)

        win_box=Rectangle((self.window.x,self.window.y),self.window.width,self.window.height,fill=None, ec='black', lw=3, angle=0)
        ax.add_patch(win_box)

        fig.show()

        plt.figure(2)
        plt.title("Window View")
        fig2, ax2 = plt.subplots(1)
        ax2.set_xlim(0,self.window.width)
        ax2.set_ylim(0,self.window.height)
        ax2.invert_yaxis()
        ax2.grid()
        ax2.set_aspect('equal')
        fig2.show()

        plt.show()
    # def generateRandomObstacle(self):
    #     # print("Attempting to spawn a new blue car")
    #     randx=random.randint(1000,2000)
    #     randy=random.randint(10,350)
    #     new_obst=car(randx,randy,"obstacle")
    #     # a=pygame.sprite.spritecollide(car(randx,randy,"obstacle"), obst_list, True)
    #     # print(a)
    #     self.obst_list.add(new_obst)
    #     self.all_sprites.add(new_obst)

    #     # return self.obst_list


class car_game():
    def __init__(self):
        pygame.init()

        self.road_speed=1.6

        # Set up canvas
        self.clock = pygame.time.Clock()
        self.run = True

        # Set up background
        self.bg = pygame.image.load('assets/road.png')
        self.bgX = 0
        self.bgX2 = self.bg.get_width()

        self.all_sprites = pygame.sprite.Group()
        self.obst_list = pygame.sprite.Group()
        self.active_list=pygame.sprite.Group()

        # Create our car
        self.orange_car=car(10,225,"protagonist")
        self.all_sprites.add(self.orange_car)

    


