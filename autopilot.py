import statespace
import motionplanning
import numpy as np
from time import time

def main():
    Map = statespace.RoadMap()
    planner = motionplanning.SamplingPlanner(Map)
    t0 = time()
    solved, plan, exploredNodes, _ = planner.RRT(maxTreeSize=1000, maxBranchSize=1)
    t1 = time() 
    if solved: 
        print(f'Path is found in {t1-t0} s\n')
    else:
        print('Path not found')
    planner.simulation(plan, exploredNodes)

    # # test cases
    # plan = [(1, 2.3), (2, 3), (3, 5), (4, 5.1), (5, 5.4), (6, 4.5), (7, 4.8), (8, 3),
    #         (9, 2.3), (10, 3.4), (11, 1), (12, 0.7), (13, 0.9), (14, 1.9), (15, 1.1), (16, 3)]

    # actions = planner.actionPlanner(plan)
    # print(actions)


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