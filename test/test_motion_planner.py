import unittest
import sys
sys.path.insert(0, "../src/")
from motion_planner import motion_planner

class TestConstants(unittest.TestCase):
    planner = None
    
    def setUp(self):
        self.planner = motion_planner(None)
    
    def test_motor_steps_per_time_step(self):
        result = self.planner._motor_steps_per_time_step(1, 2, 2)
        self.assertEqual(1, result)
        result = self.planner._motor_steps_per_time_step(0.5, 0.0174533, 0.0174533)
        self.assertEqual(0.5, result)
        result = self.planner._motor_steps_per_time_step(0.5, 0.5, 1)
        self.assertEqual(1, result)
        # exception case, result >1
        self.assertRaises(Exception, self.planner._motor_steps_per_time_step, 1, 0.5, 1)

if __name__ == '__main__':
    unittest.main()