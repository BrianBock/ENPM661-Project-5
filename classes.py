# Import Python functions
import math
import numpy as np
import pygame
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch

# Import our own functions
from trigfunctions import*

class car(pygame.sprite.Sprite):
    def __init__(self,x,y,car_type):
        pygame.sprite.Sprite.__init__(self)
        # super().__init__()

        # Start position of car origin
        self.x=x # start position
        self.y=y # start position
        self.theta=0

        # Car sprite dimensions
        self.car_width_px=130 # total width of car (for bounding box)
        self.car_height_px=70 # total height of car (for bounding box)

        # Physical car dimensions (meters)
        self.car_width = 5
        self.car_height = 2
        self.wheel_radius = .46
        self.wheel_speed = 85 # rad/s

        self.dt=.1 # seconds

        # Start position of the sprite origin
        self.updateSpriteOrigin()


        if car_type == "protagonist":
            self.car = pygame.image.load('assets/orange_car.png')
            self.stationary=False
            self.vel=12 #m/s


        if car_type == "obstacle":
            # car does not move
            self.car = pygame.image.load('assets/blue_car.png')
            self.stationary=True

        if car_type == "dynamic":
            # car moves by itself
            self.car = pygame.image.load('assets/green_car.png')
            self.stationary=False
            self.vel=7

        self.car = pygame.transform.scale(self.car, (self.car_width_px, self.car_height_px))
        self.rect = self.car.get_rect()
        # self.rect.x = x
        # self.rect.y = y

        if not self.stationary:
            # Front wheel drive car utlizing Ackermann Steering
            # http://ckw.phys.ncku.edu.tw/public/pub/Notes/GeneralPhysics/Powerpoint/Extra/05/11_0_0_Steering_Theroy.pdf
            self.l=100 # length between front and rear wheel axes (wheelbase)
            self.a2=self.l/2 # distance from the back axel to the center of mass of the car
            self.W=self.car_height # distance between the left and right wheels

            # Load all of the rotated car images into the game
            # self.angled_car_list=[]
            # for i in range (360):
            #     rotcar = pygame.image.load('assets/orange_car/orange_car_'+str(i)+'.png')
            #     rotcar = pygame.Surface.convert_alpha(rotcar)
            #     rotcar = pygame.transform.scale(rotcar, (self.car_width_px, self.car_height_px))
            #     self.angled_car_list.append(rotcar)

    def updateSpriteOrigin(self):
        self.spritex=self.x-self.car_width//2
        self.spritey=self.y-self.car_width//2

    def updateCarOrigin(self):
        self.x=self.spritex+self.car_width//2
        self.y=self.spritey+self.car_height//2


    def rot_center(self,angle):
        """rotate an image while keeping its center"""
        # http://www.pygame.org/wiki/RotateCenter?parent=CookBook
        rot_image = pygame.transform.rotate(self.car, angle)
        rot_rect = rot_image.get_rect(center=self.rect.center)
        return rot_image,rot_rect


    def moveCar(self,keys,canvas_size):
        canvas_width,canvas_height=canvas_size
        
        if keys[pygame.K_LEFT] and self.spritex > self.vel: 
            self.spritex -= self.vel

        elif keys[pygame.K_RIGHT] and self.spritex < (canvas_width - self.vel - self.car_width):
            self.spritex += self.vel

        if keys[pygame.K_DOWN] and self.spritey <(canvas_height-self.vel-self.car_height):
            self.spritey+=self.vel

        elif keys[pygame.K_UP] and self.spritey > self.vel:
            self.spritey-=self.vel


        elif keys[pygame.K_a]:
            self.turnCar(2)
        elif keys[pygame.K_s]:
            self.turnCar(-2)

        self.updateCarOrigin()
        

    # def turn(self,wheel_angle,direction,current_pos, current_vel, turn_time):
    #     # Simplifying assumption: the front wheels must remain parallel to each other.
    #     # There is therefore only one wheel angle and not two
    #     l=self.l
    #     a2=self.a2
    #     x,y,theta=current_pos # world coordinates

    #     forward_vel,angular_vel=current_vel # car velocity in car frame (+ angular_vel turning left)
    #     # angular velocity should be zero when we start to turn
    #     # car frame forward velocity remains constant while the car turns

    #     if direction == "left":
    #         turnRadius=math.sqrt(a2**2+l**2*cotd(wheel_angle)**2)
    #         # wheel_angle=sympy.acot(math.sqrt(turnRadius**2-a2**2-l**2))
    #     elif direction == "right":
    #         # wheel_angle=-sympy.acot(math.sqrt(turnRadius**2-a2**2-l**2))
    #         turnRadius=-math.sqrt(a2**2+l**2*cotd(wheel_angle)**2)

    #     arcTraveled=forward_vel*turn_time
    #     angleTraveled=np.rad2deg(arcTraveled/turnRadius) #s=0r

    #     new_theta=theta+angleTraveled
    #     new_x=-turnRadius*cosd(new_theta)
    #     new_y=turnRadius*sind(new_theta)


    #     new_pos=(new_x,new_y,new_theta)
    #     return new_pos


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
        R=math.sqrt(self.a2**2+self.l**2*cotd(wheel_angle)**2)
        # if wheel_angle<0:
        #     R*=-1
        print("R="+str(R))
        alpha=math.asin(self.a2/R)
        print("alpha="+str(alpha))
        R1=R*math.cos(alpha)

        # # Initial position of Center of Rotation in world frame (x,y)
        # COR_i=(-R1*cosd(self.theta)+self.x,-(R*math.sin(alpha))*sind(self.theta)+self.y)
        # print("COR_i="+str(COR_i))

        # # Final position of Center of Rotation in world frame (x,y)
        # COR_f=(COR_i[0]+self.vel*sind(self.theta)*self.dt,COR_i[1]+self.vel*cosd(self.theta)*self.dt)
        # print("COR_f="+str(COR_f))

        ang_vel=self.wheel_radius*self.wheel_speed/(R1+self.W/2)
        if wheel_angle<0:
            ang_vel*=-1
        print("ang vel="+str(ang_vel))
        dtheta=np.rad2deg(ang_vel*self.dt)
        print("detheta="+str(dtheta))

        B=(180-abs(dtheta))/2-np.rad2deg(alpha)

        L=abs(2*R*sind(abs(dtheta)/2))

        # Change in position of car in car frame (x,y)
        d_c=(L*sind(B), L*cosd(B))
        print("dc="+str(d_c))

        self.x+=d_c[0]*cosd(self.theta)+self.vel*cosd(self.theta)*self.dt+d_c[1]*cosd(self.theta)#+(COR_f[0]-COR_i[0])
        self.y+=d_c[1]*sind(self.theta)+self.vel*sind(self.theta)*self.dt+d_c[0]*sind(self.theta)#+(COR_f[1]-COR_i[1])

        self.theta+=dtheta

        # self.theta=self.theta % 360

        print(self.x,self.y,self.theta)
        print("\n\n")

        self.updateSpriteOrigin()
        # self.car,self.rect=self.rot_center(self.theta)
        theta = self.theta % 360
        # self.car=pygame.transform.rotozoom(self.car,theta,1)
        # self.car = self.angled_car_list[theta]


        # self.rect = self.car.get_rect()




