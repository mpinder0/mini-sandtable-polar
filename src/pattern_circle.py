
"""
Generate spiral
Start at 0, spiral clockwise outward until axis max reached.

Given
Axis max - rho
Rho increment rate, mm per full rotation
Theta step size - probaby multiples of axis step size.
"""

T_DEG_PER_STEP = 1

R_AXIS_MAX = 10
R_INCREMENT_RATE_COMPLETE = 1 # mm per rotation

R_INCREMENT_RATE_STEP = R_INCREMENT_RATE_COMPLETE / (360 * T_DEG_PER_STEP)

class pattern_spiral:
    
    pattern = []
    
    def __init__(self):
        self._generate()
    
    def _generate(self):
        t_pos = 0
        r_pos = 0
        if R_INCREMENT_RATE_STEP > 0:
            while r_pos < R_AXIS_MAX:
                t_pos += T_DEG_PER_STEP
                r_pos += R_INCREMENT_RATE_STEP
                self.pattern.append((t_pos, r_pos))

    def get_pattern(self):
        return self.pattern


if __name__ == "__main__":
    p = pattern_spiral()
    for move in p.get_pattern():
        print(move)