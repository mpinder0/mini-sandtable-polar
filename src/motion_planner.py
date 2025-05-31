
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

import math
import time
from constants import *

class MotionPlanner:

    motors = None
    current_position = (0, 0) # (theta, rho)

    def __init__(self, motors):
        self.motors = motors
        # check axis speed doesn't exceed time step
        ex_string = "{} motor steps per time step should be <=1, but is {}. Consider reducing speed or time step."
        if AXIS_STEP_RATE_T > 1:
            raise Exception(ex_string.format('Theta', AXIS_STEP_RATE_T))
        if AXIS_STEP_RATE_R > 1:
            raise Exception(ex_string.format('Rho', AXIS_STEP_RATE_R))

    def reference_routine(self):
        # routine to seek reference position for (0,0)
        #
        # Todo: seek reference sensor
        #
        self.current_position = (0, 0)

    def _count_steps_to_position(self, position, position_next):
        # subtract current position from target position
        pos_change = (position_next[0]-position[0], position_next[1]-position[1])
        
        # calulcate number of motor steps to complete the move
        steps_t = pos_change[0] / AXIS_STEP_T
        steps_r = pos_change[1] / AXIS_STEP_R
        steps = (steps_t, steps_r)
        
        return steps
    
    def _get_axis_steps_list(self, max_time_steps, steps):
        # determine physical steps to time steps ratio
        ratio = steps / max_time_steps

        result = []
        cumulative_ratio = 0.0

        # for max time stpes to move, set active steps in list
        for i in range(int(max_time_steps)):
            # Increment cumulative ratio
            cumulative_ratio += ratio

            # Append True if cumulative ratio exceeds the current index + 1
            if cumulative_ratio >= 1:
                result.append(True)
                cumulative_ratio -= 1  # Reset cumulative ratio for the next step
            else:
                result.append(False)
        return result

    def get_steps_for_move(self, position, position_next):
        '''
        return dict
            directions - tuple F/R for each axis
            axis_steps_list - list of tuples (theta, rho) for each time step
        )
        '''
        # get the number of steps between current and new position
        step_counts = self._count_steps_to_position(position, position_next)
        
        # get directions - negative is reverse
        directions = tuple((direction.FORWARD if x > 0 else direction.FORWARD for x in step_counts))
        step_counts_abs = tuple(map(abs, step_counts))

        # calculate the number of time steps required to move the distance
        time_steps_t = math.ceil(step_counts_abs[0] / AXIS_STEP_RATE_T)
        time_steps_r = math.ceil(step_counts_abs[1] / AXIS_STEP_RATE_R)
        time_steps = (time_steps_t, time_steps_r)
        # get the maximum
        max_time_steps = max(time_steps)

        # create the axis step lists
        theta_list = self._get_axis_steps_list(max_time_steps, step_counts_abs[0])
        rho_list = self._get_axis_steps_list(max_time_steps, step_counts_abs[1])
        steps_list = list(zip(theta_list, rho_list))

        # create the result dictionary
        result_dict = {
            'directions': directions,
            'axis_steps_list': steps_list
        }
        return result_dict

    def _play_one_axis_step(self, axis, dir, gear_ratio):
        is_reverse = dir != direction.FORWARD
        for i in range(int(gear_ratio)):
            self.motors.step(axis, is_reverse)

    def _play_both_axis_step(self, dir, step):
        rho_count = 0
        
        if step[0]:
            self._play_one_axis_step(axis.THETA, dir[0], AXIS_GEAR_RATIO_T)
            # axis coupled, so rho must also step.
            # rho -1 for each theta +1 and vice versa
            if dir[0] == direction.FORWARD:
                rho_count -= 1
            else:
                rho_count += 1
        
        if step[1]:
            rho_count += 1 if dir[1] == direction.FORWARD else -1

        rho_direction = direction.FORWARD if rho_count >= 0 else direction.BACKWARD
        rho_count = abs(rho_count)
        for i in range(rho_count):
            self._play_one_axis_step(axis.RHO, rho_direction, AXIS_GEAR_RATIO_R)


    def play_move(self, move):
        axis_steps_list = move['axis_steps_list']
        directions = move['directions']

        # iterate through the axis steps list
        for step in axis_steps_list:
            # execute the axis steps
            self._play_both_axis_step(directions, step)
            # wait for time step
            time.sleep(TIME_STEP_S)
    
    def play(self, pattern):
        # loop through position changes
        for position in pattern:
            move = self.get_steps_for_move(self.current_position, position)
            # execute motor steps to complete the move
            self.play_move(move)
            self.current_position = position

if __name__ == "__main__":
    print("## CONSTANTS")
    print("Time step:", TIME_STEP_S, "seconds")
    print("Axis step size: {}, {}".format(AXIS_STEP_T, AXIS_STEP_R))
    print("Axis speed (unit/s): {}, {}".format(AXIS_SPEED_T, AXIS_SPEED_R))
    print("Axis step rate (steps/time step): {}, {}".format(AXIS_STEP_RATE_T, AXIS_STEP_RATE_R))

    p = MotionPlanner(None)
    print(p._count_steps_to_position((0, 0),(2, 10)))

    print(p.get_steps_for_move((0, 0), (2, 10)))