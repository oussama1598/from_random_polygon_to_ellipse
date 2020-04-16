from manimlib.imports import *


class OutroScene(Scene):
    def construct(self):
        outro_text = VGroup(
            TextMobject('Thanks for watching.'),
            TextMobject('Hope you liked it.')
        )

        outro_text.arrange(direction=DOWN)

        self.play(
            FadeIn(outro_text),
        )
        self.wait(.5)
        self.play(
            FadeOut(outro_text),
        )