if __name__ == '__main__':
    test_car=car(50,0,"protagonist")
    right_car=car(50,0,"protagonist")
    a=Rectangle((test_car.x,test_car.y),test_car.car_width,test_car.car_height, angle=test_car.theta,alpha=.5)
    # b=Rectangle((right_car.x,right_car.y),right_car.car_width,right_car.car_height, angle=right_car.theta,alpha=.5,color='purple')

    fig, ax = plt.subplots(1)
    ax.add_patch(a)
    # ax.add_patch(b)


    for i in range(10):
        test_car.turnCar(15)
        b=Rectangle((test_car.x,test_car.y),test_car.car_width,test_car.car_height, angle=test_car.theta,color="red",alpha=1)
        ax.add_patch(b)

    for i in range(20):
        test_car.turnCar(-15)
        b=Rectangle((test_car.x,test_car.y),test_car.car_width,test_car.car_height, angle=test_car.theta,color="green",alpha=1)
        ax.add_patch(b)

    for i in range(10):
        test_car.turnCar(15)
        b=Rectangle((test_car.x,test_car.y),test_car.car_width,test_car.car_height, angle=test_car.theta,color="red",alpha=1)
        ax.add_patch(b)

    # ax.set_aspect('equal', 'box')
    ax.set_xlim(0,1250)
    ax.set_ylim(-20,180)
    ax.grid()
    plt.show()



