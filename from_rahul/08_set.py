#!/usr/bin/env python
import os
import subprocess
from manimlib.imports import *
# from manimlib.utils.rate_functions import linear
from from_rahul.ninja import Ninja
from from_rahul.extend import *
# from from_rahul.table import Table

DIR = os.path.dirname(os.path.abspath(__file__))
SDIR = os.path.join(DIR, 'svgs')

def get_boxes(text, **kwargs):
    scale = kwargs.pop('scale', 3)
    iscale = kwargs.pop('iscale', 1.6)
    width = kwargs.pop('width', 1.6)
    height = kwargs.pop('height', 2)
    corner_radius = kwargs.pop('corner_radius', 0.2)
    color = kwargs.pop('color', WHITE)
    ucolor = kwargs.pop('ucolor', MCOLORS.WildWasabi)

    boxes = VGroup()
    whole = TextMobject(text, color=color).scale(scale)
    # print(whole.set_z(-1))
    n = len(whole.submobjects[0])
    for i, txobj in enumerate(whole.submobjects[0]):
        txbox = RoundedRectangle(
            width=width, # fill_color="#202025",
            height=height, # fill_opacity=1.0,
            corner_radius=corner_radius)
        txobj.set_x(txbox.get_x())
        txidx = TextMobject(str(i), color=ucolor).scale(iscale)
        txidx.next_to(txbox, direction=DOWN)
        # txrid.next_to(txidx, direction=DOWN, aligned_edge=RIGHT)
        boxes.add(VGroup(txobj, txbox, txidx))
    boxes.arrange_submobjects()
    boxes.shift([-0.5, -0.4, 0])
    return whole, boxes

# python -m manim from_rahul\08_set.py ListSearch -pl
class ListSearch(AdvancedScene):
    def construct(self):
        self.play(FadeInFrom(self.create_ninja(), RIGHT))
        head, head_ul = self.show_heading('List', scale=2, reactions=['thinking'])
        code = TextMobject('\\texttt{[4,1,3,5,2]}').scale(2)
        code1 = TextMobject('\\texttt{4 1 3 5 2}').scale(2).shift([-0.01,.025,0])
        self.play(Type(code))
        self.play(*[FadeOut(x) for x in code[::2]])
        for x in code[::2]:
            self.remove(x)
        self.add(code1)
        self.play(*[FadeOut(x) for x in code[1::2]])
        text, string = get_boxes('41352')
        self.play(ReplacementTransform(code1, text))
        self.play(self.change_ninja('thinking'))
        self.play(*[DrawBorderThenFill(x[1]) for x in string])
        self.play(*[FadeIn(c[2]) for c in string])
        search_3 = TextMobject('\\texttt{Searching for 3').next_to(string, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Type(search_3))
        arrow = Arrow(start=[0,1.5,0], end=[0,0,0], stroke_width=10, max_stroke_width_to_length_ratio=100, max_tip_length_to_length_ratio=0.4)
        for i in range(3):
            if i:
                self.play(arrow.next_to, string[i][1], TOP, {"buff": 0.1})
            else:
                arrow.next_to(string[i][1], TOP, buff=0.1)
                self.play(FadeIn(arrow))
            self.play(Indicate(string[i][1]), Indicate(text[0][i]))
        self.play(FadeOut(arrow), self.change_ninja('happy'))
        self.play(FadeOut(search_3), self.change_ninja('thinking'))
        search_7 = TextMobject('\\texttt{Searching for 7').next_to(string, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Type(search_7))
        for i in range(5):
            if i:
                self.play(arrow.next_to, string[i][1], TOP, {"buff": 0.1})
            else:
                arrow.next_to(string[i][1], TOP, buff=0.1)
                self.play(FadeIn(arrow))
            self.play(Indicate(string[i][1]), Indicate(text[0][i]))
        self.play(FadeOut(arrow), self.change_ninja('sad'))
        self.play(FadeOut(search_7), FadeOut(text), FadeOut(string))
        self.play(FadeOut(head), FadeOut(head_ul), self.change_ninja('thinking'))


