import pygame


from classes import car
from window_class import Window, World, car_game




game=car_game()

# Generate world
world=World(game)


while game.run:
    game.clock.tick(100)
    
    # game.bgX -= game.road_speed  # Move both background images back
    # game.bgX2 -= game.road_speed

    # If there are no blue cars, make some more
    # print(len(obst_list))
    # if len(game.obst_list)<3:
    #     for i in range(0,random.randint(3,10)):
    #         game.obst_list=game.generateRandomObstacle()

    for obstacle in game.obst_list:
        # obstacle.spritex-=game.road_speed
        # obstacle.updateCarOrigin()
        if obstacle.spritex < obstacle.car_width_px * -1: # If our obstacle is off the screen we will remove it
            print(obstacle.spritex)
            obstacle.kill()
            # obst_list=game.generateRandomObstacle() # create a new obstacle to replace it

    for active_car in game.active_list:
        if active_car.spritex < active_car.car_width_px * -1: # If our obstacle is off the screen we will remove it
            game.active_list.pop(game.active_list.index(game.active_car))


    # if game.bgX < game.bg.get_width() * -1:  # If our bg is at the -width then reset its position
    #     game.bgX = game.bg.get_width()

    # if game.bgX2 < game.bg.get_width() * -1:  # If our bg is at the -width then reset its position
    #     game.bgX2 = game.bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False


    # Move the orange car based on arrow keys
    keys = pygame.key.get_pressed()
    world.moveWindow(keys,game)
    # game.orange_car.moveCar(keys,(game.canvas_width,game.canvas_height))
    


    

    world.window.redrawGameWindow(game,world.WorldSize_px) 
    
    
pygame.quit()