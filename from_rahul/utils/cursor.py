from manimlib.imports import *


class Cursor(Rectangle):
    CONFIG = {
        "stroke_width": 0,
        "opacity": 1,
    }

    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs)
        max_height, max_width = 0, 0
        for sub in mobject.submobjects:
            max_height = max(max_height, sub.get_height())
            for subsub in sub.submobjects:
                if isinstance(subsub, VMobjectFromSVGPathstring):
                    max_width = max(max_width, subsub.get_width())
        Rectangle.__init__(
            self,
            height=max_height,
            width=max_width/3,
            **kwargs
        )
        self.set_fill(color=mobject.get_color(), opacity=1)

    def start_blink(self):
        def blink(m: Mobject, dt):
            m.counter += 5*dt
            v = math.sqrt((1 + math.sin(m.counter)) / 2)
            m.set_fill(opacity=v)
        self.counter = 0
        self.add_updater(blink)

    def stop_blink(self):
        self.clear_updaters()
        self.set_fill(opacity=1)
