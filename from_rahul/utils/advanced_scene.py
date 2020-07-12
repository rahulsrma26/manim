from manimlib.imports import *
from itertools import cycle
from from_rahul.ninja import Ninja
from from_rahul.utils.code_mobject import CodeMobject
from from_rahul.utils.type_animation import Type
from from_rahul.utils.cursor import Cursor
from from_rahul.utils.table import Table
from from_rahul.utils.colors import MCOLORS

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
    TRANSPARENT = {
        "camera_config": {
            "background_opacity": 0,
            "background_color": BLACK
        }
    }
    CONFIG = {
        "camera_config": {
            "background_color": MCOLORS.Background
        }
    }
    def __init__(self, **kwargs):
        self.check_code_dir()
        self.ninja = None
        self.ss_count = 0
        super().__init__(**kwargs)
        self.count = 0
        path = self.file_writer.get_movie_file_path()
        self.base_path = path[:path.rfind('.')]

    def check_code_dir(self):
        code_dir = os.path.join(consts.MEDIA_DIR, "code")
        if not os.path.isdir(code_dir):
            os.mkdir(code_dir)

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
        intro = kwargs.pop('intro', True)
        sc = kwargs.pop('screenshot', None)
        reaction = self.get_reactions(**kwargs)

        if self.ninja is None:
            ninja = self.create_ninja(next(reaction))
            self.play(animation(ninja)) if animation else self.add(ninja)
        else:
            self.play(self.change_ninja(next(reaction)))

        h = TextMobject(heading, color=WHITE)
        if scale:
            h.scale(scale)
        h.to_corner(UL, buff=1)
        hu = Underline(h)
        if not intro:
            self.play(Write(h), self.change_ninja(next(reaction)), FadeIn(hu))
            return h, hu

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
        speed = kwargs.pop('speed', None)
        reactions = self.get_reactions(**kwargs)
        fade = kwargs.pop('fade', False)
        kwargs['screenshot'] = sc
        kwargs['reactions'] = reactions

        h, hu = self.show_heading(word, **kwargs)

        w = TextMobject(word)
        info = VGroup(*[TextMobject(line) for line in lines])
        levels = np.linspace(hu.get_y() - 0.5 - info[0].get_height(), -3, len(lines), endpoint=False)
        for obj, y in zip(info, levels):
            obj.set_y(y - obj.get_height()/2)
            obj.set_x(obj.get_width()/2 + hu.get_corner(DL)[0])
        # info.arrange_submobjects(DOWN, aligned_edge=LEFT, buff=1/len(lines))
        info.add_background_rectangle(buff=0.5)
        mid = self.ninja.get_corner(UL)[0] - hu.get_left()[0]
        if info.get_width() > mid:
            info.scale(mid/info.get_width())
        info.move_to(hu, aligned_edge=LEFT).shift([0, -0.5 -info.get_height()/2, 0])
        for i, x in enumerate(info):
            if speed and i > 0:
                self.play(Write(x), run_time=len(lines[i - 1])/speed)
            else:
                self.play(Write(x))

        sc.save() if sc else None
        self.play(self.change_ninja(next(reactions)))
        leaving_objects = [h, hu, info]
        if not fade:
            return leaving_objects
        leaving_objects.append(self.ninja) if fade else None
        self.play(*[FadeOut(x) for x in leaving_objects])

    def define_function(self, word, lines, examples, **kwargs):
        sc = kwargs.pop('screenshot', None)
        example_scale = kwargs.pop('example_scale', 1)
        reactions = self.get_reactions(**kwargs)
        fade = kwargs.pop('fade', False)
        pause = kwargs.pop('pause', False)
        code_speed = kwargs.pop('code_speed', 15)
        output_speed = kwargs.pop('output_speed', 20)
        kwargs['screenshot'] = sc
        kwargs['reactions'] = reactions

        h, hu = self.show_heading(word, **kwargs)

        info = VGroup(*[TextMobject(line) for line in lines])
        info.arrange_submobjects(DOWN, aligned_edge=LEFT, buff=1/len(lines))
        info.add_background_rectangle(buff=0.5)
        info[0].stretch_to_fit_width(10)
        info.next_to(hu, DOWN, aligned_edge=LEFT)
        for x in info:
            self.play(Write(x))

        sc.save() if sc else None

        h1 = TextMobject("\\texttt{code}")
        h2 = TextMobject("\\texttt{output}")
        code, output, cursor = None, None, None
        if pause:
            obj = TextMobject('\\texttt{[Pause if you wanna take a closer look]}').scale(0.8).to_edge(DOWN)
            h.add(obj)
            self.play(FadeIn(obj))

        for example in examples:
            if code is not None:
                self.play(*[FadeOut(x) for x in [code, output, cursor, h1, h2]])
            code = CodeMobject(*example, execute=True).scale(example_scale)
            h1.next_to(info, DOWN, aligned_edge=LEFT)
            code.next_to(info, DOWN, aligned_edge=LEFT, buff=0.8)
            self.play(DrawBorderThenFill(code[0]), Write(h1))
            # self.play(Write(code[1]))
            codeG = VGroup(*code[2:])
            cursor = Cursor(codeG) #.stretch_to_fit_width(0.2)
            self.play(Type(codeG, cursor, speed=code_speed))
            cursor.start_blink()
            self.wait()
            # otxt = [f"\\texttt{x}" for x in code.output.decode('utf-8').split('\n')]
            otxt = code.output.decode('utf-8').split('\n')
            output = CodeMobject(*otxt, language='bash').scale(example_scale)
            # output = VGroup(TextMobject(*otxt).scale(example_scale))
            # output.add(RoundedRectangle(width=output[0].get_width(), height=code.get_height()))
            # output[0].move_to(output[1].get_corner(UL))
            vdiff = output[0].get_corner(UL) - output[2].get_corner(UL)
            output[0].stretch_to_fit_height(code[0].get_height())
            h2.next_to(info, DOWN, aligned_edge=RIGHT)
            output.next_to(info, DOWN, aligned_edge=RIGHT, buff=0.8)
            self.play(DrawBorderThenFill(output[0]), Write(h2))
            outputG = VGroup(*output[2:])
            outputG.move_to(output[0].get_corner(UL) - vdiff + np.array([outputG.get_width(),-outputG.get_height(),0])/2)
            self.play(Type(outputG, speed=output_speed))
            self.wait()
            cursor.stop_blink()
            self.wait()
            sc.save() if sc else None

        self.play(self.change_ninja(next(reactions)))
        self.wait()
        leaving_objects = [h, hu, info, code, output, cursor, h1, h2]
        if not fade:
            return leaving_objects
        leaving_objects.append(self.ninja) if fade else None
        self.play(*[FadeOut(x) for x in leaving_objects])

    def define_function_egs(self, word, lines, examples, **kwargs):
        sc = kwargs.pop('screenshot', None)
        example_scale = kwargs.pop('example_scale', 1)
        color_tf = kwargs.pop('color_tf', None)
        reactions = self.get_reactions(**kwargs)
        fade = kwargs.pop('fade', False)
        kwargs['screenshot'] = sc
        kwargs['reactions'] = reactions

        h, hu = self.show_heading(word, **kwargs)

        info = VGroup(*[TextMobject(line) for line in lines])
        info.arrange_submobjects(DOWN, aligned_edge=LEFT, buff=1/len(lines))
        info.add_background_rectangle(buff=0.5)
        if info[0].get_width() < 10:
            info[0].stretch_to_fit_width(10)
        info.next_to(hu, DOWN, aligned_edge=LEFT)
        for x in info:
            self.play(Write(x))
        sc.save() if sc else None
        self.wait()
        self.play(FadeOut(info))

        content = []
        for example in examples:
            tex = example.replace('\\', '$\\backslash$').replace('_', '\\_')
            print(example, tex)
            content.append([f"\\texttt{{{tex}}}", str(eval(example))])

        table = Table(content,
            # widths=[1, 0.5, 1, 2.5, 1.2, 0.7, 1, 2],
            useTex=False, align='ll', cgap=1)
        hdiff = info.get_corner(DL)[1] - self.ninja.get_corner(DL)[1]
        if table.get_height() > hdiff:
            table.scale(hdiff / table.get_height())
        table.next_to(hu, DOWN, aligned_edge=LEFT).set_x(0)
        if color_tf:
            for r, objs in enumerate(table.text_objects):
                color = MCOLORS.WildWasabi if content[r][color_tf] == 'True' else MCOLORS.PeekabooPeach
                objs[color_tf].set_color(color=color)
        for obj in table.submobjects:
            self.play(Write(obj), run_time=0.5)
        # self.play(Write(table), run_time=len(examples))

        pause = TextMobject('\\texttt{[Pause if you wanna take a closer look]}').scale(0.8).to_edge(DOWN)
        self.play(FadeIn(pause))
        self.play(self.change_ninja(next(reactions)))
        leaving_objects = [h, hu, pause, table]
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
        write_speed = kwargs.pop('write_speed', 15)
        reaction = cycle(kwargs.pop('reactions', ['happy']))

        if self.ninja is None:
            ninja = self.create_ninja(next(reaction))
            self.play(animation(ninja)) if animation else self.add(ninja)
        else:
            self.play(self.change_ninja(next(reaction)))

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
            if write_speed:
                self.play(Write(txt, run_time=len(txt.tex_strings[0])/write_speed))
            else:
                self.play(Write(txt))
            # self.play(Write(txt)) # , run_time=len(txt.tex_strings[0]) / 20))
            sc.save() if sc else None

        self.play(self.change_ninja(next(reaction)))
        leaving_objects = [h, hu] + info.submobjects
        if not fade:
            return leaving_objects
        leaving_objects.append(self.ninja)
        self.play(*[FadeOut(x) for x in leaving_objects])
