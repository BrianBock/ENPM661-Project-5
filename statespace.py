import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon
import random

euclidean = lambda vector1, vector2: np.linalg.norm(np.array(vector1) - np.array(vector2))
manhattan = lambda vector1, vector2: np.sum(np.absolute(np.array(vector1) - np.array(vector2)))

class RoadMap:
    def __init__(self,game,world):
        # discretized space parameters
        self.width = world.width_px
        self.height = world.height_px
        self.goalRadius = 15#0.2
        # robot parameters
        self.robotRadius = game.orange_car.car_width_px//2
        self.wheelRadius, self.wheelsSeparation = 0.066, 0.16 # differential
        self.stepSize = 0.5 # unconstrained
        ## trajectory parameters
        self.uniformMotionDuration, self.no_interpolations = 3, 10
        self.timeStep = self.uniformMotionDuration / self.no_interpolations # dt

        # self.RPMs, start, goal = self.userInput()
        ## test cases
        self.offset, self.RPMs = self.robotRadius + 0.1, (1,2) # 3D
        # self.offset, self.RPMs, start, goal = self.robotRadius + 0.1, (1,2), self.sim2cart((-4,-4)), self.sim2cart((4,4)) # 2D

        start=(world.window.width_px/2+game.orange_car.car_width_px/2,world.height_px/2,0)
        goal=(world.width_px-1.5*world.window.finish.get_width(), world.height_px/2)

        self.start, self.goal = Node(start), Node(goal)
        # obstacles' parameters
    #     self.defineObstacles()


    # def defineObstacles(self):
    #     # circle = (xc,yc,r)
    #     self.c1 = {'cart': (5,5,1), 'sim': (0,0,1)}
    #     self.c2 = {'cart': (7,8,1), 'sim': (2,3,1)}
    #     self.c3 = {'cart': (3,2,1), 'sim': (-2,-3,1)}
    #     self.c4 = {'cart': (7,2,1), 'sim': (2,-3,1)}
    #     # square = (x_L,x_U,y_L,y_U)
    #     self.s1 = {'cart': (8.25,9.75,4.25,5.75), 'sim': (3.25,4.75,-0.75,0.75)}
    #     self.s2 = {'cart': (0.25,1.75,4.25,5.75), 'sim': (-4.75,-3.25,-0.75,0.75)}
    #     self.s3 = {'cart': (2.25,3.75,7.25,8.75), 'sim': (-2.75,-1.25,2.25,3.75)}

    def create(self,game):
        figure = plt.figure()
        self.ax = plt.axes(xlim=(-self.width/2,self.width/2), ylim=(-self.height/2,self.height/2))
        self.ax.set_aspect('equal')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Map')
        # plt.grid()

        for obstacle in game.obst_list:
            x_L = obstacle.spritex
            x_U = x_L+obstacle.car_width_px
            y_L = obstacle.spritey
            y_U = y_L+obstacle.car_height_px
            self.drawPolygon((x_L,x_U,y_L,y_U))

        return figure

    def collisionAvoidance(self, state, game):
        p = state[:2]
        in_obst=[]
        for obstacle in game.obst_list:
            in_obst.append(self.inRectangle(p,obstacle))
            if any(in_obst):
                return False
            else:
                return True

    def sim2cart(self, point):

        return (point[0]+self.width/2, point[1]+self.height/2)

    def cart2sim(self, point):
        
        return (point[0]-self.width/2, point[1]-self.height/2)

    # def img2cart(self,point):

    #     return (point[0],point[1])

    def sample(self, goalProbability):
        # if random.randint(0,100) > goalProbability*100:
        if random.random() > goalProbability:
            return Node((random.uniform(0, self.width), random.uniform(0, self.height)))
        else:
            return self.goal

    def contain(self, state):

        return 0 <= state[0] <= self.width and 0 <= state[1] <= self.height

    def inWalls(self, point):
        x, y = point[0], point[1]
        offset = self.offset

        return self.height-offset <= y or y <= offset or self.width-offset <= x or x <= offset

    @staticmethod
    def drawSegment(segment):
        X = list(map(lambda p: p[0], segment))
        Y = list(map(lambda p: p[1], segment))
        plt.plot(X, Y, '-o', color='cyan', linewidth=0.5, markersize=1, zorder=0)

    @staticmethod
    def scatter(X, Y):
        plt.plot(X, Y, 'o', color='cyan', linewidth=0.5, markersize=0.5, zorder=0)

    ############################################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # def inCircle(self, point, parameters):
    #     x, y = point[0], point[1]
    #     # circle Parametrs
    #     xc, yc, r = parameters

    #     return (x-xc)**2 + (y-yc)**2 <= (r+self.offset)**2

    def drawCircle(self, parameters, color='blue'):
        xc, yc, r = parameters

        circle = Circle((xc,yc), r, linewidth=0.5, color=color)
        self.ax.add_artist(circle)

        return circle

    def inRectangle(self, point, obstacle):
        # Robot's current position
        x, y = point[0], point[1]
        
        # rectangle parameters
        x_L = obstacle.spritex-self.offset
        x_U = x_L+obstacle.car_width_px+self.offset
        y_L = obstacle.spritey-self.offset
        y_U = y_L+obstacle.car_height_px+self.offset

        return x_L <= x <= x_U and y_L <= y <= y_U

    def drawPolygon(self, parameters):
        if isinstance(parameters, tuple):
            x_L, x_U, y_L, y_U = parameters
            vertices = [(x_L,y_L), (x_U,y_L), (x_U,y_U), (x_L,y_U)]
        else:
            vertices = parameters       

        polygon = Polygon(vertices, linewidth=0.5, color='blue')
        self.ax.add_artist(polygon)

    def drawArrow(self, start, end, color='black'):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        # arrow = plt.quiver(start[0], start[1], end[0], end[1], color=color, units = 'xy', scale = 5)
        arrow = plt.arrow(start[0], start[1], dx, dy, color=color, length_includes_head=True, head_width=0.1, head_length=0.15)
        self.ax.add_artist(arrow)

        return arrow

