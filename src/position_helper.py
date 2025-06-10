from constants import *

def limit_axis(position):
    """
    Limit the position of the axis to the maximum allowed value.
    """
    if position[0] < 0:
        position = (0, position[1])
    if position[1] < 0:
        position = (position[0], 0)

    if position[1] > AXIS_MAX_R:
        position = (position[0], AXIS_MAX_R)
    
    return position

def position_at_target(one_position, target, tolerance=0.1):
    return (one_position >= target - tolerance and one_position <= target + tolerance)