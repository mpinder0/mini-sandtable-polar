
"""
Generate circle
Increment theta clockwise until rotations count reached.
Rho position is always static.
"""

from constants import *

T_RAD_PER_STEP = T_FULL_ROTATION / 100

R_POS = 35 # Fixed rho position for circle

class PatternCircle:
    
    pattern = []
    
    def __init__(self, n_rotations):
        self._generate(n_rotations)
    
    def _generate(self, n_rotations):
        pos_t = 0
        pos_t_target = n_rotations * T_FULL_ROTATION
        while pos_t < pos_t_target:
            pos_t += T_RAD_PER_STEP
            self.pattern.append((pos_t, R_POS))

    def get_pattern(self):
        return self.pattern


if __name__ == "__main__":
    p = PatternCircle(10)
    for move in p.get_pattern():
        print(move)

    count = len(p.get_pattern())
    print(str(count) + " moves generated.")
    print("will take " + str(count * TIME_STEP_S) + " seconds to execute.")
