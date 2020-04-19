import pygame
import random

from classes import car

pygame.init()

# Set up canvas
canvas_width=1000
canvas_height=400
win = pygame.display.set_mode((canvas_width, canvas_height))

# Set up background
bg = pygame.image.load('assets/road.png')
bgX = 0
bgX2 = bg.get_width()

all_sprites = pygame.sprite.Group()
obst_list = pygame.sprite.Group()
active_list=pygame.sprite.Group()

# Create our car
orange_car=car(10,10,"protagonist")
all_sprites.add(orange_car)

# Create active cars
for i in range (0,random.randint(1,3)):
    tempcar=car(0,0,"dynamic")
    randx=random.randint(100,900)
    randy=random.randint(50,350)
    # # Eliminate cars on the lane lines
    # if (100-tempcar.car_height<=randy<=100+tempcar.car_height) or (200-tempcar.car_height<=randy<=200+tempcar.car_height) or (300-tempcar.car_height<=randy<=300+tempcar.car_height):
    #     randy=random.randint(50,350)
    active_list.add(car(randx,randy,"dynamic"))
    all_sprites.add(car(randx,randy,"dynamic"))
tempcar.kill()
# obst_list=[]



def generateRandomObstacle(obst_list):
    # print("Attempting to spawn a new blue car")
    randx=random.randint(1000,2000)
    randy=random.randint(10,350)
    new_obst=car(randx,randy,"obstacle")
    # a=pygame.sprite.spritecollide(car(randx,randy,"obstacle"), obst_list, True)
    # print(a)
    obst_list.add(new_obst)
    all_sprites.add(new_obst)

    return obst_list



def redrawGameWindow():
    # Redraw background
    win.blit(bg, (int(bgX), 0))  # draws our first bg image
    win.blit(bg, (int(bgX2), 0))  # draws the seconf bg image

    # Redraw our car 
    # win.blit(orange_car.car, (orange_car.x,orange_car.y))

    # Redraw other cars
    for sprite in all_sprites:
        win.blit(sprite.car,(int(sprite.x),int(sprite.y)))
    # pygame.sprite.spritecollide(orange_car, obst_list, True)

    pygame.display.update()
    

clock = pygame.time.Clock()
run = True

while run:
    clock.tick(100)
    road_speed=1.6
    bgX -= road_speed  # Move both background images back
    bgX2 -= road_speed

    # If there are no blue cars, make some more
    # print(len(obst_list))
    if len(obst_list)<3:
        for i in range(0,random.randint(3,10)):
            obst_list=generateRandomObstacle(obst_list)

    for obstacle in obst_list:
        obstacle.x-=road_speed
        if obstacle.x < obstacle.car_width * -1: # If our obstacle is off the screen we will remove it
            obstacle.kill()
            obst_list=generateRandomObstacle(obst_list) # create a new obstacle to replace it

    for active_car in active_list:
        if active_car.x < active_car.car_width * -1: # If our obstacle is off the screen we will remove it
            active_list.pop(active_list.index(active_car))


    if bgX < bg.get_width() * -1:  # If our bg is at the -width then reset its position
        bgX = bg.get_width()

    if bgX2 < bg.get_width() * -1:  # If our bg is at the -width then reset its position
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and orange_car.x > orange_car.vel: 
        orange_car.x -= orange_car.vel

    elif keys[pygame.K_RIGHT] and orange_car.x < (canvas_width - orange_car.vel - orange_car.car_width):
        orange_car.x += orange_car.vel

    if keys[pygame.K_DOWN] and orange_car.y <(canvas_height-orange_car.vel-orange_car.car_height):
        orange_car.y+=orange_car.vel

    elif keys[pygame.K_UP] and orange_car.y > orange_car.vel:
        orange_car.y-=orange_car.vel

    

    redrawGameWindow() 
    
    
pygame.quit()