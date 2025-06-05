"""
Control of stepper motors on adafruit motorkit board

2 motors:
stepper 1 - theta control
stepper 2 - rho control
"""

from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import RPi.GPIO as GPIO
import board

REFERENCE_SENSOR_PIN = 4 # GPIO pin for the reference sensor

class MotorControl:
    
    kit = None
    
    def __init__(self):
        self.kit = MotorKit(i2c=board.I2C())

        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        GPIO.setup(REFERENCE_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Sensor pin set as input w/ pull-up

    def motors_release(self):
        self.kit.stepper1.release()
        self.kit.stepper2.release()
    
    def _stepper_step(self, motor, reverse=False):
        direction = stepper.BACKWARD if reverse else stepper.FORWARD
        motor.onestep(direction=direction, style=stepper.SINGLE)

    def step(self, axis, reverse=False):
        if axis == axis.THETA:
            self.theta_step(reverse)
        elif axis == axis.RHO:
            self.rho_step(reverse)
        else:
            raise ValueError("Invalid axis. Use 'axis.THETA' or 'axis.RHO'.")

    def theta_step(self, reverse=False):
        m = self.kit.stepper1
        self._stepper_step(m, reverse)

    def rho_step(self, reverse=False):
        m = self.kit.stepper1
        self._stepper_step(m, reverse)
    
    def is_reference_sensor_triggered(self):
         # Sensor LOW when triggered. Low to return True.
        return GPIO.input(REFERENCE_SENSOR_PIN) == False
