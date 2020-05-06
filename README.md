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


## TODO
Fix nearest neighbor function where it sometimes doesn't pick the closest node.




## Sources and Additional Reading
http://ckw.phys.ncku.edu.tw/public/pub/Notes/GeneralPhysics/Powerpoint/Extra/05/11_0_0_Steering_Theroy.pdf

## Graphic Sources

Car graphics from: http://clipart-library.com/overhead-car-cliparts.html

Grass from https://www.moddb.com/groups/indie-devs/tutorials/how-to-make-a-simple-grass-texture-in-gimp