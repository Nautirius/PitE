# Your task is to get the code from your friend
# copy the code of your friend, preferably as separate files to this repository
# Test all of the methods in their code, or at least 10 unittest tests (that make sense).
# Your test must be runnable with the command `python -m unittest task`
# Write down the address of your friends repo here:
# 
# Imported from: ADRESS_LINK_HERE
#

# change the name of OTHER_CODE, to the code that you imported
import unittest
from task_mateusz import Plane


class TestPlane(unittest.TestCase):
    def test_create_new_values(self):
        plane = Plane(30)
        new_values = plane.create_new_values()
        self.assertIsNotNone(new_values, "The values are None")

    def test_apply_turbulence_returns_not_none(self):
        plane = Plane(30)
        turbulence = plane.apply_turbulence()
        self.assertIsNotNone(turbulence, "The value is None")

    def test_correct(self):
        plane = Plane(30)
        roll, yaw, pitch = plane.apply_turbulence()
        corrected_values = plane.correct(roll, yaw, pitch)
        self.assertEqual(corrected_values, (0, 0, 0), "The corrected values are not valid")

    def test_apply_turbulence_returns_not_zeros(self):
        plane = Plane(30)
        turbulence = plane.apply_turbulence()
        self.assertNotEqual(turbulence, (0, 0, 0), "The generated turbulence is not valid")

    def test_init(self):
        max_tilt = 30
        plane = Plane(max_tilt)
        self.assertEqual(plane.max_tilt, max_tilt, "The init values are not correct")


if __name__ == '__main__':
    unittest.main()



