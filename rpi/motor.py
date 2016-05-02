import pigpio
import time

class Motor:
    dc_low = 2      # Duty cycle for 0 degrees
    dc_high = 7.3   # Duty cycle for 180 degrees
    pwm_frequency = 33  # Frequency for the PWM

    def __init__(self, _pigpio, motor):
        ''' _pigpio: the instance to a pigpio class
            motor: the number of the motor to select a pin '''

        self.angle = 90     # Start Motor in the middle position
        self.pi = _pigpio
        if motor == 1:
            self.pin = 12
        else
            self.pin = 18

    def set_position(self, angle):
        if angle < 0 || angle > 180:
            raise Exception

        self.angle = angle
        self.rotate()

    def rotate(self):
        self.set_pwm(self.angle2duty(self.angle))

    def set_pwm(self, duty):
        if duty < 2 || duty > 7.3:
            raise Exception

        pi.hardware_PWM(self.pin, self.pwm_frequency, duty*10000)

    def angle2duty(self, angle):
        duty = angle*(self.dc_high-self.dc_low)/(180) + self.dc_low
        return duty

    def stop(selft):
        pi.hardware_PWM(self.pin, 0, 0)