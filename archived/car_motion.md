## Car Motion
The car we are modeling is a front wheel steer (FWS), rear wheel drive (RWD), 4 wheeled vehicle utilizing Ackerman steering. This setup was chosen to closely mirror the steering dynamics of a real car. Physical cars move with non-holonomic motion, so it is important that our simulator replicate this behavor.

![Car dimensions diagram](https://github.com/BrianBock/ENPM661-Project-5/blob/master/Report/rear_wheel_drive.png)


The figure above defines our key car dimensions. We'll be using the notation in this diagram for the duration of this paper. For simplicity, we assume that the two front wheels must remain mutually parallel. Therefore, we only have one wheel angle δ. We also define C, the vehicle's center of mass, to be in the physical center of the vehicle, and therefore:

a_2=l/2

Without loss of generality, we'll assume that the two rear wheels are actuated at equal speeds:

ω_i=ω_0=ω

The turning radius about O is:

R=\sqrt{a_2^2+l^2cot^2(δ)}

By simple trigonometry, we define a new angle α, which is the angle between R_1 and R:

α=sin^{-1}(a_2/R)


R_1, the horizontal distance between $C$ and $O$ (Figure \ref{fig:COR_wheelangles}) is:

R_1=Rcos(α)


The yaw rate, or angular velocity, of the vehicle can be defined as follows:

r = (R_w ω)/(R_1+(W/2))


From the car's perspective, as the car turns, it drives out an arc with radius R. The angle the car subtends as it travels dθ is a function of the vehicle's yaw rate r and the time it has to move dt:

dθ = r . dt

![Car turning diagram](https://github.com/BrianBock/ENPM661-Project-5/blob/master/Report/car_motion_diag.png)

The figure above displays the motion of the car (in the car's reference frame) as it moves through it's arc. L is the shortest Euclidean distance between the start position and end position; a chord of the circle of movement, defined by R and d\theta:

L=2Rsin(dθ/2)


We're interested in finding d_x and d_y, the components of the displacement of the car in the car's reference frame. Note that the center of rotation O also moves with the car. This d_x and d_y exclusively measure the displacement of the car relative to O and do not yet account for the motion of O. d_x and d_y are in directions coincident with X_{c1} and Y_{c_1}, the car's initial direction vectors, and not aligned with the global X_w and Y_w coordinate system. We will later compensate for the initial angle of the car in the world frame, but for now we can work with just the car frame without loss of generality. Since Y_{c1} is defined to be parallel to R_1, we know the angle between R and Y_{c1} must also be α. The triangle ∆RLR must be an isosceles triangle. 


2(β + α) + dθ = 180°

Rearranging to solve for β:

β=(180°-dθ)/2

We now have enough information to compute the components of the displacement of the car:

d_x=Lsin(β)

d_y=Lcos(β)


We need to compensate for angle θ of the car as well as the motion of O as the car moves. 
The component of d_x and d_y in the X_w direction is:

d_{x_w}=d_xcos(θ)+d_ycos(θ)

Similarly,

d_{y_w}=d_ysin(θ)+d_xsin(θ)


The center of rotation $O$ moves as a function of the car's forward velocity $v$, the car's angle $\theta$, and the time it has to move $dt$:

O_{x}=vcos(θ)dt


O_{y}=vsin(θ)dt


Finally, the new position of the car can be computed as follows:
\begin{align}
    x_{f}&=d_{x_w}+O_x\\
    x_f&=d_xcos(\theta)+d_ycos(\theta)+vcos(\theta)dt
\end{align}
\begin{align}
    y_{f}&=d_{y_w}+O_y\\
    y_f&=d_ysin(\theta)+d_xsin(\theta)+vsin(\theta)dt
\end{align}
\begin{equation}
    \theta_f=\theta+d\theta
\end{equation}
