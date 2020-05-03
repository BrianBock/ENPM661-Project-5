
# Import Python functions
import math
import numpy as np
import pygame
import random
import cv2
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch


# Import our own functions
from trigfunctions import*
from classes import car

class Window():
    def __init__(self,game,WorldSize_px):
        pygame.init()
        # Fixed width and height which do not ever change
        self.width_m=30 # meters
        self.height_m=13 # meters

        self.width_px=self.width_m*game.pixpermeter
        self.height_px=self.height_m*game.pixpermeter
        self.win = pygame.display.set_mode((self.width_px, self.height_px))


        # Position of the upper left corner of the viewing window, in world coordinates (pix); Moves with the orange car
        self.x=0
        self.y=170
        self.vel=10

        self.lane_width=90 # px


        # Import assets
        self.lane_line = pygame.image.load('assets/lane_line_long.png')
        self.solid_line = pygame.image.load('assets/solid_line.png')
        self.grass = pygame.image.load('assets/grass.jpg')
        self.grass = pygame.transform.scale(self.grass, (self.lane_width,self.lane_width))
 


    def redrawGameWindow(self,game,WorldSize_px):
        # Redraw background
        self.win.fill((56,56,59))
        


        self.lane_count=4
        
        # Redraw shoulder lines
        top_shoulder_pos=2*self.lane_width-self.y
        bot_shoulder_pos=WorldSize_px[1]-2*self.lane_width-self.y
            # only draw the lines that would be visible (for speed)
        if top_shoulder_pos<=self.y+self.height_px:
            self.win.blit(self.solid_line,(0-self.x,top_shoulder_pos))

        if bot_shoulder_pos<=self.y+self.height_px:
            self.win.blit(self.solid_line,(0-self.x,bot_shoulder_pos))


        # Draw grass past shoulder (top)
        if self.y<self.grass.get_height():
            self.win.blit(self.grass,(0,0-self.y))

            grass_count=WorldSize_px[0]//self.grass.get_width()
            for i in range(grass_count):
                grass_pos=i*self.grass.get_width()
                if grass_pos<self.x+self.width_px:
                    self.win.blit(self.grass,(grass_pos-self.x,0-self.y))


        # Draw grass past shoulder (bottom)
        if self.y+self.height_px>WorldSize_px[1]-self.grass.get_height():
            self.win.blit(self.grass,(0,WorldSize_px[1]-self.grass.get_height()-self.y))

            grass_count=WorldSize_px[0]//self.grass.get_width()
            for i in range(grass_count):
                grass_pos=i*self.grass.get_width()
                if grass_pos<self.x+self.width_px:
                    self.win.blit(self.grass,(grass_pos-self.x,WorldSize_px[1]-self.grass.get_height()-self.y))


        # Redraw lane lines
        for i in range(self.lane_count-1):
            lane_pos=i*self.lane_width-self.y+3*self.lane_width
            # only draw the lines that would be visible (for speed)
            if lane_pos<=self.y+self.height_px:
                self.win.blit(self.lane_line,(0-self.x,lane_pos))

        # Redraw all cars
        for sprite in game.all_sprites:
            # only blit items on screen
                # car is to the left of the window                car is to the right of the window         car is above window             car is below window
            if (sprite.spritex+sprite.car_width_px<self.x) or (sprite.spritex>self.x+self.width_px) or (sprite.spritey+sprite.car_height_px<self.y) or (sprite.spritey>self.y+self.height_px):
                pass
            else:
                self.win.blit(sprite.car_image_new,(int(sprite.spritex-self.x),int(sprite.spritey-self.y)))

        pygame.display.update()



class World():
    def __init__(self,game):

        self.width_m=200 # meters
        self.height_m=24 # meters

        self.width_px=self.width_m*game.pixpermeter
        self.height_px=self.height_m*game.pixpermeter

        self.WorldSize_px=(self.width_px,self.height_px)

        self.window=Window(game, self.WorldSize_px)

        print

        # self.width_px=4000
        # self.height_px=1600


        self.generateBlueCars(game)
        self.generateGreenCars(game)
        # self.showWorldMap(game)



        # Create our car
        game.orange_car=car(410,395,"protagonist")
        game.all_sprites.add(game.orange_car)


    def generateBlueCars(self,game):
    # Create stationary cars
        print("Populating Blue cars")
        start_pos_list=[(130,220),(200,330),(500,200)]

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


    def moveWindow(self,keys,game):

        if keys[pygame.K_LEFT] and self.window.x > self.window.vel: 
            self.window.x -= self.window.vel

        elif keys[pygame.K_RIGHT] and self.window.x < (self.width_px - self.window.vel - self.window.width_px):
            self.window.x += self.window.vel

        if keys[pygame.K_DOWN] and self.window.y <(self.height_px-self.window.vel-self.window.height_px):
            self.window.y+=self.window.vel

        elif keys[pygame.K_UP] and self.window.y > self.window.vel:
            self.window.y-=self.window.vel

        print(self.window.x,self.window.y)
        game.orange_car.x=self.window.x+self.window.width_px//2
        game.orange_car.y=self.window.y+self.window.height_px//2
        game.orange_car.updateSpriteOrigin()




    def showWorldMap(self,game):
        # plt.figure(1)
        # plt.subplot(111)
        # plt.axis([0, self.width_m, 0, self.height_m])
        # matplotlib.axes.Axes.invert_yaxis()
        # plt.title("World Map")
        # plt.grid()
        # # ax.set_aspect('equal')
        worldMap=np.full((self.width_px,self.height_px,3),(255,255,255),np.uint8)
        # Draw all cars as rectangles
        for sprite in game.all_sprites:
            worldMap=cv2.rectangle(worldMap,(sprite.spritex,sprite.spritey),(sprite.spritex+sprite.car_width,sprite.spritey+sprite.car_height),sprite.body_color,-1)


            # a=Rectangle((sprite.spritex,sprite.spritey),sprite.car_width,sprite.car_height, fc=sprite.body_color, angle=sprite.theta,alpha=.5)
            # ax.add_patch(a)
        worldMap=cv2.rectangle(worldMap,(self.window.x,self.window.y),(self.window.x+self.window.width_px,self.window.y+self.window.height_px),(0,0,0),3)
        # win_box=Rectangle(,self.window.width_m,self.window.height_m,fill=None, ec='black', lw=3, angle=0)
        # ax.add_patch(win_box)

        worldMap=cv2.resize(worldMap,(1000,400))
        cv2.imshow("World Map",worldMap)
        cv2.waitKey(0)

        # fullWorld.show()

        # viewWindow=plt.figure(2)
        # plt.title("Window View")
        # fig2, ax2 = plt.subplots(1)
        # ax2.set_xlim(0,self.window.width_m)
        # ax2.set_ylim(0,self.window.height_m)
        # ax2.invert_yaxis()
        # ax2.grid()
        # ax2.set_xlabel('meters')
        # ax2.set_ylabel('meters')

        # # ax2.set_aspect('equal')
        # viewWindow.show()


        # plt.show()
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

        self.pixpermeter=30 #pixels/meter

        # Set up canvas
        self.clock = pygame.time.Clock()
        self.run = True

        # Set up background
        # self.bg = pygame.image.load('assets/road.png')
        # self.bgX = 0
        # self.bgX2 = self.bg.get_width()

        self.all_sprites = pygame.sprite.Group()
        self.obst_list = pygame.sprite.Group()
        self.active_list=pygame.sprite.Group()



    


