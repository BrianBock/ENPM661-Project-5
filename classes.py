import math
import numpy as np
import sympy

class car():
	def __init__(self,x,y,w,h):
		self.startx=x # start position
		self.starty=y # start position
		self.car_width=w # total width of car (for bounding box)
		self.car_length=h # total height of car (for bounding box)

		self.wheel_radius

		# Front wheel drive car utlizing Ackermann Steering
		# http://ckw.phys.ncku.edu.tw/public/pub/Notes/GeneralPhysics/Powerpoint/Extra/05/11_0_0_Steering_Theroy.pdf
		self.l=20 # length between front and rear wheel axes (wheelbase)
		self.a2=self.l/2 # distance from the back axel to the center of mass of the car
		self.stationary=True

		if not self.stationary:
			self.start_velocity


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




