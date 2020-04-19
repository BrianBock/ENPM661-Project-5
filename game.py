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

# Create our car
orange_car=car(10,10,"protagonist")

# Create active cars
active_list=[]
for i in range (0,random.randint(1,3)):
    randx=random.randint(100,900)
    randy=random.randint(50,350)
    active_list.append(car(randx,randy,"dynamic"))

obst_list=[]

def generateRandomObstacle(obst_list):
        randx=random.randint(1100,2000)
        randy=random.randint(100,300)
        obst_list.append(car(randx,randy,"obstacle"))

        return obst_list



def redrawGameWindow():
    # Redraw background
    win.blit(bg, (int(bgX), 0))  # draws our first bg image
    win.blit(bg, (int(bgX2), 0))  # draws the seconf bg image

    # Redraw our car 
    win.blit(orange_car.car, (orange_car.x,orange_car.y))

    # Redraw other cars
    for obstacle in obst_list:
        win.blit(obstacle.car, (int(obstacle.x),int(obstacle.y)))

    for active_car in active_list:
        win.blit(active_car.car,(int(active_car.x),int(active_car.y)))

    pygame.display.update()
    

clock = pygame.time.Clock()
run = True

while run:
    clock.tick(100)
    road_speed=1.6
    bgX -= road_speed  # Move both background images back
    bgX2 -= road_speed

    if len(obst_list)==0:
        for i in range(0,random.randint(3,10)):
            obst_list=generateRandomObstacle(obst_list)

    for obstacle in obst_list:
        obstacle.x-=road_speed
        if obstacle.x < obstacle.car_width * -1: # If our obstacle is off the screen we will remove it
            obst_list.pop(obst_list.index(obstacle))
            obst_list=generateRandomObstacle(obst_list)

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