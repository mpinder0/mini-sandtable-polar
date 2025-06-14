from constants import *
import position_helper

ZIGZAGS_IN_FULL_TRAVEL = 5  # Number of zigzags in full travel

# ZigZag THETA
# - Rho start: 0
# - Rho end: AXIS_MAX_R
# Oscilate theta:
# - Theta start: start pos - size / 2
# - Theta end: start pos + size / 2
#
# ZigZag RHO
# - Theta start: 0
# - Theta end: T_FULL_ROTATION
# Oscilate theta:
# - Rho start: start pos - size / 2
# - rho end: start pos + size / 2

class PatternZigzag:
    ax = None
    start = None
    size = None
    pattern = []

    def __init__(self, ax=axis.THETA, start=0.5, size=1):
        self.ax = ax
        self.pattern = []

        self.start = start
        self.oscillate_min = start - size / 2
        self.oscillate_max = start + size / 2

        if self.ax == axis.THETA:
            self.travel_min = 0
            self.travel_max = AXIS_MAX_R
        elif self.ax == axis.RHO:
            self.travel_min = 0
            self.travel_max = T_FULL_ROTATION
        else:
            raise ValueError("Invalid axis specified. Use axis.THETA or axis.RHO.")
        
        self.travel_distance_per_oscillation = (self.travel_max - self.travel_min) / ZIGZAGS_IN_FULL_TRAVEL

        self._generate()
    
    def _add_position(self, pos_travel, pos_oscillate):
        if self.ax == axis.THETA:
            # Oscillate theta
            pos = (pos_oscillate, pos_travel)
        else:
            # Oscillate rho
            pos = (pos_travel, pos_oscillate)

        self.pattern.append(position_helper.limit_axis(pos))

    def _generate(self):
        pos_travel = self.travel_min
        pos_oscillate = self.start
        direction = 1  # 1 for positive, -1 for negative

        # Add the initial position
        self._add_position(pos_travel, pos_oscillate)

        while pos_travel < self.travel_max:
            pos_travel += self.travel_distance_per_oscillation
            pos_oscillate = self.oscillate_max if direction == 1 else self.oscillate_min
            direction *= -1
            self._add_position(pos_travel, pos_oscillate)

    def get_pattern(self):
        return self.pattern
    
if __name__ == "__main__":
    print("Zigzag in THETA axis:")
    # size 1 rad
    p = PatternZigzag(ax=axis.THETA, start=0.5, size=1)
    for move in p.get_pattern():
        print(move)

    print("Zigzag in RHO axis:")
    p2 = PatternZigzag(ax=axis.RHO, start=25, size=50)
    for move in p2.get_pattern():
        print(move)