
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

    def _do_simple_reference_move(self, ax, dir, desired_state, steps_in_state, step_limit):
        step_count = 0
        in_state_count = 0
        directions = (dir, dir)
        step_instructions = (ax == axis.THETA, ax == axis.RHO)
        while step_count < step_limit:
            self._play_both_axis_step(directions, step_instructions)
            step_count += 1
            # check for reference sensor
            if self.motors.is_reference_sensor_triggered() == desired_state:
                in_state_count += 1
                print(".", end='', flush=True)
            # steps in desired state met, return
            if in_state_count >= steps_in_state:
                print("Found ref:{} - {}{}".format(desired_state, ax, dir))
                return step_count
            time.sleep(MIN_STEP_DELAY)
        raise Exception("Error during reference routine. could not find reference={} before exceeding step limit, moving axis {}".format(desired_state, ax))

    def reference_routine(self):
        T_FULL_ROTATION = 2 * 3.141592653589793
        T_FULL_ROTATION_STEPS = int(T_FULL_ROTATION / AXIS_STEP_T) # number of steps for full rotation
        R_STEP_INC = 65 * 2 # ~2mm
        STEPS_IN_STATE = 5 # number of steps in desired state to consider it found
        R_STEPS_TO_LIMIT = 65 * 4
        R_DIST_TO_CENTRE = 45  # mm, distance to return rho to centre after detecting reference

        start_time = datetime.now()
        timeout = timedelta(minutes=30)  # 30 minutes timeout for seeking reference (it moves slowly)
        in_state_count = 0
        found_reference = False

        # find the sensor leading edge - spiralling outwards
        while datetime.now() - start_time < timeout and not found_reference:
            # loop theta, full rotation    
            for i in range(T_FULL_ROTATION_STEPS):
                self._play_both_axis_step((direction.FORWARD, direction.FORWARD), (True, False))
                # check for reference sensor
                if self.motors.is_reference_sensor_triggered():
                    in_state_count += 1
                    print(".", end='', flush=True)
                # steps in desired state met
                if in_state_count >= STEPS_IN_STATE:
                    print("Found theta+")
                    found_reference = True
                    break
                time.sleep(MIN_STEP_DELAY)

            if not found_reference:
                # increment rho
                print("rho step out")
                for i in range(R_STEP_INC):
                    self._play_both_axis_step((direction.FORWARD, direction.FORWARD), (False, True))
                    time.sleep(MIN_STEP_DELAY)

        if found_reference:        
            print("Ref found... refining position")
            # find the sensor trailing edge in theta
            ref_step_count = self._do_simple_reference_move(axis.THETA, direction.FORWARD, False, STEPS_IN_STATE, 500)
            print("Theta step count:", ref_step_count)

            print("Moving to theta mid point")
            # move to the middle of the leading and trailing edges
            count_mid = int(ref_step_count / 2)
            for i in range(count_mid):
                self._play_both_axis_step((direction.BACKWARD, direction.BACKWARD), (True, False))
                time.sleep(MIN_STEP_DELAY)

            if not self.motors.is_reference_sensor_triggered():
                raise Exception("Ref sensor not found after moving to Theta mid point.")

            print("Finding rho trailing edge")
            # find the sensor trailing edge in rho
            self._do_simple_reference_move(axis.RHO, direction.BACKWARD, False, STEPS_IN_STATE, 500)

            # move rho to the limit
            print("Moving rho to limit")
            for i in range(R_STEPS_TO_LIMIT):
                self._play_both_axis_step((direction.FORWARD, direction.FORWARD), (False, True))
                time.sleep(MIN_STEP_DELAY)
            
            self.current_position = (0, R_DIST_TO_CENTRE)
            print("Referencing complete.")
        else:
            raise Exception("Reference sensor not found before timeout")

    def _count_steps_to_position(self, position, position_next):
        # subtract current position from target position
        pos_change = (position_next[0]-position[0], position_next[1]-position[1])
        
        # calulcate number of motor steps to complete the move
        steps_t = int(pos_change[0] / AXIS_STEP_T)
        steps_r = int(pos_change[1] / AXIS_STEP_R)
        steps = (steps_t, steps_r)
        
        print("start, end:", self.current_position, position_next)
        print("steps:", steps)
        
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

    def get_steps_for_move(self, position_next):
        '''
        params
            position - tuple int (theta, rho) current position
            position_next - tuple int (theta, rho) next position
        return dict
            directions - tuple F/R for each axis
            axis_steps_list - list of tuples (theta, rho) for each time step
        '''
        # get the number of steps between current and new position
        step_counts = self._count_steps_to_position(self.current_position, position_next)
        
        # get directions - negative is reverse
        directions = tuple((direction.FORWARD if x > 0 else direction.BACKWARD for x in step_counts))
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
            'start_position': self.current_position,
            'end_position': position_next,
            'directions': directions,
            'axis_steps_list': steps_list
        }
        return result_dict

    def _play_one_axis_step(self, axis, dir, gear_ratio):
        is_reverse = dir != direction.FORWARD
        for i in range(int(gear_ratio)):
            self.motors.step(axis, is_reverse)
            time.sleep(MIN_STEP_DELAY)  # small delay to allow motor to step

    def _play_both_axis_step(self, dir, step):
        rho_count = 0
        
        if step[0]:
            self._play_one_axis_step(axis.THETA, dir[0], AXIS_GEAR_RATIO_T)
            # axis coupled, so rho must also step.
            # rho -1 for each theta +1 and vice versa
            if dir[0] == direction.FORWARD:
                rho_count += 1
            else:
                rho_count -= 1
        
        if step[1]:
            rho_count += 1 if dir[1] == direction.FORWARD else -1

        #print(1 if step[0] else 0, rho_count)

        rho_direction = direction.FORWARD if rho_count >= 0 else direction.BACKWARD
        rho_count = abs(rho_count)
        for i in range(rho_count):
            self._play_one_axis_step(axis.RHO, rho_direction, AXIS_GEAR_RATIO_R)


    def play_move(self, move):
        '''
        params
        move - dict:
            start_position - tuple (theta, rho) current position
            end_position - tuple (theta, rho) next position
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
        
        self.current_position = move["end_position"]
    
    def play(self, pattern):
        # loop through position changes
        for position in pattern:
            move = self.get_steps_for_move(position)
            # execute motor steps to complete the move
            self.play_move(move)

if __name__ == "__main__":
    print("## CONSTANTS")
    print("Time step:", TIME_STEP_S, "seconds")
    print("Axis step size: {}, {}".format(AXIS_STEP_T, AXIS_STEP_R))
    #print("Axis speed (unit/s): {}, {}".format(AXIS_SPEED_T, AXIS_SPEED_R))
    print("Axis step rate (steps/time step): {}, {}".format(AXIS_STEP_RATE_T, AXIS_STEP_RATE_R))

    p = MotionPlanner(None)
    p.current_position = (0, 0)
    print(p._count_steps_to_position((2, 10)))

    p.current_position = (0, 0)
    print(p.get_steps_for_move((2, 10)))
