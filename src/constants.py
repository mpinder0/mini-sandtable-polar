from enum import Enum

class axis(Enum):
    THETA = 1
    RHO = 2

class direction(Enum):
    FORWARD = 1 # Extend/ Clockwise
    BACKWARD = 2

AXIS_MAX_R = 10.0 # mm, min always 0
TIME_STEP_S = 0.05 # seconds, 50 ms time step for the motion planner

MIN_STEP_DELAY = 0.002 # Minimum delay between steps in sections, to allow the motor to step properly

# axis gearing
AXIS_GEAR_RATIO_T = 6 # 6:1 gear ratio
AXIS_GEAR_RATIO_R = 1 # 1:1 gear ratio
# note: theta and rho axis are coupled, so for each theta step rho must also step (theta:rho - 6:1)

# step size - units
AXIS_STEP_T = 0.00306796 # * AXIS_GEAR_RATIO_T # radians
AXIS_STEP_R = 0.08726646 # * AXIS_GEAR_RATIO_R # mm

# speed - untis per second
AXIS_SPEED_T = 0.0174533
AXIS_SPEED_R = 1
# speed - motor steps per time step
#AXIS_STEP_RATE_T = AXIS_SPEED_T / AXIS_STEP_T * TIME_STEP_S
#AXIS_STEP_RATE_R = AXIS_SPEED_R / AXIS_STEP_R * TIME_STEP_S
AXIS_STEP_RATE_T = 1 # max speed
AXIS_STEP_RATE_R = 1

AXIS_T_INVERT_DIR = False
AXIS_R_INVERT_DIR = True
