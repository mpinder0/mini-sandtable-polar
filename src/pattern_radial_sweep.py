
"""
Generate radial pattern
Start at 0, go to rho outer limit, inscrement theta then return to 0, repeat for n rotations
"""

from constants import *
import position_helper

T_STEP_SIZE = T_FULL_ROTATION / 100
R_STEP_SIZE = 2 # mm

class PatternRadialSweep:
    
    pattern = []
    
    def __init__(self, n_rotations=1):
        self.pattern = []
        self._generate(n_rotations)
    
    def _generate(self, n_rotations):
        pos_t = 0
        pos_r = 0
        pos_t_target = n_rotations * T_FULL_ROTATION
        while pos_t < pos_t_target:
            while pos_r < AXIS_MAX_R:
                pos_r += R_STEP_SIZE
                pos = position_helper.limit_axis((pos_t, pos_r))
                self.pattern.append(pos)
            
            # inscrement theta
            pos_t += T_STEP_SIZE
            self.pattern.append((pos_t, pos_r))

            while pos_r > 0:
                pos_r -= R_STEP_SIZE
                pos = position_helper.limit_axis((pos_t, pos_r))
                self.pattern.append(pos) 

            # inscrement theta
            pos_t += T_STEP_SIZE
            self.pattern.append((pos_t, pos_r))

    def get_pattern(self):
        return self.pattern

if __name__ == "__main__":
    p = PatternRadialSweep(10)
    for move in p.get_pattern():
        print(move)

    count = len(p.get_pattern())
    print(str(count) + " moves generated.")
