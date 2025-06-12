
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
#from pattern_circle import PatternCircle
from pattern_spiral import PatternSpiral
from pattern_radial_sweep import PatternRadialSweep

motors = MotorControl()
planner = MotionPlanner(motors)

print("Referenceing...")
# Zero the motors
planner.reference_routine()

print("Move to the center...")
move = planner.get_steps_for_move((0, 0))
planner.play_move(move)

print("Loading patterns...")
# load a pattern
radial = PatternRadialSweep(1)
spiral = PatternSpiral()
pattern_radial = radial.get_pattern()
pattern_spiral = spiral.get_pattern()

print("Pattern loaded. Executing...")
# Ececute the pattern
while True:
    planner.play(pattern_radial)
    planner.play(pattern_spiral)