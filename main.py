from app.scenes.simulation_scene import SimulationScene
from app.scenes.intro_scene import IntroScene
from app.scenes.conclusion_scene import ConclusionScene
from app.scenes.outro_scene import OutroScene


class IntroScene(IntroScene):
    pass


class SimulationScene(SimulationScene):
    pass


class ConclusionScene(ConclusionScene):
    pass


class OutroScene(OutroScene):
    pass


SCENES = [
    IntroScene,
    SimulationScene,
    ConclusionScene,
    OutroScene
]