# python -m manim from_rahul\08_set.py Sets -pl
class Sets(AdvancedScene):
    def construct(self):
        # self.add(self.create_ninja('thinking'))
        head, head_ul = self.show_heading('Set', scale=2, reactions=['thinking'])
        boxes = VGroup(*[RoundedRectangle(width=1.2, height=1.5, corner_radius=0.2) for _ in range(10)])
        boxes.arrange_submobjects(buff=0).shift([0, 0.5, 0])
        self.play(Write(boxes), run_time=5)

        indices = VGroup()
        for i, box in enumerate(boxes):
            index = TextMobject(str(i), color=MCOLORS.WildWasabi).scale(1.5)
            index.next_to(box, direction=DOWN)
            indices.add(index)
        self.play(FadeIn(indices))

        occupied = [None] * 10
        def add(n):
            adding = TextMobject('Adding').to_corner(DL, buff=1.5).scale(1.5)
            num = TextMobject(f'\\texttt{{{n}}}', color=MCOLORS.BadYellow).next_to(adding, buff=0.5).scale(1.5)
            self.play(FadeIn(adding))
            self.play(Type(num))
            ul = Underline(num[len(str(n)) - 1])
            self.play(GrowFromCenter(ul))
            self.wait()
            for i in range(n % 10, 10):
                self.play(Indicate(boxes[i]))
                if occupied[i]:
                    self.play(WiggleOutThenIn(occupied[i][1]))
                else:
                    self.play(num.move_to, boxes[i])
                    occupied[i] = (n, num)
                    break
            self.play(FadeOut(ul), FadeOut(adding))

        def search(n):
            searching = TextMobject('Searching').to_corner(DL, buff=1.5).scale(1.5)
            num = TextMobject(f'\\texttt{{{n}}}', color=MCOLORS.BadYellow).next_to(searching, buff=0.5).scale(1.5)
            self.play(FadeIn(searching))
            self.play(Type(num))
            ul = Underline(num[len(str(n)) - 1])
            self.play(GrowFromCenter(ul))
            self.wait()
            for i in range(n % 10, 10):
                self.play(Indicate(boxes[i]))
                if occupied[i]:
                    self.play(Indicate(occupied[i][1]))
                    if occupied[i][0] == n:
                        self.play(Flash(boxes[i], flash_radius=0.8))
                        break
                else:
                    self.play(WiggleOutThenIn(boxes[i]))
                    break
            self.play(FadeOut(num), FadeOut(ul), FadeOut(searching))

        add(14)
        self.play(self.change_ninja('happy'))
        add(27)
        self.wait()
        add(33)
        self.play(self.change_ninja('thinking'))
        search(27)
        self.play(self.change_ninja('surprised'))
        search(55)
        self.play(self.change_ninja('thinking'))
        add(44)
        self.play(self.change_ninja('surprised'))
        search(44)
        self.play(self.change_ninja('thinking'))
        search(55)
        self.play(self.change_ninja('happy'))
        self.wait()
        nums = [x[1] for x in occupied if x]
        self.play(*[FadeOut(x) for x in nums + [head, head_ul, boxes, indices, self.ninja]])

# python -m manim from_rahul\08_set.py Intro -pl
class Intro(AdvancedScene):
    def construct(self):
        t = TextMobject("\\texttt{csglitz}").scale(2.5)
        w = Ninja("wave")
        c = Group(t, w).arrange_submobjects(RIGHT, buff=1)
        self.play(DrawBorderThenFill(w), Write(t))
        w.wave(self, 1)
        self.wait()
        n = self.create_ninja('wave').move_to(w)
        self.remove(w).add(n)
        self.play(FadeOut(t))
        self.play(n.to_corner, DR)
        self.play(self.change_ninja('thinking'))
        self.wait()
        self.play(self.change_ninja('happy'))

        leaving_objects = self.create_slide(
            "Topics on sets",
            [
                "Create, iterate, and membership operators",
                "set() constructor",
                "Adding and Removing elements",
                "Comparison operators",
                "Union, Intersection and other operations",
                "Unpacking and Set Comprehension",
            ],
            write_speed=35,
            reactions=['happy', 'thinking'])
        self.wait()
        leaving_objects.append(self.ninja)
        self.play(*[FadeOut(x) for x in leaving_objects])
        self.wait()

