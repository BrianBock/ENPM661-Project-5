import math

def cosd(deg_angle):
	a=math.cos(math.deg2rad(deg_angle))
	return a

def sind(deg_angle):
	a=math.sin(math.deg2rad(deg_angle))
	return a

def tand(deg_angle):
	a=math.tan(math.deg2rad(deg_angle))
	return a


def cotd(deg_angle):
	a=math.sin(math.deg2rad(deg_angle))
	b=math.cos(math.deg2rad(deg_angle))

	cotd=b/a
	return cotd

def cot(rad_angle):
	a=math.sin(rad_angle)
	b=math.cos(rad_angle)
	cot=b/a
	return cot