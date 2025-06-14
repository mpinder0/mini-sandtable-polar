
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
from pattern_radial_sweep import PatternRadialSweep
from pattern_zigzag import PatternZigzag
import logging
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='plotter.log')

motors = MotorControl()
planner = MotionPlanner(motors)

logger.info("Referenceing...")
# Zero the motors
planner.reference_routine()

logger.info("Move to the center...")
move = planner.get_steps_for_move((0, 0))
planner.play_move(move)

logger.info("Loading patterns...")
# load a pattern
zigza_t = PatternZigzag(ax='THETA', start=0.5, size=1)
zigza_r = PatternZigzag(ax='RHO', start=25, size=50)
radial = PatternRadialSweep(1)
spiral = PatternSpiral()

logger.info("Pattern loaded. Executing...")
# Ececute the pattern
while True:
    planner.play(zigza_t.get_pattern())
    planner.play(radial.get_pattern())
    planner.play(zigza_r.get_pattern())
    planner.play(spiral.get_pattern())