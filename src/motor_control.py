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
from constants import *
import time
from datetime import datetime, timedelta

REFERENCE_SENSOR_PIN = 4 # GPIO pin for the reference sensor

class MotorControl:
    
    kit = None
    theta_timestamp = datetime.now()
    rho_timestamp = datetime.now()
    
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

    def step(self, ax, reverse=False):
        if ax == axis.THETA:
            self.theta_step(reverse)
        elif ax == axis.RHO:
            self.rho_step(reverse)
        else:
            raise ValueError("Invalid axis. Use 'axis.THETA' or 'axis.RHO'.")

    def theta_step(self, reverse=False):
        # Wait for the minimum step delay before stepping again
        while (datetime.now() - self.theta_timestamp) < timedelta(seconds=MIN_STEP_DELAY):
            time.sleep(0.001)
        
        if AXIS_T_INVERT_DIR:
            reverse = reverse == False
        
        m = self.kit.stepper1
        self._stepper_step(m, reverse)
        self.theta_timestamp = datetime.now()

    def rho_step(self, reverse=False):
        # Wait for the minimum step delay before stepping again
        while (datetime.now() - self.rho_timestamp) < timedelta(seconds=MIN_STEP_DELAY):
            time.sleep(0.001)
        
        if AXIS_R_INVERT_DIR:
            reverse = reverse == False
        
        m = self.kit.stepper2
        self._stepper_step(m, reverse)
        self.rho_timestamp = datetime.now()
    
    def is_reference_sensor_triggered(self):
        # Sensor LOW when triggered. Low to return True.
        return GPIO.input(REFERENCE_SENSOR_PIN) == False

if __name__ == "__main__":
    mc = MotorControl()    

    print("Stepping Theta 500 Forward times, 500 times Backward...")
    for i in range(500):
        mc.step(axis.THETA)
        time.sleep(0.005)
    for i in range(500):
        mc.step(axis.THETA, reverse=True)
        time.sleep(0.005)
    
    print("Stepping rho 500 Forward times, 500 times Backward...")
    for i in range(500):
        mc.step(axis.RHO)
        time.sleep(0.005)
    for i in range(500):
        mc.step(axis.RHO, reverse=True)
        time.sleep(0.005)

    mc.motors_release()
    print("Motors released.")
