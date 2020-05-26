import os
import subprocess
from itertools import cycle
from manimlib.imports import *
from from_rahul.ninja import Ninja


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

    def end_blink(self):
        self.clear_updaters()
        self.set_fill(opacity=1)


class Type(Animation):
    CONFIG = {
        "suspend_mobject_updating": False,
        "int_func": np.floor,
        "rate_func": linear,
        "run_time": None,
    }

    def __init__(self, mobjects, cursor, **kwargs):
        self.all_submobs = []
        self.positions = []
        max_width = 0
        for mobject in mobjects.submobjects:
            for subobject in mobject.submobjects:
                max_width = max(max_width, subobject.get_width())
                x = subobject.get_x()
                self.positions.append((len(self.all_submobs), x, mobject.get_y()))
                self.all_submobs.append(subobject)
                x += subobject.get_width()
            self.positions.append((len(self.all_submobs), x, mobject.get_y()))
            self.positions.append(self.positions[-1])
            self.positions.append(self.positions[-1])
        self.gap = max_width / 3
        self.cursor = cursor
        super().__init__(mobjects, **kwargs)
        self.run_time = self.run_time or len(self.positions)/7

    def interpolate_mobject(self, alpha):
        n_submobs = len(self.positions)
        index = int(self.int_func(alpha * n_submobs))
        self.update_submobject_list(index)

    def update_submobject_list(self, index):
        last_idx = max(0, index - 1)
        idx, x, y = self.positions[last_idx]
        self.cursor.set_x(x + self.gap).set_y(y)
        self.mobject.submobjects = self.all_submobs[:idx] + [self.cursor]


class CodeMobject(TexMobject):
    CONFIG = {
        "alignment": "\\centering",
        "arg_separator": " ",
    }

    def get_indentation(self, string):
        for i, c in enumerate(string):
            if c != ' ':
                return i
        return 0

    def get_indexes(self, string):
        result, idx = [], 0
        for i, c in enumerate(string):
            if c != ' ':
                result.append(idx)
                idx += 1
            else:
                result.append(-1)
        # print(string, result)
        return result

    KEYWORDS = set(("False await else import pass None break except in raise True class" \
        " finally is return and continue for lambda try as def from nonlocal while" \
        " assert del global not with async elif if or yield").split())
    KEYWORD_COLOR = "#ffffaf"

    def set_color(self, obj, code):
        indexes = self.get_indexes(code)
        for key in self.KEYWORDS:
            idx, n = code.find(key), len(key)
            if idx >= 0 and (idx == 0 or code[idx - 1] == ' ') \
                and (idx + n < len(code) or code[idx + n] == ' '):
                for i in range(idx, idx + n):
                    obj.submobjects[indexes[i]].set_color(color=self.KEYWORD_COLOR)
        # print(words)

    def __init__(self, *code_string, **kwargs):
        text_string = []
        indentations = []
        for code in code_string:
            text = code.replace("'", "\\textquotesingle ")
            text_string.append("\\texttt{" + text + "}")
            indentations.append(self.get_indentation(code))
            # print(indentations[-1])
        super().__init__(*text_string, **kwargs)
        self.arrange_submobjects(DOWN, aligned_edge=LEFT)
        width = max([max([y.get_width() for y in x.submobjects]) for x in self.submobjects])
        # print('self.submobjects', len(self.submobjects))
        for obj, ind, code in zip(self.submobjects, indentations, code_string):
            # print(len(obj.submobjects), obj.tex_string)
            # print(code, max(a) if a else 0)
            # print(len(obj.submobjects), max(self.get_indexes(code_string[ind])))
            obj.set_x(obj.get_x() + width*ind)
            # self.set_color(obj, code)


