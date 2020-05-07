from collections import deque
import heapq
import numpy as np
from statespace import Tree, euclidean, manhattan

from matplotlib.backends.backend_agg import FigureCanvasAgg
import cv2 as cv

class SamplingPlanner:
    def __init__(self, stateSpace):
        self.stateSpace = stateSpace
        self._planCost = 0

    def RRT(self, maxTreeSize=1000, maxBranchSize=0.2, goalProbability=0.05):
        ''' Rapidly-exploring Random Tree '''
        solved = False

        start, goal = self.stateSpace.start, self.stateSpace.goal

        # Forward Search
        randomTree = Tree(start)
        for _ in range(maxTreeSize):            
            sample = self.stateSpace.sample(goalProbability)
            nearest, distance = randomTree.nearestNeighbor(sample)
            new = nearest.stoppingState(self.stateSpace, sample, maxBranchSize, distance) # new in direction of sample
            if new is None:
                continue
            if self._localPlanner(nearest, new) is not None: 
                randomTree.addEdge(nearest, new)
                if new.cost2go(goal, heuristic=euclidean) <= self.stateSpace.goalRadius:
                    solved = True
                    break 

        exploredNodes = randomTree.nodes # for the visualization of path finding
        
        # Backtrack
        if solved == False:
            new, _ = randomTree.nearestNeighbor(goal)
        plan = _generatePlan(new)
        self._measureCost(plan)
    
        return (solved, plan, exploredNodes, self._planCost)

    @staticmethod
    def _localPlanner(nearestNode, newNode):
        # trajectory (straight-line) planner

        return True

    def _measureCost(self, plan):
        for i in range(1, len(plan)):
            self._planCost += plan[i-1].cost2go(plan[i])

    def simulation(self, plan, exploredNodes, plannerType='Sampling', step=1000):
        visualizePathFinding(self.stateSpace, plan, exploredNodes, plannerType, step)

class GridPlanner:
    def __init__(self, stateSpace, positionResolution=0.05, angleResolution=45):
        # grid parameters
        self.stateSpace = stateSpace
        self.positionResolution = positionResolution # in ]0,1]
        self.angleResolution = np.deg2rad(angleResolution)
        self.sizeX = int(stateSpace.width / self.positionResolution)
        self.sizeY = int(stateSpace.height / self.positionResolution)
        self.sizeTheta = int(2*np.pi / self.angleResolution)
        self.gridSize = self.sizeX*self.sizeY*self.sizeTheta

    def Astar(self):
        ''' Fast Optimal Search '''
        solved, exploredNodes = False, []
        visited = np.zeros((self.gridSize,), dtype=bool)
        cost = np.full((self.gridSize,), np.inf, dtype=np.float64)

        start, goal = self.stateSpace.start, self.stateSpace.goal

        # Forward Search
        cost[start.discretize(self)] = 0
        unvisited = [(cost[start.discretize(self)], start)] # minimum-based priority queue (pq)

        while unvisited:
            minCost, current = heapq.heappop(unvisited) # pq.remove()
            cost2come, cost2go = cost[current.discretize(self)], current.cost2go(goal, heuristic=euclidean)

            if cost2go <= self.stateSpace.goalRadius:
                solved = True
                break

            visited[current.discretize(self)] = True

            if minCost <= cost2come + cost2go: # to avoid processing node duplicates in pq
                exploredNodes.append(current) # for the visualization of path finding
                for neighbor in current.neighbors(self.stateSpace):
                    node, edgeCost = neighbor[0], neighbor[1]
                    newcost2come = cost2come + edgeCost
                    if not visited[node.discretize(self)]:
                        if newcost2come < cost[node.discretize(self)]:
                            node.parent = current
                            cost[node.discretize(self)] = newcost2come
                            newcost2come += node.cost2go(goal, heuristic=euclidean)
                            heapq.heappush(unvisited, (newcost2come, node)) # pq.insert() / pq.updatePriority()
        
        # Backtrack
        planCost = cost[current.discretize(self)]
        plan = _generatePlan(current)
        
        return (solved, plan, exploredNodes, planCost)

    def Dijkstra(self):
        ''' Optimal Search '''
        solved, exploredNodes = False, []
        visited = np.zeros((self.gridSize,), dtype=bool)
        cost = np.full((self.gridSize,), np.inf, dtype=np.float64)

        start, goal = self.stateSpace.start, self.stateSpace.goal

        # Forward Search
        cost[start.discretize(self)] = 0
        unvisited = [(cost[start.discretize(self)], start)] # minimum-based priority queue (pq)

        while unvisited:
            minCost, current = heapq.heappop(unvisited) # pq.remove()
            cost2come, cost2go = cost[current.discretize(self)], current.cost2go(goal, heuristic=euclidean)

            if cost2go <= self.stateSpace.goalRadius:
                solved = True
                break

            visited[current.discretize(self)] = True

            if minCost <= cost2come: # to avoid processing node duplicates in pq
                exploredNodes.append(current) # for the visualization of path finding
                for neighbor in current.neighbors(self.stateSpace):
                    node, edgeCost = neighbor[0], neighbor[1]
                    newcost2come = cost2come + edgeCost
                    if not visited[node.discretize(self)]:
                        if newcost2come < cost[node.discretize(self)]:
                            node.parent = current
                            cost[node.discretize(self)] = newcost2come
                            heapq.heappush(unvisited, (newcost2come, node)) # pq.insert() / pq.updatePriority()
        
        # Backtrack
        planCost = cost[current.discretize(self)]
        plan = _generatePlan(current)
        
        return (solved, plan, exploredNodes, planCost)

    def BFS(self):
        ''' Brute-force Search (Breadth-first Search) '''
        solved, exploredNodes = False, []
        visited = np.zeros((self.gridSize,), dtype=bool)

        start, goal = self.stateSpace.start, self.stateSpace.goal

        # Forward Search
        unvisited = deque([start]) # queue
        visited[start.discretize(self)] = True

        while unvisited:
            current = unvisited.pop() # queue.dequeue()

            if current.cost2go(goal, heuristic=euclidean) <= self.stateSpace.goalRadius:
                solved = True
                break

            exploredNodes.append(current) # for the visualization of path finding

            for neighbor in current.neighbors(self.stateSpace):
                node = neighbor[0]
                if not visited[node.discretize(self)]:
                    node.parent = current
                    unvisited.appendleft(node) # queue.enqueue()
                    visited[node.discretize(self)] = True
        
        # Backtrack
        plan = _generatePlan(current)
        planCost = len(plan) - 1 # number of edges; since BFS doesn't take edge cost into account

        return (solved, plan, exploredNodes, planCost)

    def DFS(self):
        ''' Brute-force Search (Depth-first Search) '''
        solved, exploredNodes = False, []
        visited = np.zeros((self.gridSize,), dtype=bool)

        start, goal = self.stateSpace.start, self.stateSpace.goal

        # Forward Search
        unvisited = deque([start]) # stack

        while unvisited:
            current = unvisited.pop() # stack.pop()

            if current.cost2go(goal, heuristic=euclidean) <= self.stateSpace.goalRadius:
                solved = True
                break

            visited[current.discretize(self)] = True
            exploredNodes.append(current) # for the visualization of path finding

            for neighbor in current.neighbors(self.stateSpace):
                node = neighbor[0]
                if not visited[node.discretize(self)]:
                    node.parent = current
                    unvisited.append(node) # stack.push()

        # Backtrack
        plan = _generatePlan(current)
        planCost = len(plan) - 1 # number of edges; since DFS doesn't take edge cost into account

        return (solved, plan, exploredNodes, planCost)

    def simulation(self, plan, exploredNodes, plannerType='Grid', step=1000):
        visualizePathFinding(self.stateSpace, plan, exploredNodes, plannerType, step)

