import pygame
import random

from classes import car

class car_game():
    def __init__(self):
        pygame.init()

        self.road_speed=1.6

        # Set up canvas
        self.canvas_width=1000
        self.canvas_height=400
        self.win = pygame.display.set_mode((self.canvas_width, self.canvas_height))

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
        self.orange_car=car(10,10,"protagonist")
        self.all_sprites.add(self.orange_car)

        # Create stationary cars
        self.generateBlueCars()

        # Create active cars
        for i in range (0,random.randint(1,3)):
            tempcar=car(0,0,"dynamic")
            randx=random.randint(100,900)
            randy=random.randint(50,350)
            # # Eliminate cars on the lane lines
            # if (100-tempcar.car_height<=randy<=100+tempcar.car_height) or (200-tempcar.car_height<=randy<=200+tempcar.car_height) or (300-tempcar.car_height<=randy<=300+tempcar.car_height):
            #     randy=random.randint(50,350)
            self.active_list.add(car(randx,randy,"dynamic"))
            self.all_sprites.add(car(randx,randy,"dynamic"))
        tempcar.kill()
        # obst_list=[]



    def generateRandomObstacle(self):
        # print("Attempting to spawn a new blue car")
        randx=random.randint(1000,2000)
        randy=random.randint(10,350)
        new_obst=car(randx,randy,"obstacle")
        # a=pygame.sprite.spritecollide(car(randx,randy,"obstacle"), obst_list, True)
        # print(a)
        self.obst_list.add(new_obst)
        self.all_sprites.add(new_obst)

        # return self.obst_list



    def generateBlueCars(self):

        start_pos_list=[(130,220),(200,330),(500,10)]

        for start_pos in start_pos_list:
            x,y=start_pos
            new_obst=car(x,y,"obstacle")
            self.obst_list.add(new_obst)
            self.all_sprites.add(new_obst)






    def redrawGameWindow(self):
        # Redraw background
        self.win.blit(self.bg, (int(self.bgX), 0))  # draws our first bg image
        self.win.blit(self.bg, (int(self.bgX2), 0))  # draws the seconf bg image

        # Redraw all cars
        for sprite in self.all_sprites:
            self.win.blit(sprite.car_image_new,(int(sprite.spritex),int(sprite.spritey)))

        pygame.display.update()
    




game=car_game()


while game.run:
    game.clock.tick(100)
    
    game.bgX -= game.road_speed  # Move both background images back
    game.bgX2 -= game.road_speed

    # If there are no blue cars, make some more
    # print(len(obst_list))
    # if len(game.obst_list)<3:
    #     for i in range(0,random.randint(3,10)):
    #         game.obst_list=game.generateRandomObstacle()

    for obstacle in game.obst_list:
        obstacle.spritex-=game.road_speed
        # obstacle.updateCarOrigin()
        if obstacle.spritex < obstacle.car_width_px * -1: # If our obstacle is off the screen we will remove it
            print(obstacle.spritex)
            obstacle.kill()
            # obst_list=game.generateRandomObstacle() # create a new obstacle to replace it

    for active_car in game.active_list:
        if active_car.spritex < active_car.car_width_px * -1: # If our obstacle is off the screen we will remove it
            game.active_list.pop(game.active_list.index(game.active_car))


    if game.bgX < game.bg.get_width() * -1:  # If our bg is at the -width then reset its position
        game.bgX = game.bg.get_width()

    if game.bgX2 < game.bg.get_width() * -1:  # If our bg is at the -width then reset its position
        game.bgX2 = game.bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False


    # Move the orange car based on arrow keys
    keys = pygame.key.get_pressed()
    game.orange_car.moveCar(keys,(game.canvas_width,game.canvas_height))
    


    

    game.redrawGameWindow() 
    
    
pygame.quit()