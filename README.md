# ENPM661 Project 5 (Self-driving Car)      			             
This project implements RRT trajectory planning for a car (non-holonomic robot) with steering as the only control input.  
A\*, Dijkstra, BFS and DFS search algorithms are also supported.

## How to Run
Clone this entire repository. Make sure the directory you clone it to is one you have write access to, as several files are created while the program runs. Open Terminal and navigate to the Code directory. Type `python game.py`. If you have additional versions of Python installed, you may need to type `python3 game.py` instead. 

The program will solve a path from the start to goal. A matplotlib based visualization will appear, showing you the obstacles as blue blocks and the explored nodes in light blue. When that concludes, the Pygame visualization will launch, showing you the car driving from start to finish. 

## Dependencies
    numpy
    cv2
    pickle
    pygame
    random
    matplotlib
    collections
    heapq
    time
    Python 3.8


## Difficulty Modes
The program has several difficulty modes, which can be selected by changing the value of `gameMode` in `game.py`. 



### Easy
Easy mode features a very short road and few obstacles. 

![Easy Mode](https://github.com/BrianBock/ENPM661-Project-5/blob/master/Report/Easy1.png)



### Medium

![Medium Mode](https://github.com/BrianBock/ENPM661-Project-5/blob/master/Report/Medium1.png)



### Hard

![Hard Mode](https://github.com/BrianBock/ENPM661-Project-5/blob/master/Report/Hard1.png)


### Random

The other modes have the blue cars in carefully handpicked locations, placed for the right combination of difficulty and feasibility. They were all designed to be solvable, with at least one valid path. There is also a random mode, which generates a random number of blue cars in random locations on a road of random length. There is no check for or guarantee that the produced world will be solvable, but you're welcome to try it anyway. Change `gameMode` in `game.py` to "Random". 


## View Modes

### Chaser View
This mode fixes the camera frame to the orange car, and moves with it. The planner has access to the entire course, but the pygame visualizer only shows a portion of it at a time. This allows you to see the action up close and with more detail. This mode is the default. 

### Sky View (PENDING)
This mode fixes the camera frame to the entire track, and it does not move. This allows you to see the entire track at once, but it may be more difficult to see the finer details, especially on the longer courses. 

### Photo Mode
The program has an optional Photo Mode (accessible via a boolean toogle - `photoMode` in `game.py`) that takes a photo of the entire track at the start. This mode was used to create the track images for each of the difficulty modes above. Due to the way photoMode changes the viewing window and other crucial game elements, it is incompatiable with actual game function. 


## TODO
Fix nearest neighbor function where it sometimes doesn't pick the closest node.




## Sources and Additional Reading
http://ckw.phys.ncku.edu.tw/public/pub/Notes/GeneralPhysics/Powerpoint/Extra/05/11_0_0_Steering_Theroy.pdf

## Graphic Sources

Car graphics from: http://clipart-library.com/overhead-car-cliparts.html

Grass from https://www.moddb.com/groups/indie-devs/tutorials/how-to-make-a-simple-grass-texture-in-gimp