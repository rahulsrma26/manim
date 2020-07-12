from manimlib.imports import *


class Type(Animation):
    CONFIG = {
        "suspend_mobject_updating": False,
        "int_func": np.floor,
        "rate_func": linear,
        "run_time": None,
    }

    def __init__(self, mobjects, cursor=None, **kwargs):
        self.speed = kwargs.pop('speed', 10)
        self.all_submobs = []
        self.positions = []
        max_width = 0
        # print('mobjects.submobjects', len(mobjects.submobjects))
        for mobject in mobjects.submobjects:
            x = None
            for subobject in mobject.submobjects:
                if isinstance(subobject, VMobjectFromSVGPathstring):
                    max_width = max(max_width, subobject.get_width())
                    x = subobject.get_x()
                    self.positions.append((len(self.all_submobs), x, mobject.get_y()))
                    self.all_submobs.append(subobject)
                    x += subobject.get_width()
            if x:
                self.positions.append((len(self.all_submobs), x, mobject.get_y()))
                self.positions.append(self.positions[-1])
                self.positions.append(self.positions[-1])
        # print('len', len(self.positions))
        self.gap = max_width / 3
        self.cursor = cursor
        super().__init__(mobjects, **kwargs)
        self.run_time = self.run_time or len(self.positions)/self.speed

    def interpolate_mobject(self, alpha):
        n_submobs = len(self.positions)
        index = int(self.int_func(alpha * n_submobs))
        self.update_submobject_list(index)

    def update_submobject_list(self, index):
        last_idx = max(0, index - 1)
        idx, x, y = self.positions[last_idx]
        display_objs = self.all_submobs[:idx]
        if self.cursor:
            self.cursor.set_x(x + self.gap).set_y(y)
            display_objs.append(self.cursor)
        self.mobject.submobjects = display_objs
