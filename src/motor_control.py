"""
Control of stepper motors on adafruit motorkit board

2 motors:
stepper 1 - theta control
stepper 2 - rho control
"""

from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

class motor_control:
    
    kit = None
    
    def __init__(self):
        self.kit = MotorKit(i2c=board.I2C(), steppers_microsteps=4)

    def motors_release(self):
        self.kit.stepper1.release()
        self.kit.stepper2.release()
    
    def _stepper_step(self, motor, reverse=False):
        direction = stepper.BACKWARD if reverse else stepper.FORWARD
        motor.onestep(direction=direction, style=stepper.MICROSTEP)

    def theta_step(self, reverse=False):
        m = self.kit.stepper1
        self._stepper_step(m, reverse)

    def rho_step(self, reverse=False):
        m = self.kit.stepper1
        self._stepper_step(m, reverse)