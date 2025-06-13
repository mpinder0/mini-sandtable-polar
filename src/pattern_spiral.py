
"""
Generate spiral
Start at 0, spiral clockwise outward until axis max reached.

Given
Axis max - rho
Rho increment rate, mm per full rotation
Theta step size - probaby multiples of axis step size.
"""

from constants import *
import position_helper

T_DEG_PER_STEP = 45
T_RAD_PER_STEP = position_helper.deg_to_rad(T_DEG_PER_STEP)

R_INCREMENT_RATE_COMPLETE = 4 # mm per rotation

R_INCREMENT_RATE_STEP = R_INCREMENT_RATE_COMPLETE / (360 * T_DEG_PER_STEP)

INNER_POS = (0,0)
OUTER_POS = (0, AXIS_MAX_R)

class PatternSpiral:
    
    pattern = []
    
    def __init__(self, r_reverse=False):
        self._generate(r_reverse)
    
    def _generate(self, r_reverse):
        if not r_reverse:
            pos_t = INNER_POS[0]
            pos_r = INNER_POS[1]
            # spiral from inner to outer
            while pos_r < OUTER_POS[1]:
                pos_t += T_RAD_PER_STEP
                pos_r += R_INCREMENT_RATE_STEP
                pos = position_helper.limit_axis((pos_t, pos_r))
                self.pattern.append(pos)
        else:
            # spiral from outer to inner
            pos_t = OUTER_POS[0]
            pos_r = OUTER_POS[1]
            while pos_r > INNER_POS[1]:
                pos_t += T_RAD_PER_STEP
                pos_r -= R_INCREMENT_RATE_STEP # move inward
                pos = position_helper.limit_axis((pos_t, pos_r))
                self.pattern.append(pos)

    def get_pattern(self):
        return self.pattern

if __name__ == "__main__":
    p = PatternSpiral()
    for move in p.get_pattern():
        print(move)