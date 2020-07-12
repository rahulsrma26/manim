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

# python -m manim from_rahul\shorts.py Outro -pl
class Outro(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja(corner=None)
        channel = TextMobject("csglitz").next_to(ninja, DOWN)
        self.play(DrawBorderThenFill(ninja), Write(channel))
        # self.add(self.create_ninja(corner=None))
        up = Arrow(1.9*UL, 2*UL+LEFT, buff=0, stroke_width=20, max_stroke_width_to_length_ratio=20)
        up.scale(1).shift(-UL)
        # self.play(GrowArrow(up))
        self.wait(duration=1)
        self.play(self.change_ninja('yes', corner=None))
        self.wait()
        dn = Arrow(1.9*DL, 2*DL+LEFT, buff=0, stroke_width=20, max_stroke_width_to_length_ratio=20)
        dn.scale(1).shift(-DL + 0.2*DOWN)
        # self.play(GrowArrow(dn), FadeOut(up))
        self.wait(duration=1)
        self.play(self.change_ninja('surprised', corner=None))
        self.play(self.change_ninja('happy', corner=None))
        # self.play(FadeOut(dn), self.ninja.to_corner, DR)
        self.play(FadeOut(channel), self.ninja.to_corner, DR)
        end = TextMobject("Thanks", "for", "watching!").arrange_submobjects(DOWN).scale(1.8)
        self.play(Write(end))
        self.play(self.change_ninja('cool'))
        self.wait(duration=1)
        self.play(*[FadeOut(x) for x in [end, self.ninja]])
        self.wait()

