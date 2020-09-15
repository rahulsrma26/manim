#!/usr/bin/env python

from manimlib.imports import *
from from_rahul.ninja import Ninja
from from_rahul.extend import *

# To watch one of these scenes, run the following:
# python -m manim rahul\example.py LogoAnimation -c #151520 -pl
# optional arguments:
# -h, --help show this help message and exit
# -p, --preview
# -w, --write_to_movie
# -s, --show_last_frame
# -l, --low_quality
# -m, --medium_quality
# -g, --save_pngs
# -f, --show_file_in_finder
# -t, --transparent
# -q, --quiet
# -a, --write_all
# -o OUTPUT_NAME, --output_name OUTPUT_NAME
# -n START_AT_ANIMATION_NUMBER, --start_at_animation_number START_AT_ANIMATION_NUMBER
# -r RESOLUTION, --resolution RESOLUTION
# -c COLOR, --color COLOR
# -d OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY

class Logo(Scene):
    def construct(self):
        n = Ninja()
        self.play(FadeIn(n))
        self.wait()

class LogoAnimation(Scene):
    def construct(self):
        x1, x2, x3 = -2, 0, 2
        lw = 6
        nodes = Mobject()
        nodes.add(
            Circle(radius=0.3).set_x(x1).set_y(1),
            Circle(radius=0.3).set_x(x1).set_y(-1),
            Circle(radius=0.3).set_x(x2).set_y(2),
            Circle(radius=0.3).set_x(x2).set_y(0),
            Circle(radius=0.3).set_x(x2).set_y(-2),
            Circle(radius=0.3).set_x(x3).set_y(1),
            Circle(radius=0.3).set_x(x3).set_y(-1),
        )
        for node in nodes:
            node.set_style(fill_opacity=1, fill_color=BLUE, stroke_width=0)
        self.play(*[ShowCreation(x) for x in nodes])

        left = Mobject()
        left.add(
            Line((x1,-1,0), (x2,-2,0)).set_color_by_gradient([YELLOW, GREEN]).set_stroke(width=lw),
            Line((x1,-1,0), (x2,0,0)).set_color_by_gradient([YELLOW, GREEN]).set_stroke(width=lw),
            Line((x1,1,0), (x2,0,0)).set_color_by_gradient([YELLOW, GREEN]).set_stroke(width=lw),
            Line((x1,1,0), (x2,2,0)).set_color_by_gradient([YELLOW, GREEN]).set_stroke(width=lw),
        )
        self.bring_to_back(left)
        self.play(*[ShowCreation(x) for x in left])

        right = Mobject()
        right.add(
            Line((x2,-2,0), (x3,-1,0)).set_color_by_gradient([RED, YELLOW]).set_stroke(width=lw),
            Line((x2,0,0), (x3,-1,0)).set_color_by_gradient([RED, YELLOW]).set_stroke(width=lw),
            Line((x2,0,0), (x3,1,0)).set_color_by_gradient([RED, YELLOW]).set_stroke(width=lw),
            Line((x2,2,0), (x3,1,0)).set_color_by_gradient([RED, YELLOW]).set_stroke(width=lw),
        )
        self.bring_to_back(right)
        self.play(*[ShowCreation(x) for x in right])

        logo = Group(left, right, nodes)
        # self.bring_to_front(*n0)
        lg = logo.copy().scale(0.5).to_edge(RIGHT, buff=3)

        name = TextMobject("\\texttt{csglitz}").scale(3).to_edge(LEFT, buff=3)
        self.play(Transform(logo, lg), FadeInFrom(name, LEFT))
        self.wait()


# python -m manim from_rahul\logo.py GitHub -pl
class GitHub(AdvancedScene):
    CONFIG = {
        "camera_config": {
            "background_color": WHITE
        }
    }
    def construct(self):
        w = Ninja("wave")
        self.add(w)
        w.wave(self, 1)