# python -m manim from_rahul\08_set.py Comparison -pl
class Comparison(AdvancedScene):
    def construct(self):
        sc = ScreenGrabber(self)
        operands = [
            ('set()', '{1}'),
            ('{1}', 'set()'),
            ('{1}', '{1, 2}'),
            ('{1, 2}', '{1}'),
            ('{1, 2}', '{1, 2}'),
            ('{1, 2}', '{3, 4}')]
        operators = [
            ('<', 'Less than', 'Returns true if left is a PROPER subset of right'),
            ('<=', 'Less than or Equal to', 'Returns true if left is a subset of right'),
            ('>', 'Greater than', 'Returns true if right is a PROPER subset of left'),
            ('>=', 'Greater than or Equal to', 'Returns true if right is a subset of left'),
            ('==', 'Equal to', 'Returns true only if both have exact same elements'),
            ('!=', 'Not equal to', 'Returns true if any of the elements is different'),
        ]

        h, hu = self.show_heading(
            "Comparison operators",
            animation=DrawBorderThenFill,
            scale=1, hbuff=0.7)

        des = TextMobject("These operators are based on set theory.").next_to(hu, direction=DOWN, aligned_edge=LEFT)
        self.play(Type(des))
        self.wait()

        def sf(s):
            s = s.replace('{', '\\{').replace('}', '\\}')
            return f'\\texttt{{{s}}}'

        texts = [[x, '..', y, '.....'] for (x, y) in operands]
        table = Table(
            [[sf(t) for t in row] for row in texts],
            widths=[1, 0.35, 1, 2.5],
            align='rrll', useTex=False
        ).shift([0,-0.6,0])
        self.play(Write(table), run_time=3)
        msg = TextMobject('\\texttt{[Pause if you wanna take a closer look]}').scale(0.7)
        msg.to_edge(DOWN)
        self.play(FadeIn(msg), self.change_ninja('thinking'))

        for op, txt, desc in operators:
            h1 = TextMobject(txt).scale(1.3).to_corner(UL, buff=0.7)
            hu1 = Underline(h1)
            self.play(ReplacementTransform(h, h1), ReplacementTransform(hu, hu1))
            des1 = TextMobject(desc).next_to(hu1, direction=DOWN, aligned_edge=LEFT)
            self.play(ReplacementTransform(des, des1))
            h, hu, des = h1, hu1, des1

            new_objs = []
            for i, (x, y) in enumerate(operands):
                k = i*4 + 1
                old_op = table.submobjects[k]
                old_tx = table.submobjects[k+2]
                new_op = TextMobject(f'${op}$').set_x(old_op.get_x()).set_y(old_op.get_y())
                rs = str(eval(f"{x} {op} {y}"))
                color = MCOLORS.WildWasabi if rs == 'True' else MCOLORS.PeekabooPeach
                new_tx = TextMobject(rs).set_y(old_tx.get_y()).set_color(color=color)
                new_tx.set_x(old_tx.get_x() - old_tx.get_width()/2 + new_tx.get_width()/2)
                new_objs.append((k, old_op, new_op))
                new_objs.append((k+2, old_tx, new_tx))

            self.play(*[ReplacementTransform(o, n) for _, o, n in new_objs])
            self.wait(duration=4)
            # sc.save()
            for i, o, n in new_objs:
                table.submobjects[i] = n

        self.play(self.change_ninja('happy'))
        self.play(*[FadeOut(x) for x in [h, hu, des, table, msg, self.ninja]])
        self.wait()

class IndicateFill(Transform):
    CONFIG = {
        "rate_func": there_and_back_with_pause,
        "scale_factor": 1,
    }
    # def __init__(self, mobject, target_mobject=None, **kwargs):
    #     super().__init__(mobject, target_mobject=target_mobject, **kwargs)
    def create_target(self):
        target = self.mobject.copy()
        target.scale_in_place(self.scale_factor)
        target.set_fill(
            color=WHITE,
            opacity=0.5,
        )
        return target

