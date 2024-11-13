import random


class FlightSimulator:
    """
    Plane course correction simulator
    """
    def __init__(self, tilt_correction=0, orientation=0):
        self.orientation = orientation
        self.tilt_correction = tilt_correction

        self.run_simulation()

    """
    Runs the simulation
    """
    def run_simulation(self):
        print("Press CTRL+C to stop the simulation")
        try:
            while True:
                self._simulation_step()
        except KeyboardInterrupt:
            pass

    """
    Single simulation step
    """
    def _simulation_step(self):
        self.orientation += self.tilt_correction

        self.orientation += self._generate_random_angle(self, 2.0)
        self.tilt_correction = -self.orientation
        self._print_stats()

    """
    Prints the plane stats
    """
    def _print_stats(self):
        print(f"Plane orientation: {self.orientation}, plane tilt correction: {self.tilt_correction}")

    """
    Generates a random gaussian angle (turbulence)
    """
    @staticmethod
    def _generate_random_angle(self, rate_of_correction) -> float:
        return random.gauss(0, 2 * rate_of_correction)


if __name__ == '__main__':
    flight_sim = FlightSimulator()
