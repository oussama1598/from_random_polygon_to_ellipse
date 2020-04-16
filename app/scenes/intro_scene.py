from manimlib.imports import *
from app.modules.text_scene import TextScene


class IntroScene(TextScene):
    CONFIG = {
        'title': 'From Random Polygon to an ellipse',
        'text_sets': [
            [
                {'text': 'While browsing Twitter, as usual, I came across a very fascinating animation.'},
                {'text': 'The transformation of a polygon with random vertices into an ellipse.', 'color': YELLOW},
                {'text': 'Upon further digging, I found more details about this incredible phenomenon.'},
                {'text': 'I was able to recreate the animation.'}
            ],
            [
                {'text': 'The animation was created using a very simple yet incredible algorithm.'},
                {'text': 'Take a polygon with random vertices, find the mid-points of its sides,'},
                {'text': 'and use these to create a new polygon.'},
                {'text': 'repeat these steps and an ellipse will eventually form!'}
            ],
            [
                {'text': 'Let you enjoy the animation.'}
            ]
        ]
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setup(self):
        super().setup()

        self._construct_video_title()

    def construct(self):
        self.play(
            FadeIn(
                self.video_title,
            )
        )

        self.wait(.5)

        self.play(
            UpdateFromAlphaFunc(
                self.video_title,
                lambda obj, a: obj.move_to(
                    straight_path(np.zeros(3), .8 * TOP, a)
                )
            )
        )

        super().construct()

        self.play(
            UpdateFromAlphaFunc(
                self.video_title,
                lambda obj, a: obj.move_to(
                    straight_path(.8 * TOP, np.zeros(3),  a)
                )
            )
        )

        self.play(
            FadeOut(self.video_title)
        )

    def _construct_video_title(self):
        self.video_title = TextMobject(self.title)

        self.video_title.set_fill(RED)
