
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
from datetime import datetime, timedelta
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

    def _seek_reference_sensor(self):
        T_FULL_ROTATION = 2 * 3.141592653589793
        T_FULL_ROTATION_STEPS = int(T_FULL_ROTATION / AXIS_STEP_T)  # number of steps for full rotation
        T_STEP_DELAY = 0.0  # no delay
        R_STEP_INC = 11

        start_time = datetime.now()
        timeout = timedelta(seconds=60)  # 10 seconds timeout for seeking reference

        while datetime.now() - start_time < timeout:
            # loop theta, full rotation    
            for i in range(T_FULL_ROTATION_STEPS):
                self._play_both_axis_step((direction.FORWARD, direction.FORWARD), (True, False))
                # check for reference sensor
                if self.motors.is_reference_sensor_triggered():
                    return True # reference sensor found - success
                time.sleep(T_STEP_DELAY)

            # increment rho
            for i in range(R_STEP_INC):
                self._play_both_axis_step((direction.FORWARD, direction.FORWARD), (False, True))
        return False # reference sensor not found within timeout
    
    def reference_routine(self):
        # routine to seek reference position, apply offset to centre then set position to (0,0)
        R_RETURN_TO_CENTRE = -5  # mm, distance to return rho to centre after detecting reference

        found_reference = self._seek_reference_sensor()
        if found_reference:
            # move rho to centre
            move = self.get_steps_for_move(self.current_position, (0, R_RETURN_TO_CENTRE))
            self.play_move(move)
            # this position is 0,0
            self.current_position = (0, 0)
        else:
            raise Exception("Reference sensor not found. Check motor connections and sensor functionality.")

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
        params
            position - tuple int (theta, rho) current position
            position_next - tuple int (theta, rho) next position
        return dict
            directions - tuple F/R for each axis
            axis_steps_list - list of tuples (theta, rho) for each time step
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
        '''
        params
        move - dict:
            axis_steps_list - list of tuples (theta, rho) contraining step True/False for each time step
            directions - tuple F/R for each axis
        '''
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
