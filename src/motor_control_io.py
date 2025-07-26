"""
Control of stepper motors using direct GPIO to an A4988 Stepper Motor Driver or equivalent.

2 motors:
stepper 1 - theta control
stepper 2 - rho control
"""

import RPi.GPIO as GPIO
from constants import *
import time
from datetime import datetime, timedelta

REFERENCE_SENSOR_PIN = 4 # GPIO pin for the reference sensor

# Motor control pins
THETA_STEP_PIN = 17 # Theta step when True
THETA_DIR_PIN = 22 # Theta direction - CW when True
RHO_STEP_PIN = 10
RHO_DIR_PIN = 11

MOTORS_ENABLE_PIN = 5

STEP_PULSE_WIDTH = 0.001 # seconds, pulse width for the step signal

class MotorControlIO:
    
    theta_timestamp = datetime.now()
    rho_timestamp = datetime.now()
    enabled = True
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        GPIO.setup(REFERENCE_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Sensor pin set as input w/ pull-up
        GPIO.setup(THETA_STEP_PIN, GPIO.OUT)
        GPIO.setup(THETA_DIR_PIN, GPIO.OUT)
        GPIO.setup(RHO_STEP_PIN, GPIO.OUT)
        GPIO.setup(RHO_DIR_PIN, GPIO.OUT)
        GPIO.setup(MOTORS_ENABLE_PIN, GPIO.OUT)
        self._motors_set_enable(True)

    def _motors_set_enable(self, enable):
        self.enabled = enable
        # both drivers are enabled or disabled at the same time
        GPIO.output(MOTORS_ENABLE_PIN, not enable)  # Enable pins are active low
    
    def motors_release(self):
        self._motors_set_enable(False)  # Disable motors

    def step(self, ax, reverse=False):
        self._motors_set_enable(True)  # Ensure motors are enabled

        if ax == axis.THETA:
            self.theta_step(reverse)
        elif ax == axis.RHO:
            self.rho_step(reverse)
        else:
            raise ValueError("Invalid axis. Use 'axis.THETA' or 'axis.RHO'.")

    def theta_step(self, reverse=False):
        if not self.enabled:
            raise RuntimeError("{} motor was asked to step when drivers were not enabled.".format("Theta"))
        
        # Wait for the minimum step delay before stepping again
        while (datetime.now() - self.theta_timestamp) < timedelta(seconds=MIN_STEP_DELAY):
            time.sleep(0.001)
        
        if AXIS_T_INVERT_DIR:
            reverse = reverse == False
        
        GPIO.output(THETA_DIR_PIN, not reverse)  # Set direction
        GPIO.output(THETA_STEP_PIN, True)  # Step the motor
        time.sleep(STEP_PULSE_WIDTH)  # Pulse width for the step signal
        GPIO.output(THETA_STEP_PIN, False)  # Reset step signal
        self.theta_timestamp = datetime.now()

    def rho_step(self, reverse=False):
        if not self.enabled:
            raise RuntimeError("{} motor was asked to step when drivers were not enabled.".format("Rho"))
        
        # Wait for the minimum step delay before stepping again
        while (datetime.now() - self.rho_timestamp) < timedelta(seconds=MIN_STEP_DELAY):
            time.sleep(0.001)
        
        if AXIS_R_INVERT_DIR:
            reverse = reverse == False
        
        GPIO.output(RHO_DIR_PIN, not reverse)  # Set direction
        GPIO.output(RHO_STEP_PIN, True)  # Step the motor
        time.sleep(STEP_PULSE_WIDTH)  # Pulse width for the step signal
        GPIO.output(RHO_STEP_PIN, False)  # Reset step signal
        self.rho_timestamp = datetime.now()
    
    def is_reference_sensor_triggered(self):
        # Sensor LOW when triggered. Low to return True.
        return GPIO.input(REFERENCE_SENSOR_PIN) == False

if __name__ == "__main__":
    mc = MotorControlIO()

    '''
    for i in range(20):
        print("Enable ON")
        mc._motors_set_enable(True)
        time.sleep(2)
        print("Enable OFF")
        mc._motors_set_enable(False)
        time.sleep(2)
    '''

    step_delay = 0.050  # seconds
    steps_t = 100
    steps_r = 100

    print("Stepping Theta {} times Forward, {} times Backward...".format(steps_t, steps_t))
    for i in range(steps_t):
        mc.step(axis.THETA)
        time.sleep(step_delay)
    for i in range(steps_t):
        mc.step(axis.THETA, reverse=True)
        time.sleep(step_delay)

    mc.motors_release()
    print("Motors released.")

    print("Stepping Rho {} times Forward, {} times Backward...".format(steps_r, steps_r))
    for i in range(steps_r):
        mc.step(axis.RHO)
        time.sleep(step_delay)
    for i in range(steps_r):
        mc.step(axis.RHO, reverse=True)
        time.sleep(step_delay)

    mc.motors_release()
    print("Motors released.")