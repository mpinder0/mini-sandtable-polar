
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
from pattern_circle import PatternCircle

motors = MotorControl()
planner = MotionPlanner(motors)

print("Referenceing...")
# Zero the motors
planner.reference_routine()

print("Loading a circle...")
# load a pattern
p = PatternCircle()
pattern = p.get_pattern()

print("Pattern loaded. Executing...")
# Ececute the pattern
planner.play(pattern)