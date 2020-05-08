import os
from itertools import cycle
from manimlib.imports import *
from rahul.ninja import Ninja


class VSColors:
    function = "#dcdcaa"
    variable = "#e4e4d9"
    string = "#de824b"
    keywords = "#569cca"
    comments = "#72b975"
    kwargs = "#9cdcfe"
    class_name = "#3ac9b0"


class MCOLORS:
    PeekabooPeach = "#F9A96A"
    WildWasabi = "#8CA65F"
    PoolParty = "#96D2C8"
    PerfectPlum = "#906979"
    FlatTeal = "#356272"


class ExplainableTextObject:
    def __init__(self, text, hint, direction=DOWN):
        self.text = TextMobject(text)
        self.text.scale(1.5)
        self.braces = Brace(self.text, direction=direction).set_color(VSColors.class_name)
        self.hint = self.braces.get_text(hint).set_color(VSColors.comments)
        self.obj = Group(self.text, self.braces, self.hint)

        self.braces.add_updater(lambda d: d.next_to(self.text, direction))
        self.hint.add_updater(lambda d: d.next_to(self.braces, direction))



class ScreenGrabber:
    def __init__(self, scene: Scene):
        self.scene = scene
        self.count = 0
        path = scene.file_writer.get_movie_file_path()
        self.base = path[:path.rfind('.')]

    def save(self):
        filepath = f"{self.base}_{self.count:03}.png"
        self.scene.get_image().save(filepath)
        print(f"Saved screenshot at {filepath}")
        self.count += 1


class AdvancedScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = 0
        path = self.file_writer.get_movie_file_path()
        self.base_path = path[:path.rfind('.')]
        self.ss_count = 0
        self.ninja = None

    def create_ninja(self, *args):
        self.ninja = Ninja(*args).to_corner(DR)
        return self.ninja

    def change_ninja(self, *args):
        if self.ninja:
            old = self.ninja
            self.ninja = Ninja(*args).to_corner(DR)
            return ReplacementTransform(old, self.ninja)

    def create_slide(self, heading, points, **kwargs):
        question = kwargs.pop('question', None)
        animation = kwargs.pop('animation', None)
        sc = kwargs.pop('screenshot', None)
        reaction = cycle(kwargs.pop('reactions', ['happy']))

        ninja = self.create_ninja(next(reaction))
        if animation:
            self.play(animation(ninja))
        else:
            self.add(ninja)

        h = TextMobject(heading, color=WHITE)
        if h.get_width() < 4:
            s = 5 / h.get_width()
            print('heading scale', s)
            h.scale(s)
        h.to_corner(UL, buff=1)
        hu = Underline(h)
        if question:
            bubble = self.ninja.get_bubble()
            self.play(self.change_ninja(next(reaction)), Write(bubble))
            q = TextMobject(question, color=BLACK)
            q.scale(0.9 * bubble.get_width() / q.get_width())
            q.move_to(bubble.submobjects[3].get_center())
            self.play(Write(q))
            sc.save() if sc else None
            self.play(ReplacementTransform(q, h), FadeOut(bubble))
        else:
            self.play(FadeIn(h))

        self.play(self.change_ninja(next(reaction)), FadeIn(hu))

        info = VGroup(*[TextMobject("$\\bullet$ " + txt) for txt in points])
        gap = 9.29 * (len(points) ** -1.68)
        info.arrange_submobjects(DOWN, aligned_edge=LEFT, buff=gap)
        lt = np.array([h.get_coord(0, direction=LEFT), hu.get_coord(1, direction=DOWN)])
        rb = np.array([self.ninja.get_coord(0, direction=LEFT), self.ninja.get_coord(1, direction=DOWN)])
        if (rb[0] - lt[0]) < info.get_width():
            s = (rb[0] - lt[0]) / info.get_width()
            print('points scale', s)
            info.scale(s)
        center_x, center_y = (lt + rb) / 2
        info.set_x(center_x).set_y(center_y)

        for txt in info.submobjects:
            self.play(Write(txt)) # , run_time=len(txt.tex_strings[0]) / 20))
            sc.save() if sc else None

        self.play(self.change_ninja(next(reaction)))
        self.play(*[FadeOut(x) for x in [info, h, hu]])

# 3 - 1.3
# 4 - 1
# 5 - 0.7
# 6 - 0.5
# 7 - 0.3