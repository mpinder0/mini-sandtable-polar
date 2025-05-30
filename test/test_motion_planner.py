import unittest
import sys
sys.path.insert(0, "src/")
from constants import axis, direction
from motion_planner import MotionPlanner
from motor_control_mock import MotorControlMock

class TestMotionPlanner(unittest.TestCase):
    motors = None
    planner = None
    
    def setUp(self):
        self.motors = MotorControlMock()
        self.planner = MotionPlanner(self.motors)
    
    '''
    def test_motor_steps_per_time_step(self):
        result = self.planner._motor_steps_per_time_step(1, 2, 2)
        self.assertEqual(1, result)
        result = self.planner._motor_steps_per_time_step(0.5, 0.0174533, 0.0174533)
        self.assertEqual(0.5, result)
        result = self.planner._motor_steps_per_time_step(0.5, 0.5, 1)
        self.assertEqual(1, result)
        # exception case, result >1
        self.assertRaises(Exception, self.planner._motor_steps_per_time_step, 1, 0.5, 1)
    '''

    def test_count_steps_to_position(self):
        #  - theta: 0.00306796 * 6 = 0.01840776 radians
        #  - rho: 0.08726646 * 1 = 0.08726646 mm
        rad_step = 0.01840776
        mm_step = 0.08726646
        
        # Test with a simple move
        position_start = (0, 0)
        position_next = (5, 5)
        steps = self.planner._count_steps_to_position(position_start, position_next)
        t = 5 / rad_step # steps in 5 rad
        r = 5 / mm_step # steos in 5 mm
        self.assertEqual(steps, (t, r))
        
        # Test with a move that requires no steps
        position_next = (0, 0)
        steps = self.planner._count_steps_to_position(position_start, position_next)
        self.assertEqual(steps, (0, 0))
        
        # Test with a negative move
        position_next = (-1, -1)
        steps = self.planner._count_steps_to_position(position_start, position_next)
        t = -1 / rad_step
        r = -1 / mm_step
        self.assertEqual(steps, (t, r))

    def test_play_one_axis_steps(self):
        # Theta axis 2 steps forward
        x = axis.THETA
        d = direction.FORWARD
        gear_ratio = 2
        self.planner._play_one_axis_step(x, d, gear_ratio)
        self.assertEqual(self.motors.theta_count, 2)
        # Theta axis 2 steps backward
        d = direction.BACKWARD
        self.planner._play_one_axis_step(x, d, gear_ratio)
        self.assertEqual(self.motors.theta_count, 0)
        # Theta axis 2 more steps backward
        self.planner._play_one_axis_step(x, d, gear_ratio)
        self.assertEqual(self.motors.theta_count, -2)

        # Rho axis 2 steps forward
        x = axis.RHO
        d = direction.FORWARD
        gear_ratio = 6
        self.planner._play_one_axis_step(x, d, gear_ratio)
        self.assertEqual(self.motors.rho_count, 6)

if __name__ == '__main__':
    unittest.main()