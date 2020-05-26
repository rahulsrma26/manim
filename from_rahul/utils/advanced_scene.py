from manimlib.imports import *
from itertools import cycle
from from_rahul.ninja import Ninja


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
        if not fade:
            return leaving_objects
        leaving_objects.append(self.ninja)
        self.play(*[FadeOut(x) for x in leaving_objects])