# python -m manim from_rahul\08_set.py Example -pl
class Example(AdvancedScene):
    CONFIG = CONFIG = {
        "camera_config": {
            "background_color": "#1e1e1e"
        }
    }
    def construct(self):
        nums = VGroup(*[TextMobject(str(i), color=MCOLORS.BadYellow).scale(1.5) for i in range(1,10)])
        nums[0].shift([-3.4, 1.8, 0])
        nums[8].shift([+3.4, 1.8, 0])
        nums[2].shift([+1.3, 1, 0])
        nums[3].shift([-1.3, 1, 0])
        nums[4].shift([+2.4, 0, 0])
        nums[5].shift([-2.4, 0, 0])
        nums[6].shift([+1.3, -1, 0])
        nums[7].shift([-1.3, -1, 0])
        self.play(DrawBorderThenFill(nums))
        rect = Rectangle(width=8, height=5)
        rect = VGroup(rect, TextMobject("n").scale(2).next_to(rect, direction=UP, aligned_edge=RIGHT))
        self.play(DrawBorderThenFill(rect))
        svg = SVGMobject(os.path.join(SDIR, 'sets.svg')).scale(1.8)
        # self.bring_to_back(svg)
        for obj in svg:
            obj.set_stroke(color=WHITE, width=0).set_fill(color=RED, opacity=0)
            # self.play(DrawBorderThenFill(obj))
        set_e, set_p, set_i, set_u, a_diff_b, b_diff_a = svg
        # self.play(DrawBorderThenFill(svg))
        # self.play(IndicateFill(rect))
        set_e.set_stroke(color=MCOLORS.WildWasabi, width=5)
        even = TextMobject("e").scale(2).next_to(set_e, direction=DOWN, aligned_edge=LEFT, buff=-0.5)
        self.play(DrawBorderThenFill(set_e), FadeIn(even))
        self.play(IndicateFill(set_e))
        self.wait()
        set_p.set_stroke(color=MCOLORS.PeekabooPeach, width=5)
        prime = TextMobject("p").scale(2).next_to(set_p, direction=DOWN, aligned_edge=RIGHT, buff=-0.5)
        self.play(DrawBorderThenFill(set_p), FadeIn(prime))
        self.play(IndicateFill(set_p))
        self.wait()
        self.play(IndicateFill(set_i), run_time=3)
        self.remove(set_i)
        self.wait()
        self.play(IndicateFill(set_u), run_time=3)
        self.remove(set_u)
        self.wait()
        self.play(IndicateFill(a_diff_b), run_time=3)
        self.remove(a_diff_b)
        self.wait()
        self.play(IndicateFill(b_diff_a), run_time=3)
        self.remove(b_diff_a)
        self.wait()
        self.play(IndicateFill(a_diff_b), IndicateFill(b_diff_a), run_time=3)
        self.remove(a_diff_b, b_diff_a)
        self.wait()

class Logo(AdvancedScene):
    def construct(self):
        t = TextMobject("\\texttt{csglitz}").scale(2.5)
        w = Ninja("wave")
        c = Group(t, w).arrange_submobjects(RIGHT, buff=1)
        self.play(DrawBorderThenFill(w), Write(t))
        w.wave(self, 1)
        self.wait()
        self.play(FadeOut(t), FadeOut(w))
        self.wait()


# python -m manim from_rahul\08_set.py Outro -pl
class Outro(AdvancedScene):
    def construct(self):
        # objs = self.define_word(
        #     "Practice Makes Progress",
        #     [
        #         "Links to the example source",
        #         "code and assignments are",
        #         "in the description.",
        #     ],
        #     scale=1.5,
        #     reactions=['happy', 'cool', 'cool'])
        # self.wait()
        # self.play(*[FadeOut(x) for x in objs])
        self.play(DrawBorderThenFill(self.create_ninja('cool')))
        end = TextMobject("Thanks", "for", "watching!").arrange_submobjects(DOWN).scale(1.8)
        self.play(Write(end))
        self.wait(duration=3)
        self.play(*[FadeOut(x) for x in [end, self.ninja]])
        self.wait()

# python -m manim from_rahul\08_set.py ComeIn -t -m -r 1080
class ComeIn(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        sc = ScreenGrabber(self)
        happy = self.create_ninja('happy')
        self.play(FadeInFrom(happy, RIGHT))
        sc.save()

# python -m manim from_rahul\08_set.py Think -t -m -r 1080
class Think(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        sc = ScreenGrabber(self)
        self.add(self.create_ninja('happy'))
        self.play(self.change_ninja('thinking'))
        sc.save()

# python -m manim from_rahul\08_set.py Yes -t -m -r 1080
class Yes(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        sc = ScreenGrabber(self)
        self.add(self.create_ninja('thinking'))
        self.play(self.change_ninja('yes'))
        sc.save()

# python -m manim from_rahul\08_set.py YesGoOut -t -m -r 1080
class YesGoOut(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        self.add(self.create_ninja('yes'))
        self.play(FadeOutAndShift(self.ninja, RIGHT))

# python -m manim from_rahul\08_set.py Confused -t -m -r 1080
class Confused(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        sc = ScreenGrabber(self)
        self.add(self.create_ninja('yes'))
        self.play(self.change_ninja('confused'))
        self.wait(2)
        sc.save()

# python -m manim from_rahul\08_set.py GoOut -t -m -r 1080
class GoOut(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        self.add(self.create_ninja('confused'))
        self.play(FadeOutAndShift(self.ninja, RIGHT))
