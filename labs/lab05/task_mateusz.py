import random
import logging
from time import sleep


class Plane:
    def __init__(self, max_tilt):
        self.max_tilt = max_tilt
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self._logger = logging.getLogger(__name__)

    def create_new_values(self):
        Roll_axis = random.gauss(0, 2 * self.max_tilt)
        Yaw_axsis = random.gauss(0, 2 * self.max_tilt)
        Pitch_axsis = random.gauss(0, 2 * self.max_tilt)
        yield Roll_axis, Yaw_axsis, Pitch_axsis

    def apply_turbulence(self):
        generator = self.create_new_values()
        roll, yaw, pitch = next(generator)
        if abs(roll) > 0.5 or abs(yaw) > 0.5 or abs(pitch) > 0.5:
            self._logger.warning("The turbulance were detected")
        if abs(roll) > 60 or abs(yaw) > 60 or abs(pitch) > 60:
            self._logger.warning("plane is falling to fast! No way of getting back on track!")
        return roll, yaw, pitch

    def correct(self, roll_axis, yaw_axis, pitch_axis):
        original_values = (roll_axis, yaw_axis, pitch_axis)
        corrected_values = (0, 0, 0)
        self._logger.info(f"Correcting the track from {original_values} to {corrected_values}")
        return corrected_values

    def simulate(self):
        try:
            while (True):
                roll, yaw, pitch = self.apply_turbulence()
                self.correct(roll, yaw, pitch)
                sleep(1)
        except KeyboardInterrupt:
            self._logger.info("\n\nSimulation stopped by user\n")


if __name__ == "__main__":
    easyjet12 = Plane(30)
    easyjet12.simulate()