def RunCode(self: AdvancedScene, code: CodeMobject, sequence, gap=0.2, corner=0.2, color=WHITE):
    def Rect(obj):
        h = max(obj.get_height() + gap, corner*2.5)
        w = max(obj.get_width() + gap, corner*2.5)
        rect = RoundedRectangle(width=w, height=h, corner_radius=corner).move_to(obj)
        rect.set_stroke(width=0).set_fill(color=color, opacity=0.5)
        return rect

    rect = Rect(code.submobjects[sequence[0]])
    self.play(GrowFromCenter(rect))
    for idx in sequence:
        animations = []
        if isinstance(idx, list):
            animations = idx[1:]
            idx = idx[0]
        rect1 = Rect(code.submobjects[idx])
        self.play(*([ReplacementTransform(rect, rect1)] + animations))
        rect = rect1
    return rect


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
        self.ninja = None
        self.ss_count = 0
        super().__init__(**kwargs)
        self.count = 0
        path = self.file_writer.get_movie_file_path()
        self.base_path = path[:path.rfind('.')]

    def create_ninja(self, *args, **kwargs) -> Ninja:
        corner = kwargs.pop('corner', DR)
        edge = kwargs.pop('edge', None)
        self.ninja = Ninja(*args)
        if edge is not None:
            self.ninja.to_edge(edge)
        elif corner is not None:
            self.ninja.to_corner(corner)
        return self.ninja

    def change_ninja(self, *args, **kwargs):
        if self.ninja:
            old = self.ninja
            self.create_ninja(*args, **kwargs)
            return ReplacementTransform(old, self.ninja)

    def get_reactions(self, **kwargs):
        reactions = kwargs.pop('reactions', None)
        if reactions is None:
            return cycle(['happy'])
        elif isinstance(reactions, str):
            return cycle([reactions])
        elif isinstance(reactions, list):
            return cycle(reactions)
        return reactions

    def show_heading(self, heading, **kwargs):
        question = kwargs.pop('question', None)
        animation = kwargs.pop('animation', None)
        scale = kwargs.pop('scale', None)
        sc = kwargs.pop('screenshot', None)
        reaction = self.get_reactions(**kwargs)

        if self.ninja is None:
            ninja = self.create_ninja(next(reaction))
            self.play(animation(ninja)) if animation else self.add(ninja)
        else:
            self.play(self.change_ninja(next(reaction)))

        h = TextMobject(heading, color=WHITE)
        if scale: h.scale(scale)
        h.to_corner(UL, buff=1)
        hu = Underline(h)

        if question:
            bubble = self.ninja.get_bubble()
            self.play(self.change_ninja(next(reaction)), Write(bubble))
            sc.save() if sc else None
            q = TextMobject(question, color=BLACK)
            bub = bubble.submobjects[3]
            q.scale(0.9 * bub.get_width() / q.get_width())
            if q.get_height() > 0.6*bub.get_height():
                q.scale(0.6 * bub.get_height() / q.get_height())
            q.move_to(bub.get_center())
            self.play(Write(q))
            self.wait()
            self.play(ReplacementTransform(q, h), FadeOut(bubble))
        else:
            q = TextMobject(heading, color=WHITE)
            q.scale(10 / q.get_width())
            if q.get_height() > 3:
                q.scale(3 / q.get_height())
            self.play(Write(q))
            self.play(ReplacementTransform(q, h))

        self.play(self.change_ninja(next(reaction)), FadeIn(hu))
        return h, hu

    def define_word(self, word, lines, **kwargs):
        sc = kwargs.pop('screenshot', None)
        reactions = self.get_reactions(**kwargs)
        fade = kwargs.pop('fade', False)
        kwargs['screenshot'] = sc
        kwargs['reactions'] = reactions

        h, hu = self.show_heading(word, **kwargs)

        w = TextMobject(word)
        info = VGroup(*[TextMobject(line) for line in lines])
        info.arrange_submobjects(DOWN, aligned_edge=LEFT, buff=1/len(lines))
        info.add_background_rectangle(buff=0.5)
        for x in info:
            self.play(Write(x))

        sc.save() if sc else None
        self.play(self.change_ninja(next(reactions)))
        leaving_objects = [h, hu, info]
        if not fade:
            return leaving_objects
        leaving_objects.append(self.ninja) if fade else None
        self.play(*[FadeOut(x) for x in leaving_objects])

    def create_slide(self, heading, points, **kwargs):
        # TODO: Use show_heading
        question = kwargs.pop('question', None)
        animation = kwargs.pop('animation', None)
        bullets = kwargs.pop('bullets', True)
        gap = kwargs.pop('gap', None)
        fade = kwargs.pop('fade', False)
        heading_scale = kwargs.pop('heading_scale', 4)
        sc = kwargs.pop('screenshot', None)
        reaction = cycle(kwargs.pop('reactions', ['happy']))

        ninja = self.create_ninja(next(reaction))
        if animation:
            self.play(animation(ninja))
        else:
            self.add(ninja)

        h = TextMobject(heading, color=WHITE)
        if h.get_width() < heading_scale:
            s = heading_scale / h.get_width()
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
            q = TextMobject(heading)
            q.scale(8 / q.get_width())
            if q.get_height() > 3:
                q.scale(3 / q.get_height())
            self.play(Write(q))
            sc.save() if sc else None
            self.play(ReplacementTransform(q, h))
            # self.play(FadeIn(h))

        self.play(self.change_ninja(next(reaction)), FadeIn(hu))

        prefix = "$\\bullet$ " if bullets else ""
        info = VGroup(*[TextMobject(prefix + txt) for txt in points])
        if not gap:
            gap = 9.29 * (len(points) ** -1.68)
            print('gap', gap)
        info.arrange_submobjects(DOWN, aligned_edge=LEFT, buff=gap)
        lt = np.array([h.get_coord(0, direction=LEFT), hu.get_coord(1, direction=DOWN) - 0.3])
        rb = np.array([self.ninja.get_coord(0, direction=LEFT), self.ninja.get_coord(1, direction=DOWN)])
        if (rb[0] - lt[0]) < info.get_width():
            s = (rb[0] - lt[0]) / info.get_width()
            print('points scale width', s)
            info.scale(s)
        if (lt[1] - rb[1]) < info.get_height():
            s = (lt[1] - rb[1]) / info.get_height()
            print('points scale height', s)
            info.scale(s)
        center_x, center_y = (lt + rb) / 2
        info.set_x(center_x).set_y(center_y)

        for txt in info.submobjects:
            self.play(Write(txt)) # , run_time=len(txt.tex_strings[0]) / 20))
            sc.save() if sc else None

        self.play(self.change_ninja(next(reaction)))
        leaving_objects = [h, hu] + info.submobjects
        leaving_objects.append(self.ninja) if fade else None
        self.play(*[FadeOut(x) for x in leaving_objects])

    def show_code(self, program, split='vertical'):
        result = subprocess.run(['python', '-c', program], stdout=subprocess.PIPE)
        print(result.stdout.decode() + '▌')

# 3 - 1.3
# 4 - 1
# 5 - 0.7
# 6 - 0.5
# 7 - 0.3