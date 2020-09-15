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

# python -m manim from_rahul\07_tuple.py Intro -pl
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
            "Topics on tuples",
            [
                "Create, access, iterate, and unpacking",
                "list() vs tuple() and slicing",
                "+ (concatenation) and * (repeat) operators",
                "count(), index() and membership operators",
                "reversing, sorting and comparison operators",
                "Understanding enumerate() and zip()",
            ],
            write_speed=35,
            reactions=['happy', 'thinking'])
        self.wait()
        leaving_objects.append(self.ninja)
        self.play(*[FadeOut(x) for x in leaving_objects])
        self.wait()

# python -m manim from_rahul\07_tuple.py Comparison -pl
class Comparison(AdvancedScene):
    def construct(self):
        operands = [
            ('()', '(1,)'),
            ('(1,)', '(1, 2)'),
            ('(1, 2)', '(1, 1)'),
            ('(1, 2)', '(1, 2)'),
            ('(1, 2)', '(1, 3)'),
            ('(1, 2)', '(1, 2, 1)')]
        operators = [
            ('<', 'Less than'),
            ('<=', 'Less than or Equal to'),
            ('>', 'Greater than'),
            ('>=', 'Greater than or Equal to'),
            ('==', 'Equal to'),
            ('!=', 'Not equal to'),
        ]

        h, hu = self.show_heading(
            "Comparison operators",
            animation=DrawBorderThenFill,
            scale=1.3)
        self.wait()

        texts = [[x, '..', y, '.....'] for (x, y) in operands]
        table = Table(
            [[f'\\texttt{{{t}}}' for t in row] for row in texts],
            widths=[1, 0.35, 1, 2.5],
            align='rrll'
        )
        self.play(Write(table), run_time=3)
        msg = TextMobject('\\texttt{[Pause if you wanna take a closer look]}').scale(0.8)
        msg.to_edge(DOWN)
        self.play(FadeIn(msg), self.change_ninja('thinking'))

        for op, txt in operators:
            h1 = TextMobject(txt).scale(1.3).to_corner(UL, buff=1)
            hu1 = Underline(h1)
            self.play(ReplacementTransform(h, h1), ReplacementTransform(hu, hu1))
            h, hu = h1, hu1

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
            self.wait(duration=3)
            for i, o, n in new_objs:
                table.submobjects[i] = n

        self.play(self.change_ninja('happy'))
        self.play(*[FadeOut(x) for x in [h, hu, table, msg, self.ninja]])
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


# python -m manim from_rahul\07_tuple.py Outro -pl
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

# python -m manim from_rahul\07_tuple.py Differences -pl
class Differences(AdvancedScene):
    def construct(self):
        self.play(DrawBorderThenFill(self.create_ninja()))
        leaving_objects = self.create_slide(
            "Differences between list and tuple",
            [
                "Tuples are immutable",
                "Tuples take less memory",
                "Tuples are faster to create and copy",
            ],
            write_speed=20,
            reactions=['happy', 'thinking'])
        self.wait()
        leaving_objects.append(self.ninja)
        self.play(*[FadeOut(x) for x in leaving_objects])
        self.wait()
