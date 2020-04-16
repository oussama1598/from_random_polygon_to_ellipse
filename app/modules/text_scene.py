from manimlib.imports import *


class TextScene(Scene):
    CONFIG = {
        'text_sets': [
            [
                {'text': 'Random text', 'color': YELLOW},
            ]
        ],
        'time_between_text_sets': 2,
    }

    def _construct_text_sets(self):
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

    def setup(self):
        self._construct_text_sets()

    def construct(self):
        for text_set in self.text_sets_objects:
            for line in text_set:
                self.play(
                    Write(line, stroke_width=1)
                )

            self.wait(self.time_between_text_sets)
            self.play(
                FadeOut(text_set)
            )
            self.text_sets_objects.remove(text_set)
