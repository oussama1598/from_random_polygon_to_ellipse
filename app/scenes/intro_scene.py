from manimlib.imports import *


class IntroScene(Scene):
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
            ]
        ],
        'time_between_text_sets': 2,
    }

    def setup(self):
        self._construct_video_title()
        self._construct_video_description()

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

        for text_set in self.text_sets_objects:
            for line in text_set:
                self.play(
                    AddTextWordByWord(line)
                )

            self.wait(self.time_between_text_sets)
            self.play(
                FadeOut(text_set)
            )

        self.play(
            FadeOut(self.video_title),
            FadeOut(self.text_sets_objects)
        )

    def _construct_video_title(self):
        self.video_title = TextMobject(self.title)

        self.video_title.set_fill(RED)

    def _construct_video_description(self):
        self.text_sets_objects = VGroup()

        for text_set in self.text_sets:
            text_set_object = VGroup()

            for line in text_set:
                text_color = WHITE if not 'color' in line else line['color']
                text_line = TextMobject(line['text'])

                text_line.scale(.8)
                text_line.set_fill(text_color)

                text_set_object.add(text_line)

            text_set_object.arrange(direction=DOWN)
            self.text_sets_objects.add(text_set_object)

        self.text_sets_objects.set_width(FRAME_WIDTH - 2)
