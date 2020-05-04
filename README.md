# Car Planner        			             
This project implements RRT trajectory planning for a car (non-holonomic robot) with steering as the only control input.  
A*, Dijkstra, BFS and DFS search algorithms are also supported.

## Setup
1. Run the following command in the terminal: python autopilot.py

## Demo 
The simulation was run using the following user inputs:  
Robot Clearance: 0.1   
Start State: -4 -4 90  
Goal State: 4 4 0
   
## Dependencies
numpy, cv2, matplotlib, collections, heapq, time