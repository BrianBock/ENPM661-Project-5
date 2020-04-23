import math
import numpy as np
# import sympy
import pygame
# pygame.init()

class car(pygame.sprite.Sprite):
    def __init__(self,x,y,car_type):
        pygame.sprite.Sprite.__init__(self)
        # super().__init__()
        self.x=x # start position
        self.y=y # start position
        self.car_width=130 # total width of car (for bounding box)
        self.car_height=70 # total height of car (for bounding box)


        # self.wheel_radius

        if car_type == "protagonist":
            self.car = pygame.image.load('assets/orange_car.png')
            self.stationary=False
            self.vel=12


        if car_type == "obstacle":
            # car does not move
            self.car = pygame.image.load('assets/blue_car.png')
            self.stationary=True

        if car_type == "dynamic":
            # car moves by itself
            self.car = pygame.image.load('assets/green_car.png')
            self.stationary=False
            self.vel=7

        self.car = pygame.transform.scale(self.car, (self.car_width, self.car_height))
        self.rect = self.car.get_rect()
        # self.rect.x = x
        # self.rect.y = y

        if not self.stationary:
            # Front wheel drive car utlizing Ackermann Steering
            # http://ckw.phys.ncku.edu.tw/public/pub/Notes/GeneralPhysics/Powerpoint/Extra/05/11_0_0_Steering_Theroy.pdf
            self.l=20 # length between front and rear wheel axes (wheelbase)
            self.a2=self.l/2 # distance from the back axel to the center of mass of the car


    def moveCar(self,keys,canvas_size):
        canvas_width,canvas_height=canvas_size
        
        if keys[pygame.K_LEFT] and self.x > self.vel: 
            self.x -= self.vel

        elif keys[pygame.K_RIGHT] and self.x < (canvas_width - self.vel - self.car_width):
            self.x += self.vel

        if keys[pygame.K_DOWN] and self.y <(canvas_height-self.vel-self.car_height):
            self.y+=self.vel

        elif keys[pygame.K_UP] and self.y > self.vel:
            self.y-=self.vel


    def turn(self,wheel_angle,direction,current_pos, current_vel, turn_time):
        # Simplifying assumption: the front wheels must remain parallel to each other.
        # There is therefore only one wheel angle and not two
        l=self.l
        a2=self.a2
        x,y,theta=current_pos # world coordinates

        forward_vel,angular_vel=current_vel # car velocity in car frame (+ angular_vel turning left)
        # angular velocity should be zero when we start to turn
        # car frame forward velocity remains constant while the car turns

        if direction == "left":
            turnRadius=math.sqrt(a2**2+l**2*sympy.cot(wheel_angle)**2)
            # wheel_angle=sympy.acot(math.sqrt(turnRadius**2-a2**2-l**2))
        elif direction == "right":
            # wheel_angle=-sympy.acot(math.sqrt(turnRadius**2-a2**2-l**2))
            turnRadius=-math.sqrt(a2**2+l**2*sympy.cot(wheel_angle)**2)

        arcTraveled=forward_vel*turn_time
        angleTraveled=np.rad2deg(arcTraveled/turnRadius) #s=0r

        new_theta=theta+angleTraveled
        new_x=-turnRadius*math.cos(np.deg2rad(new_theta))
        new_y=turnRadius*math.sin(np.deg2rad(new_theta))


        new_pos=(new_x,new_y,new_theta)
        return new_pos


        # new_pos_list=[]
        # for x,y in range(0,1000):
        #     a=(x-self.x)**2+(y-self.y)**2
        #     if math.isclose(a,turnRadius**2,rel_tol=1e-1):
        #         new_pos_list.append((x,y))


        #things to know about a node
        # Constants we know: l, a2, wheel speed, wheel radius
        # starting x, y, theta, vx, vy, wheel angle
        # after a dt, want to know new x,y,theta, vx,vy
        # need to find initial position of center of rotation (COR)
            # Find R
            # Use R, theta, x, y to find COR in world frame
            # Use R, a2 to find R1
        # Use R1, wheel speed, wheel radius to compute angular velocity around COR (Av)


    def turnCar(self,wheel_angle):
        R=math.sqrt(self.a2**2+self.l**2*sympy.cot(wheel_angle)**2)
        alpha=math.asin(self.a2/R)
        R1=R*math.cos(alpha)

        # Initial position of Center of Rotation in world frame (x,y)
        COR_i=(-R1*math.cos(np.deg2rad(self.theta))+self.x,-(R*math.sin(alpha))*math.sin(np.deg2rad(self.theta))+self.y)

        # Final position of Center of Rotation in world frame (x,y)
        COR_f=(COR_i[0]+self.vel*math.sin(np.deg2rad(self.theta))*self.dt,COR_i[1]+self.vel*math.cos(np.deg2rad(self.theta))*self.dt)

        ang_vel=self.wheel_radius*self.wheel_speed/(R1+self.W/2)
        dtheta=np.rad2deg(ang_vel*self.dt)

        B=(180-dtheta)/2-np.rad2deg(alpha)

        L=2*R*math.sin(np.deg2rad(dtheta)/2)
        # Change in position of car in car frame (x,y)
        d_c=(L*math.sin(np.deg2rad(B)), L*math.cos(np.deg2rad(B)))


        self.x=d_c[0]*math.cos(np.deg2rad(theta))+COR_f[0]
        self.y=d_c[1]*math.sin(np.deg2rad(theta))+COR_f[1]

        self.theta+=dtheta








