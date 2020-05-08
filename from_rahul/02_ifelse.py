#!/usr/bin/env python

from manimlib.imports import *
from rahul.ninja import Ninja
from rahul.utils import VSColors, ExplainableTextObject

# python -m manim rahul\02_ifelse.py Test -c #151520 -pl
DIR = os.path.dirname(os.path.abspath(__file__))

class Test(Scene):
    def construct(self):
        emotions = ['happy', 'dunno', 'thinking', 'happy', 'sad', 'confused', 'cool', 'poker', 'surprised']

        last = emotions[0]
        last_ninja = Ninja(last).obj().scale(2)
        self.play(DrawBorderThenFill(last_ninja))

        for cur in emotions[1:]:
            ninja = Ninja(cur)
            cur_ninja = ninja.obj().scale(2)
            self.play(ReplacementTransform(last_ninja, cur_ninja))
            last_ninja = cur_ninja
            self.wait(duration=2)

        self.play(*[FadeOutAndShiftDown(x) for x in [last_ninja]])
        self.wait()


class EmojiTest(Scene):
    def construct(self):
        emotions = ['cool', 'confused', 'sad', 'happy']

        last = emotions[0]
        last_ninja = Ninja(last).obj()
        self.play(DrawBorderThenFill(last_ninja))

        for cur in emotions[1:]:
            ninja = Ninja(cur)
            cur_ninja = ninja.obj()
            self.play(ReplacementTransform(last_ninja, cur_ninja))
            last_ninja = cur_ninja
            self.wait()

        self.play(*[FadeOutAndShiftDown(x) for x in [last_ninja]])
        self.wait()


class TypeConversion(Scene):
    def construct(self):
        tc = TextMobject("Type Conversion")
        self.play(Write(tc))
        self.wait()

        ei = TextMobject("Explicit", "Implicit").arrange_submobjects(DOWN).space_out_submobjects(factor=2)
        br = Brace(ei, direction=LEFT)
        ei.add_updater(lambda d: d.next_to(br, RIGHT))
        br.add_updater(lambda d: d.next_to(tc, RIGHT))
        self.play(tc.to_edge, LEFT, 3)
        self.play(Write(br))
        self.play(Write(ei))

        self.play(tc.to_edge, LEFT, 1.5)
        ee = TextMobject("\\texttt{a = int(\"3\")}", "$$\\Rightarrow a = 3$$")
        ee.arrange_submobjects(DOWN, aligned_edge=LEFT).add_background_rectangle(opacity=0.4, color="#356272", buff=0.4)
        ee.add_updater(lambda d: d.next_to(ei[0], UR, aligned_edge=BOTTOM, buff=0.5))
        for x in [1,0,2]:
            self.play(Write(ee[x]))
        self.wait()
        ie = TextMobject("\\texttt{a = 1 + 2.14}", "$$\\Rightarrow a = 3.14$$")
        ie.arrange_submobjects(DOWN, aligned_edge=LEFT).add_background_rectangle(opacity=0.4, color="#356272", buff=0.4)
        ie.add_updater(lambda d: d.next_to(ei[1], DR, aligned_edge=TOP, buff=0.5))
        for x in [1,0,2]:
            self.play(Write(ie[x]))
        self.wait()


class Types(Scene):
    def construct(self):
        data = [
            ('Integer', 'int', [0, 1, -12, 78546]),
            ('Real number', 'float', [3.1415, 0.00, 2/3, 6.6e-11]),
            ('Text', 'str', ['""', '"world"', '"good day"']),
            ('Boolean', 'bool', ['True', 'False'])
        ]

        dt = TextMobject("Data Types").scale(3)
        self.play(Write(dt))
        dt.add(Underline(dt))
        self.play(FadeIn(dt[-1]))

        dt1 = dt.copy().scale(.5).to_corner(UL, buff=1)
        self.play(ReplacementTransform(dt, dt1))

        row = None
        for real, py, egs in data:
            h = TextMobject(real + " Type").scale(1.3)
            i = TextMobject("\\texttt{Python equivalent is " + py + "}")
            e = TextMobject('e.g. ' + ', '.join([str(x) for x in egs])).scale(0.8)
            box = VGroup(h, i, e).arrange_submobjects(DOWN, aligned_edge=LEFT, buff=0.7)
            if row:
                for old, new in zip(row, box.submobjects):
                    self.play(ReplacementTransform(old, new))
            else:
                for txt in box:
                    self.play(Write(txt))
            self.wait(duration=2)
            row = box.submobjects

        self.wait()
        self.play(*[FadeOut(x) for x in row], FadeOut(dt1))
        self.wait()


