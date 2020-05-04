import statespace
import motionplanning
import numpy as np
from time import time

def main():
    Map = statespace.RoadMap()
    planner = motionplanning.SamplingPlanner(Map)
    t0 = time()
    solved, plan, exploredNodes, _ = planner.RRT()
    t1 = time() 
    if solved: 
        print(f'Path is found in {t1-t0} s\n')
    else:
        print('Path not found')
    motionplanning.Simulation(Map, plan, exploredNodes)
    # logResults(plan, Map)    

def logResults(plan, Map):
    with open('plan.txt', 'w') as file:
        file.write('State\t\t\tAction\n')
        for node in plan:
            position = Map.cart2sim(node.state[:2])
            file.write(f'({position[0]:.3f}, {position[1]:.3f}, {np.rad2deg(node.state[2]):.1f})\t')
            if node.action is not None:
                file.write(f'({node.action[0]}, {node.action[1]})\n')
            else:
                file.write('(0, 0)\n')

if __name__ == '__main__':
    main()