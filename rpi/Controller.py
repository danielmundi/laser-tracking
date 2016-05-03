import math, time, pigpio
from threading import Thread
import threading
from Identification import Identification
import numpy as np

class Controller():
    def __init__(self, _pigpio, motor_x, motor_y, sampling_period):
        #Thread.__init__(self)
        self.motors = []
        self.motors.append(motor_x)
        self.motors.append(motor_y)
        self.sampling_period = sampling_period
        self.kp = 0.001   # Constant for the proportional controller
        self.object = Identification()
        self.laser = Identification()
        #self.__stop = threading.Event()
        self.pi = _pigpio

        self.laser_pin = 16
        self.pi.set_mode(self.laser_pin, pigpio.OUTPUT)  # laser
        self.pi.set_pull_up_down(self.laser_pin, pigpio.PUD_DOWN)

        self.pi.write(self.laser_pin, 1)

    def run(self):
        #self.pi.write(self.laser_pin, 1)

        while not self.stopped():
            self.control()
            time.sleep(self.sampling_period)

        #self.pi.write(self.laser_pin, 0)

        # Stop all motors
        #list(map(lambda x: x.stop(), self.motors))

    def update_positions(self,_object, _laser):
        self.object = _object
        self.laser = _laser

    def target(self, pos):
        x, y = pos
        screen = np.array([float(x), float(y), 1.0])
        servo = self.transform.dot(screen)
        servo = servo/servo[2]

        self.motors[0].set_position(round(servo[0]))
        time.sleep(0.05)
        self.motors[1].set_position(round(servo[1]))

        print("({0},{1}) = ({2},{3})".format(x, y, round(servo[0]), round(servo[1])))

    def control(self):
        if not self.laser.visible:
            return

        # First control the motor in X axis than on Y
        for i in range(2):
            # Estimated laser position (from camera)
            x_hat = self.motors[i].angle_est = self.laser.position[i]
            # Estimated object position (from camera) - the laser goal
            x_goal = self.object.position[i]
            # Position the motor think is pointing
            x = self.motors[i].angle

            # Calculate the next position for the motor
            x = x + self.kp*(math.degrees(math.atan(x_goal))-math.degrees(math.atan(x_hat)))

            self.motors[i].set_position(x)

    def stop(self):
        self.pi.write(self.laser_pin, 0)

        # Stop all motors
        list(map(lambda x: x.stop(), self.motors))

        #self.__stop.set()

    def stopped(self):
        return self.__stop.isSet()

    def generate_transform(self):
        x1 = -0.3
        y1 =  0.25
        x2 =  0.25
        y2 =  0.25
        x3 =  0.25
        y3 = -0.29
        x4 = -0.37
        y4 = -0.39

        X1 =  70
        Y1 = 100
        X2 = 115
        Y2 = 100
        X3 = 115
        Y3 =  70
        X4 =  70
        Y4 =  72

        A = np.array([  [x1, y1,  1,  0,  0,  0, -X1*x1, -X1*y1],
                        [ 0,  0,  0, x1, y1,  1, -Y1*x1, -Y1*y1],
                        [x2, y2,  1,  0,  0,  0, -X2*x2, -X2*y2],
                        [ 0,  0,  0, x2, y2,  1, -Y2*x2, -Y2*y2],
                        [x3, y3,  1,  0,  0,  0, -X3*x3, -X3*y3],
                        [ 0,  0,  0, x3, y3,  1, -Y3*x3, -Y3*y3],
                        [x4, y4,  1,  0,  0,  0, -X4*x4, -X4*y4],
                        [ 0,  0,  0, x4, y4,  1, -Y4*x4, -Y4*y4] ])
        B = np.array([X1, Y1, X2, Y2, X3, Y3, X4, Y4])
        # Solve for coefficients x in equation Ax = B
        x = np.linalg.solve(A, B)
        # Set transformation matrix with coefficients
        self.transform = np.array([  [x[0], x[1], x[2]],
                                     [x[3], x[4], x[5]],
                                     [x[6], x[7],  1.0] ])