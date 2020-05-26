#!/usr/bin/env python

from manimlib.imports import *
from from_rahul.ninja import Ninja
from from_rahul.utils import *

# python -m manim from_rahul\02_fstring.py Test -c #151520 -pl
DIR = os.path.dirname(os.path.abspath(__file__))
SDIR = os.path.join(DIR, 'svgs')

class Test(AdvancedScene):
    def construct(self):
        self.define_word(
            "\\texttt{list.pop([i])}",
            [
                "Remove the item at the given position in the list,",
                "and return it. If no index is specified, \\texttt{a.pop()}",
                "removes and returns the last item in the list."
            ],
            fade=True,
            reactions=['happy', 'thinking'])
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


class Variable(AdvancedScene):
    def construct(self):
        self.create_slide(
            "Variable naming rules",
            [
                "$\\bullet$ A variable must begin with a letter or underscore.",
                "$\\bullet$ Letters can be small or capital.",
                "$\\bullet$ Apart from the first character, other characters",
                "$\\hookrightarrow$ can be a letter, a number, or underscore.",
                "$\\bullet$ Some examples of valid variable names are:",
	            "$\\rightarrow$ \\texttt{A, x, goodVariable, my\\_value}",
                "$\\rightarrow$ \\texttt{g6, \\_important, Superman, SHOUTING, \\_}",
                "$\\bullet$ And these are some of the invalid variable names:",
	            "$\\rightarrow$ \\texttt{4pi, 2bOrNot2b} (starts with the digit)",
                "$\\rightarrow$ \\texttt{Age+, *stars*} (contains special characters)"
            ],
            screenshot=ScreenGrabber(self),
            fade=True,
            bullets=False,
            reactions=['happy', 'thinking'])
        self.wait()


class Input(AdvancedScene):
    def construct(self):
        self.create_slide(
            "User Input",
            [
                "User input is an information or data",
                "sent to the computer for processing.",
                "Which can be done from input devices."
            ],
            screenshot=ScreenGrabber(self),
            gap=0.5,
            question="What's a user input?",
            bullets=False,
            reactions=['happy', 'dunno', 'thinking'])

        heading = TextMobject("Input devices").scale(3)
        title = heading.copy().scale(0.5).to_corner(UL, buff=1)
        self.play(Write(heading))
        self.play(ReplacementTransform(heading, title))
        underline = Underline(title)
        self.play(FadeIn(underline))

        devices = "keyboard,mouse,controller,touchpad,microphone,camera"
        info = Group(*[
            SVGMobject(os.path.join(SDIR, f'{o}.svg')) for o in devices.split(',')
            ])

        info.submobjects[0].set_x(-3).set_y(0.5)
        info.submobjects[1].set_x(1).set_y(0.5)
        info.submobjects[2].set_x(-4).set_y(-2.5)
        info.submobjects[3].scale(0.7).set_x(1).set_y(-2.5)
        info.submobjects[4].set_x(3).set_y(2)
        info.submobjects[5].set_x(4.5).set_y(0)

        for obj in info.submobjects:
            obj.set_fill(opacity=0)
            self.play(DrawBorderThenFill(obj))

        self.wait()
        self.play(*[FadeOut(x) for x in [info, self.ninja, title, underline]])
        self.wait()

class Recap(AdvancedScene):
    def construct(self):
        sc = ScreenGrabber(self)
        self.create_slide(
            "What we learned today?",
            [
                "Different ways to assign variables",
                "Variable naming rules and good practices",
                "Different ways to initialize string",
                "3 arithmetic operators with string (+, *, \\%)",
                "How to take values from user",
                "Formatting string (f-string)",
            ],
            animation=DrawBorderThenFill,
            screenshot=sc,
            reactions=['thinking', 'happy', 'surprised'])

        sc.save()
        ninja = Ninja('cool').to_corner(DR)

        end = TextMobject("Thanks for watching!").scale(1.8)
        self.play(Write(end))
        self.wait()
        self.play(ReplacementTransform(self.ninja, ninja))
        self.wait()
        self.play(*[FadeOut(x) for x in [end, ninja]])
        self.wait()