class ArithmaticOperators(Scene):
    def construct(self):
        operands = [(2, 3), (5, 2), (4, 2)]
        operators = [
            ('+', lambda x,y: x+y, ['Addition']),
            ('-', lambda x,y: x-y, ['Subtraction']),
            ('*', lambda x,y: x*y, ['Multiplication']),
            ('/', lambda x,y: x/y, ['Division']),
            ('\%', lambda x,y: x%y, ['Remainder']),
            ('**', lambda x,y: x**y, ['Exponentiation', '$$x^y$$']),
            ('//', lambda x,y: x//y, ['Floor division', '$$\\lfloor{x}\\rfloor$$'])
        ]
        # texts = ['Add', 'Subtract', 'Multiply', 'Divide', 'Modulus', 'Exponent', 'Floor divide']

        ao = TextMobject("Arithmatic operators")
        self.play(Write(ao))
        ao1 = ao.copy().scale(1.5).to_corner(UL, buff=2)
        self.play(ReplacementTransform(ao, ao1))
        info = VGroup(
            TextMobject("Arithmetic operators are used"),
            TextMobject("to perform common mathematical operations")
        ).arrange_submobjects(DOWN, aligned_edge=LEFT)
        br = info.add_background_rectangle(buff=0.5)
        for x in info:
            if isinstance(x, TextMobject):
                self.play(Write(x), run_time=len(x.tex_strings[0]) / 15)
            else:
                self.play(Write(x))
        self.wait()
        self.play(*[FadeOutAndShiftDown(x) for x in [ao1, info]])
        self.wait()

        heading, examples = None, None
        for op, fn, txt in operators:
            new_heading = TextMobject(*txt).arrange_submobjects(RIGHT).scale(1.5).to_corner(UL, buff=2)
            new_examples = VGroup()
            for x, y in operands:
                strs = [f"\\texttt{{{i}}} " for i in [x, op, y, '=', fn(x,y)]]
                new_examples.add(TextMobject(*strs))
            new_examples.arrange_submobjects(DOWN).to_edge(DOWN, buff=3)

            if heading:
                self.play(
                    ReplacementTransform(heading, new_heading),
                    ReplacementTransform(examples, new_examples))
            else:
                self.play(Write(new_heading), Write(new_examples))
            self.wait(duration=2)
            heading, examples = new_heading, new_examples

        self.wait()
        self.play(*[FadeOut(x) for x in [heading, examples]])
        self.wait()


class PrintFunction(Scene):
    def construct(self):
        happy = Ninja('happy').svg.to_corner(DR)
        confused = Ninja('confused').svg.to_corner(DR)
        poker = Ninja('poker').svg.to_corner(DR)
        pf = ExplainableTextObject("print", "function")
        pf.text.set_color(VSColors.variable).to_edge(LEFT, buff=4)
        lb = TextMobject("(").set_color(VSColors.variable).scale(1.5)
        lb.add_updater(lambda d: d.next_to(pf.text))
        rb = TextMobject(")").set_color(VSColors.variable).scale(1.5).next_to(lb)

        self.play(Write(pf.text), Write(lb), Write(rb), DrawBorderThenFill(happy))
        self.play(GrowFromCenter(pf.braces))
        self.play(Write(pf.hint))
        self.wait()

        hw = ExplainableTextObject("\"Hello\"", "argument", direction=UP)
        hw.text.set_color(VSColors.string).add_updater(lambda d: d.next_to(lb))
        self.play(rb.next_to, hw.text)
        self.play(Write(hw.text))
        self.play(GrowFromCenter(hw.braces))
        self.play(Write(hw.hint))
        # self.wait()

        self.play(pf.text.to_edge, LEFT, 3)
        com = TextMobject(",").set_color(VSColors.variable).scale(1.5)
        com.next_to(hw.text)
        hw1 = ExplainableTextObject("\"World\"", "argument", direction=UP)
        hw1.text.set_color(VSColors.string).next_to(com)
        com.set_y(-0.33)
        self.play(rb.next_to, hw1.text)
        self.play(Write(hw1.text), Write(com), ReplacementTransform(happy, poker))
        self.play(GrowFromCenter(hw1.braces))
        self.play(Write(hw1.hint), ReplacementTransform(poker, confused))
        self.wait()

        self.play(*[FadeOut(x) for x in [pf.braces, pf.hint, hw.obj, lb, rb, hw1.obj, com]])
        pf1 = pf.text.copy().scale(1.2).to_corner(UL, buff=2)
        poker = Ninja('poker').svg.to_corner(DR)
        self.play(ReplacementTransform(pf.text, pf1), ReplacementTransform(confused, poker))

        info = VGroup(
            TextMobject("\\texttt{print} is one of the built-in functions"),
            TextMobject("which can be used to print value(s) on screen")
        ).arrange_submobjects(DOWN, aligned_edge=LEFT)
        info[0][0][:5].set_color(color=VSColors.variable)
        br = info.add_background_rectangle(buff=0.5)

        for x in info:
            if isinstance(x, TextMobject):
                self.play(Write(x), run_time=len(x.tex_strings[0]) / 15)
            else:
                self.play(Write(x))

        happy = Ninja('happy').svg.to_corner(DR)
        self.play(ReplacementTransform(poker, happy))
        self.wait(duration=2)

