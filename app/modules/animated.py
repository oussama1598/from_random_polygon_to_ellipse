from manimlib.imports import VGroup


class Animated(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.animations = []

        self.add_updater(lambda obj, dt: obj._update_animations())

    def _update_animations(self):
        if len(self.animations) == 0:
            self.is_animating = False
            return

        animation = self.animations[0]

        for anim in animation:
            if anim.start_time == None:
                anim.begin()
                anim.start_time = self.time

            progress = (self.time - anim.start_time) / anim.run_time

            print(progress)

            if progress > 1:
                self.remove_animation(animation)
                return

            anim.interpolate(progress)

    def add_animation(self, animation):
        self.is_animating = True

        for anim in animation:
            anim.suspend_mobject_updating = False
            anim.start_time = None

        self.animations.append(animation)

    def remove_animation(self, animation):
        for anim in animation:
            anim.update(1)
            anim.finish()

        self.animations.remove(animation)
