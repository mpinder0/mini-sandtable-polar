
"""
Translate move pattern points into time-based intermediate/ step based moves

## Constants
- Axis speed - theta, rho
- Axis step size - theta, rho
- Axis min max - theta, rho
- Time increment size 

## Functionality
- Using start/ end point - time to complete move
- Pattern execution time
- Intermediate moves (linear), time steps
- Physical stuff
    - Axis min/max
    - Pattern scaling if needed?
    - Get step action - given current and requested position
- Play pattern
    - track current pos
    - return next action

## Play pattern rough structure
- Iterate pattern moves
    - Planner - get intermediate moves (from current, next pos)
    - Iterate intermediate moves
        - Planner - get step action
            - return step action
            - Update current pos
        - Delay time increment size
"""

class motion_planner:
    def __init__(self):
        pass