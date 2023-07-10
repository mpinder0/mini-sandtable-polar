
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

AXIS_MAX_R = 10.0 # mm, min always 0
TIME_STEP_S = 0.5

# step size - units
AXIS_STEP_T = 0.0174533 # radians
AXIS_STEP_R = 0.5       # mm

# speed - untis per second
AXIS_SPEED_T = 0.0174533
AXIS_SPEED_R = 1

class motion_planner:

    motors = None
    position = (0, 0)
    pattern = []
    AXIS_STEPS_SPEED_T = 0
    AXIS_STEPS_SPEED_R = 0

    def __init__(self, motors):
        self.motors = motors
        AXIS_STEPS_SPEED_T = _motor_steps_per_time_step(TIME_STEP_S, AXIS_STEP_T, AXIS_SPEED_T)
        AXIS_STEPS_SPEED_R = _motor_steps_per_time_step(TIME_STEP_S, AXIS_STEP_R, AXIS_SPEED_R)

    def load_pattern(self):
        pass

    def _motor_steps_per_time_step(self, time_step, axis_step, speed):
        result =  speed / axis_step * time_step
        ex_string = "Motor steps per time step should be <1, but is {}. Consider reducing speed or time step."
        if result > 1:
            raise Exception(ex_string.format(result))
        return result

    def _count_steps_to_position(self, new_position):
        # subtract current position from target position
        pos_change = tuple(map(lambda t, r: t - r, new_position, self.position))
        
        # get directions
        directions = tuple(('F' if x > 0 else "R" for x in pos_change))
        
        pos_change = tuple(map(abs, pos_change))

        # calulcate number of motor steps to complete the move
        steps_t = pos_change[0] / AXIS_STEP_T
        steps_r = pos_change[1] / AXIS_STEP_R
        steps = (steps_t, steps_r)

        max_steps = max(steps)
        
        # time to move
        time_t = pos_change[0] / AXIS_SPEED_T
        time_r = pos_change[1] / AXIS_SPEED_T
        # time steps to move
        time_steps_t = time_t * TIME_STEP_S
        time_steps_r = time_r * TIME_STEP_S
        time_steps = (time_steps_t, time_steps_r)

        max_time_steps = max(time_steps)
        
        return steps


    def play(self):
        # get next action steps
        pass


if __name__ == "__main__":
    print("## CONSTANTS")
    print("Time step:", TIME_STEP_S, "seconds")
    print("AXIS_STEPS_SPEED_T:", AXIS_STEPS_SPEED_T, " motor steps per time step")
    print("rad", AXIS_STEPS_SPEED_T * AXIS_STEP_T)
    print("AXIS_STEPS_SPEED_R:", AXIS_STEPS_SPEED_R, " motor steps per time step")
    print("mm", AXIS_STEPS_SPEED_R * AXIS_STEP_R)

    p = motion_planner(None)
    print(p._count_steps_to_position((2, 10)))