def _generatePlan(currentNode):
    plan = deque() # queue
    while (currentNode.parent is not None):
        plan.appendleft(currentNode)
        currentNode = currentNode.parent
    plan.appendleft(currentNode)

    return plan

def visualizePathFinding(stateSpace, plan, exploredNodes, plannerType, step):
    robotSize_simulation = 0.15
    robot_start = (*stateSpace.cart2sim(stateSpace.start.state[:2]), robotSize_simulation)
    robot_goal = (*stateSpace.cart2sim(stateSpace.goal.state[:2]), robotSize_simulation)
    Map = stateSpace.create()
    canvas = FigureCanvasAgg(Map)
    width, height = canvas.get_width_height()
    outputVideo = cv.VideoWriter('Simulation.mp4', cv.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    # draw explored space
    size = len(exploredNodes) - 1
    for i in range(1, size, step):
        if size - i + 1 < step:
            step = size - i + 1
        for j in range(step):
            if plannerType == 'Grid':
                x, y = stateSpace.cart2sim(exploredNodes[i+j].state[:2])
                stateSpace.scatter(x, y)
            elif plannerType == 'Sampling':
                branch = [exploredNodes[i+j].parent.state[:2], exploredNodes[i+j].state[:2]]
                branch = list(map(stateSpace.cart2sim, branch))
                stateSpace.drawSegment(branch)
            
        stateSpace.drawCircle(robot_start, 'red')
        stateSpace.drawCircle(robot_goal, 'red')

        frame = _renderFrame(canvas, width, height)
        outputVideo.write(frame)
        cv.imshow('Simulation', frame)
        if cv.waitKey(1) >= 0:
            break

    # draw path
    robot = stateSpace.drawCircle(robot_start, 'yellow')
    for i in range(1, len(plan)):
        robot.remove()
        consecutiveStates = (plan[i-1].state[:2], plan[i].state[:2])
        previousState, currentState = tuple(map(stateSpace.cart2sim, consecutiveStates))
        stateSpace.drawArrow(previousState, currentState, 'black')
        robot = stateSpace.drawCircle((*currentState, robotSize_simulation), 'yellow')

        frame = _renderFrame(canvas, width, height)
        outputVideo.write(frame)
        cv.imshow('Simulation', frame)
        if cv.waitKey(1) >= 0:
            break

    cv.waitKey(0)

def _renderFrame(canvas, width, height):
    canvas.draw()
    frame = np.frombuffer(canvas.tostring_rgb(), dtype=np.uint8).reshape((height, width, 3))

    return cv.cvtColor(frame, cv.COLOR_RGB2BGR)