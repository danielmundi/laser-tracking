import math

class Controller:
    def __init__(self, motor_x, motor_y):
        self.motors = []
        self.motors.append(motor_x)
        self.motors.append(motor_y)
        self.kp = 0.2   # Constant for the proportional controller

    def control(self, obj_position, laser_position):
        # First control the motor in X axis than on Y
        for i in range(2):
            # Estimated laser position (from camera)
            x_hat = self.motors[i].angle_est = laser_position(i)
            # Estimated object position (from camera) - the laser goal
            x_goal = obj_position(i)
            # Position the motor think is pointing
            x = self.motor[i].angle

            # Calculate the next position for the motor
            x = x + self.kp*(math.degrees(math.atan(x_goal))-math.degrees(math.atan(x_hat)))

            self.motors[i].set_position(x)