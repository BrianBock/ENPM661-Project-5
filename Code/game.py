# Import Python functions
import pygame
import pickle
from time import time

# Import our own functions
from classes import car
from window_class import Window, World, car_game
import statespace
import motionplanning
import logResults


manuallyAddCars=False
difficulty="Medium" #Medium, Hard, Extreme
photoMode=False

if manuallyAddCars == True:
    needCheck=True
    print("This is a building mode designed for picking the locations of the blue cars")
    while needCheck:
        check=input("This mode will overwrite any previously saved blue car positions. Are you sure you want to continue? Type 'Yes' or 'No': ")
        if check.lower()=="no" or check.lower()=='n':
            print("Exiting")
            needCheck=False
            exit()
        elif check.lower()=="yes" or check.lower()=='y':
            needCheck=False
            print("Use the arrow keys to move the window, and then select where you'd like the blue cars to go")
            print("A blue car will appear where you have clicked, and it's location will be saved for later use")
            print("When you are done, hit Q to save and exit. The next time you run, change 'manuallyAddCars' to False in game.py and 'userDefinedCars' to True in the World class")
        else:
            print("I didn't understand. Please try again.")

    bluecarlist=[]



print("Instantiating game")
# Instantiate game
game=car_game()

print("Generating world")
# Generate world
world=World(game,manuallyAddCars,difficulty,photoMode)

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












# Run the game
while game.run:
    game.clock.tick(100)

    # If there are no blue cars, make some more
    # print(len(obst_list))
    # if len(game.obst_list)<3:
    #     for i in range(0,random.randint(3,10)):
    #         game.obst_list=game.generateRandomObstacle()

    # for obstacle in game.obst_list:
    #     if obstacle.spritex < obstacle.car_width_px * -1: # If our obstacle is off the screen we will remove it
    #         print(obstacle.spritex)
    #         obstacle.kill()
            # obst_list=game.generateRandomObstacle() # create a new obstacle to replace it

    for active_car in game.active_list:
        active_car.spritex+=active_car.vel
        active_car.updateCarOrigin()
        # if active_car.spritex < active_car.car_width_px * -1: # If our obstacle is off the screen we will remove it
        #     game.active_list.pop(game.active_list.index(game.active_car))



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False


    # Move the orange car based on arrow keys
    keys = pygame.key.get_pressed()
    world.moveWindow(keys,game)
    # game.orange_car.moveCar(keys,(game.canvas_width,game.canvas_height))
    

    if manuallyAddCars:
    # Get cursor position for placing blue cars
        cursor=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        # print(click)
        if click[0]==1:
            window_pos=(world.window.x,world.window.y)
            cursor_pos=(cursor[0]+window_pos[0],cursor[1]+window_pos[1])
            # print(cursor_pos)
            new_obst=car(cursor_pos[0],cursor_pos[1],"obstacle")
            game.obst_list.add(new_obst)
            game.all_sprites.add(new_obst)
            bluecarlist.append(cursor_pos)
    
    world.window.redrawGameWindow(game,world.WorldSize_px,difficulty) 
        

    if keys[pygame.K_q]:
        pygame.quit()
        game.run=False

pygame.quit()

if manuallyAddCars:
    print("Saving data")

    # Purge duplicates from long clicks
    bluecarlist=list(dict.fromkeys(bluecarlist))
    # print(bluecarlist)
    with open('car_positions_'+difficulty+'.data','wb') as filehandle:
        pickle.dump(bluecarlist,filehandle)
        print("Data saved")
