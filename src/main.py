
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

import motor_control
import motion_planner
import pattern_spiral

motors = motor_control()
planner = motion_planner(motors)

spiral = pattern_spiral()
pattern = spiral.get_pattern()

planner.play(pattern)