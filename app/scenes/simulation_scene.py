from manimlib.imports import *
from app.modules.simulation import Simulation


class SimulationScene(Scene):
    def setup(self):
        self._add_simulation()

    def construct(self):
        self.wait(5)

    def _add_simulation(self):
        self.simulation = Simulation(scene=self)

        self.add(self.simulation)