class Tree:
    def __init__(self, rootNode):
        self.nodes = [rootNode] # robot states 

    def addEdge(self, existingNode, newNode):
        newNode.parent = existingNode
        self.nodes.append(newNode)

    def nearestNeighbor(self, randomState):
        minDistance = np.inf
        for state in self.nodes:
            distance = state.cost2go(randomState)
            if distance < minDistance:
                minDistance = distance
                nearestNode = state

        return nearestNode

class Node:
    def __init__(self, state, action=None, parent=None):
        self.state = state # the pose (position + orientation) of the point robot stored as (x, y, theta)
        self.action = action # the action performed on the parent to produce this state
        self.parent = parent # previous node
        self.trajectory = [] # interpolated states from parent to child

        # # Differential Robot
    # def neighbors(self, Map):    
    #     adj = []
    #     x, y, theta = self.state[0], self.state[1], self.state[2]  
    #     slow, fast, r, L, dt = *Map.RPMs, Map.wheelRadius, Map.wheelsSeparation, Map.timeStep

    #     # 8-connected action set
    #     actions = [
    #         (fast,fast),
    #         (fast,slow),
    #         (fast,0),
    #         (slow,fast),
    #         (slow,slow),
    #         (slow,0),
    #         (0,fast),
    #         (0,slow),
    #     ]

    #     for action in actions:
    #         ul, ur = action
    #         x_next, y_next, theta_next = x, y, theta
    #         for _ in range(Map.no_interpolations):
    #             x_next += 0.5*r*(ur+ul)*np.cos(theta_next)*dt    
    #             y_next += 0.5*r*(ur+ul)*np.sin(theta_next)*dt
    #             theta_next += r/L*(ur-ul)*dt
    #             if theta_next <= -np.pi:
    #                 theta_next += 2*np.pi
    #             if theta_next > np.pi:
    #                 theta_next -= 2*np.pi   
    #         edgeCost = np.sqrt((x_next-x)**2+(y_next-y)**2)    
    #         adj.append(((x_next, y_next, theta_next), action, edgeCost))     

    #     return [(Node(neighbor[0], neighbor[1]), neighbor[2]) for neighbor in adj if Map.contain(neighbor[0]) and Map.collisionAvoidance(neighbor[0])] 


    def neighbors(self, Map):    
        adj = []
        x, y, theta = self.state[0], self.state[1], self.state[2]      

        # action set = {direction of movement defined as an angle}
        no_actions=8
        d = Map.stepSize
        actions = np.linspace(np.deg2rad(-180), np.deg2rad(180), no_actions, endpoint=True) 
        for action in actions:
            angle = theta + action # in radians
            if angle <= -np.pi:
                angle += 2*np.pi
            if angle > np.pi:
                angle -= 2*np.pi
            adj.append(((x + d*np.cos(angle), y + d*np.sin(angle), angle), action))

        return [(Node(neighbor[0], neighbor[1]), Map.stepSize) for neighbor in adj if Map.contain(neighbor[0]) and Map.collisionAvoidance(neighbor[0])]

    def cost2go(self, other, heuristic=euclidean):

        return heuristic(self.state[:2], other.state[:2])

    def discretize(self, grid):
        xIndex = self.index(self.state[0], grid.positionResolution)
        yIndex = self.index(self.state[1], grid.positionResolution)
        thetaIndex = int(self.state[2]/grid.angleResolution)

        return xIndex + grid.sizeX*(yIndex + thetaIndex*grid.sizeY)

    @staticmethod
    def index(num, threshold):
        # amplification is needed because of floating point roundoff errors
        amplification = 1e6 # higher amplification allows lower thresholds
        num_int = num // 1
        num_dec = (num % 1)
        quotient = num_dec // threshold 

        num_dec *= amplification
        threshold *= amplification
        remainder = num_dec % threshold

        if quotient:
            if remainder >= threshold/2:
                i = num_int + (quotient*threshold + threshold)/amplification
            else:
                i = num_int + quotient*threshold/amplification
        else:
            if remainder >= threshold/2: 
                i = num_int + threshold/amplification
            else:
                i = num_int

        return int(i/threshold*amplification)

    def stoppingState(self, stateSpace, other, maxBranchSize,game):
        if self == other:
            newNode = None
        elif self.cost2go(other) <= maxBranchSize and stateSpace.collisionAvoidance(other.state,game):
            newNode = other
        else:
            p1, p2 = self.state, other.state
            slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
            dx = maxBranchSize / np.sqrt(1 + slope**2)
            dy = slope * dx
            newNode = Node((p1[0] + dx, p1[1] + dy))
            if not stateSpace.collisionAvoidance(newNode.state,game):
                newNode = None

        return newNode
                
    def __eq__(self, other):

        return self.state == other.state

    def __lt__(self, other): 
        # overloading this operator is required to make "heapq" work 
        return self.state < other.state