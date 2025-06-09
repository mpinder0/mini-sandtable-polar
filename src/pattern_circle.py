
"""
Generate circle
Increment theta clockwise until rotations count reached.
Rho position is always static.
"""

import constants as c

T_FULL_ROTATION = 2 * 3.141592653589793  # Full rotation in radians - 2pi
T_RAD_PER_STEP = T_FULL_ROTATION / 100

R_POS = 35 # Fixed rho position for circle

class PatternCircle:
    
    pattern = []
    
    def __init__(self, n_rotations):
        self._generate(n_rotations)
    
    def _generate(self, n_rotations):
        t_pos = 0
        t_pos_target = n_rotations * T_FULL_ROTATION
        while t_pos < t_pos_target:
            t_pos += T_RAD_PER_STEP
            self.pattern.append((t_pos, R_POS))

    def get_pattern(self):
        return self.pattern


if __name__ == "__main__":
    p = PatternCircle(10)
    for move in p.get_pattern():
        print(move)

    count = len(p.get_pattern())
    print(str(count) + " moves generated.")
    print("will take " + str(count * c.TIME_STEP_S) + " seconds to execute.")
