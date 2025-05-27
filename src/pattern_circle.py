
"""
Generate circle
Increment theta clockwise until rotations count reached.
Rho position is always 0.
"""

T_FULL_ROTATION = 2 * 3.141592653589793  # Full rotation in radians - 2pi
T_RAD_PER_STEP = T_FULL_ROTATION / 100

R_POS = 0 # Fixed rho position for circle

class pattern_circle:
    
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
    p = pattern_circle()
    for move in p.get_pattern():
        print(move)