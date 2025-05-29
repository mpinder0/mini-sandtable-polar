
"""
- calls to motion planner
    - current position - get, set zero
    - play pattern
    - move to position
- Physical stuff
    - Zeroing/ reference
    - Motor control - stepper step


## Rough structure
- Get pattern
- Planner - load pattern and play
    - (callback?) execute motor action
"""

from motor_control import MotorControl
from motion_planner import MotionPlanner
from pattern_spiral import PatternSpiral

motors = MotorControl()
planner = MotionPlanner(motors)

spiral = PatternSpiral()
pattern = spiral.get_pattern()

planner.play(pattern)