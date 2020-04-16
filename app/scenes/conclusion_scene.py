from manimlib.imports import *
from app.modules.text_scene import TextScene


class ConclusionScene(TextScene):
    CONFIG = {
        'text_sets': [
            [
                {'text': 'As you can see the polygon, after some amount of iterations,'},
                {'text': 'eventually turned into an ellipse.'},
                {'text': 'For more details and resources check the video\'s description.'},
            ]
        ]
    }
