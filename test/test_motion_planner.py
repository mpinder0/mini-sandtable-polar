import unittest
import sys
sys.path.insert(0, "src/")
from constants import *
from motion_planner import MotionPlanner
from motor_control_mock import MotorControlMock

class TestMotionPlanner(unittest.TestCase):
    motors = None
    planner = None
    
    def setUp(self):
        self.motors = MotorControlMock()
        self.planner = MotionPlanner(self.motors)

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

    def test_play_one_axis_step(self):
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

    def test_play_both_axis_steps(self):
        step_multiplier = (AXIS_GEAR_RATIO_T, AXIS_GEAR_RATIO_R)
        results = {"FF": (1, 0),
                   "FR": (1, 2),
                   "RF": (-1, -2),
                   "RR": (-1, 0),
                   "FX": (1, 1),
                   "RX": (-1, -1),
                   "XF": (0, -1),
                   "XR": (0, 1),
                   "XX": (0, 0)}
        # unzip theta and rho into separate lists
        r_list_t, r_list_r = zip(*results.values())
        r_list_t = [x * step_multiplier[0] for x in list(r_list_t)]
        r_list_r = [x * step_multiplier[1] for x in list(r_list_r)]
        
        # FF
        self.motors.theta_count = 0
        self.motors.rho_count = 0
        self.planner._play_both_axis_step((direction.FORWARD, direction.FORWARD), (True, True))
        self.assertEqual(self.motors.theta_count, r_list_t[0])
        self.assertEqual(self.motors.rho_count, r_list_r[0])
        # FR
        self.motors.theta_count = 0
        self.motors.rho_count = 0
        self.planner._play_both_axis_step((direction.FORWARD, direction.BACKWARD), (True, True))
        self.assertEqual(self.motors.theta_count, r_list_t[1])
        self.assertEqual(self.motors.rho_count, r_list_r[1])
        # RF
        self.motors.theta_count = 0
        self.motors.rho_count = 0
        self.planner._play_both_axis_step((direction.BACKWARD, direction.FORWARD), (True, True))
        self.assertEqual(self.motors.theta_count, r_list_t[2])
        self.assertEqual(self.motors.rho_count, r_list_r[2])
        # RR
        self.motors.theta_count = 0
        self.motors.rho_count = 0
        self.planner._play_both_axis_step((direction.BACKWARD, direction.BACKWARD), (True, True))
        self.assertEqual(self.motors.theta_count, r_list_t[3])
        self.assertEqual(self.motors.rho_count, r_list_r[3])
        # FX
        self.motors.theta_count = 0
        self.motors.rho_count = 0
        self.planner._play_both_axis_step((direction.FORWARD, direction.FORWARD), (True, False))
        self.assertEqual(self.motors.theta_count, r_list_t[4])
        self.assertEqual(self.motors.rho_count, r_list_r[4])
        # RX
        self.motors.theta_count = 0
        self.motors.rho_count = 0
        self.planner._play_both_axis_step((direction.BACKWARD, direction.BACKWARD), (True, False))
        self.assertEqual(self.motors.theta_count, r_list_t[5])
        self.assertEqual(self.motors.rho_count, r_list_r[5])
        # XF
        self.motors.theta_count = 0
        self.motors.rho_count = 0
        self.planner._play_both_axis_step((direction.FORWARD, direction.FORWARD), (False, True))
        self.assertEqual(self.motors.theta_count, r_list_t[6])
        self.assertEqual(self.motors.rho_count, r_list_r[6])
        # XR
        self.motors.theta_count = 0
        self.motors.rho_count = 0
        self.planner._play_both_axis_step((direction.BACKWARD, direction.BACKWARD), (False, True))
        self.assertEqual(self.motors.theta_count, r_list_t[7])
        self.assertEqual(self.motors.rho_count, r_list_r[7])
        # XX
        self.motors.theta_count = 0
        self.motors.rho_count = 0
        self.planner._play_both_axis_step((direction.FORWARD, direction.FORWARD), (False, False))
        self.assertEqual(self.motors.theta_count, r_list_t[8])
        self.assertEqual(self.motors.rho_count, r_list_r[8])

    def test_play_move(self):
        instructions = {
            'directions': (direction.FORWARD, direction.FORWARD),
            'axis_steps_list': [(True, True), (False, False), (True, True)]
        }
        # Theta axis 2 * AXIS_GEAR_RATIO_T
        # Rho axis steps 2 * AXIS_GEAR_RATIO_R + (Theta steps * -1)
        results = (12,0)
        self.motors.theta_count = 0
        self.motors.rho_count = 0
        self.planner.play_move(instructions)
        self.assertEqual(self.motors.theta_count, results[0])
        self.assertEqual(self.motors.rho_count, results[1])

        instructions = {
            'directions': (direction.FORWARD, direction.BACKWARD),
            'axis_steps_list': [(True, True), (False, False), (True, True)]
        }
        # Theta axis 2 * AXIS_GEAR_RATIO_T
        # Rho axis steps -2 * AXIS_GEAR_RATIO_R + (Theta steps * -1)
        results = (12,-4)
        self.motors.theta_count = 0
        self.motors.rho_count = 0
        self.planner.play_move(instructions)
        self.assertEqual(self.motors.theta_count, results[0])
        self.assertEqual(self.motors.rho_count, results[1])

        instructions = {
            'directions': (direction.BACKWARD, direction.FORWARD),
            'axis_steps_list': [(True, True), (False, False), (True, True)]
        }
        # Theta axis -2 * AXIS_GEAR_RATIO_T
        # Rho axis steps 2 * AXIS_GEAR_RATIO_R + (Theta steps * -1)
        results = (-12,4)
        self.motors.theta_count = 0
        self.motors.rho_count = 0
        self.planner.play_move(instructions)
        self.assertEqual(self.motors.theta_count, results[0])
        self.assertEqual(self.motors.rho_count, results[1])

        # Just theta
        instructions = {
            'directions': (direction.FORWARD, direction.FORWARD),
            'axis_steps_list': [(True, False), (False, False), (True, False)]
        }
        # Theta axis 2 * AXIS_GEAR_RATIO_T
        # Rho axis steps 2 * AXIS_GEAR_RATIO_R + (Theta steps * -1)
        results = (12,-2)
        self.motors.theta_count = 0
        self.motors.rho_count = 0
        self.planner.play_move(instructions)
        self.assertEqual(self.motors.theta_count, results[0])
        self.assertEqual(self.motors.rho_count, results[1])

        # Just rho
        instructions = {
            'directions': (direction.FORWARD, direction.FORWARD),
            'axis_steps_list': [(False, True), (False, False), (False, True)]
        }
        results = (0,2)
        self.motors.theta_count = 0
        self.motors.rho_count = 0
        self.planner.play_move(instructions)
        self.assertEqual(self.motors.theta_count, results[0])
        self.assertEqual(self.motors.rho_count, results[1])

if __name__ == '__main__':
    unittest.main()
