#!/usr/bin/env python
import subprocess
from manimlib.imports import *
# from manimlib.utils.rate_functions import linear
from from_rahul.ninja import Ninja
from from_rahul.extend import *
# from from_rahul.table import Table


# python -m manim from_rahul\05_str.py Test -c #151520 -pl
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
    dcolor = kwargs.pop('dcolor', MCOLORS.PeekabooPeach)

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
        txidx.next_to(txbox, direction=UP)
        txrid = TextMobject(str(i - n), color=dcolor).scale(iscale)
        txrid.next_to(txbox, direction=DOWN)
        # txrid.next_to(txidx, direction=DOWN, aligned_edge=RIGHT)
        boxes.add(VGroup(txobj, txbox, txidx, txrid))
    boxes.arrange_submobjects()
    boxes.shift([-0.5, 0.3, 0])
    return whole, boxes

class Index(AdvancedScene):
    def construct(self):
        self.play(FadeInFrom(self.create_ninja(), RIGHT))
        code = TextMobject('\\texttt{"python"}').scale(2)
        code1 = TextMobject('\\texttt{python}').scale(2)
        self.play(Type(code))
        self.play(*[FadeOut(x) for x in [code[0], code[-1]]])
        for x in code[1:-1]:
            self.remove(x)
        self.add(code1)
        text, string = get_boxes('python')
        self.play(ReplacementTransform(code1, text))
        self.play(self.change_ninja('thinking'))
        self.play(*[DrawBorderThenFill(x[1]) for x in string])
        for ch in string:
            self.play(FadeIn(ch[2]))
        ub = BraceLabel(string, "index", UP, label_scale=1.6)
        for x in ub:
            x.set_color(color=MCOLORS.WildWasabi)
        self.play(GrowFromCenter(ub))
        self.wait()
        self.play(self.change_ninja('confused'))
        self.wait(duration=2)
        self.play(self.change_ninja('happy'))
        self.wait()
        for i, ch in enumerate(string[::-1]):
            self.play(FadeIn(ch[3]))
            if i == 0:
                self.play(self.change_ninja('surprised'))
        db = BraceLabel(string, "negative\\text{ }index", DOWN, label_scale=1.6)
        for x in db:
            x.set_color(color=MCOLORS.PeekabooPeach)
        self.play(GrowFromCenter(db), self.change_ninja('thinking'))
        self.wait()
        self.play(self.change_ninja('happy'))
        self.wait()
        outobjs = VGroup(text, ub, db)
        for ch in string:
            outobjs.add(ch[1:])
        old = outobjs.copy().scale(0.7).to_edge(UP)
        self.play(ReplacementTransform(outobjs, old))
        self.wait()
        eg = VGroup(
            TextMobject(r'\texttt{n = len("python")'),
            TexMobject(r"\text{valid index} \in [-n,n-1]", color=MCOLORS.Twitter, background_stroke_color=MCOLORS.Twitter))
        eg.arrange_submobjects(DOWN, aligned_edge=LEFT).next_to(old, DOWN, buff=0.8)
        eg.add_background_rectangle(buff=0.5)
        for obj in eg:
            self.play(Write(obj))
        self.wait()
        self.play(*[FadeOut(x) for x in [old, eg]] + [FadeOutAndShift(self.ninja, RIGHT)])
        # self.play(*[FadeOut(x) for x in outobjs])
        self.wait()


def run_eg(self, function, info, eg):
    leaving = self.define_function(
        function,
        info,
        [
            [f"s = \"{eg}\"", f"t = s.{function}", "print(\"'\" + t + \"'\")"]
        ],
        reactions=['happy', 'thinking'],
        scale=1.5, example_scale=1.2, intro=False)
    self.play(*[FadeOut(x) for x in leaving])

class Str1(AdvancedScene):
    def construct(self):
        leaving = self.define_word(
            "String Methods", [
                'Strings implement all of the common sequence operations,',
                'along with the additional string methods',
                'They can be called with .(dot) and function name.',
                'As string are immutable, all functions return a new string.'],
                scale=1.5, reactions=['happy', 'thinking'], animation=DrawBorderThenFill)
        self.wait()
        self.play(*[FadeOut(x) for x in leaving])

        run_eg(self, "lower()", ["Converts a string into lower case"], "What are YOU doing?")
        run_eg(self, "upper()", ["Converts a string into upper case"], "What are YOU doing?")
        run_eg(self, "swapcase()", ["Swaps cases, lower case becomes", "upper case and vice versa"], "What are YOU doing?")
        run_eg(self, "capitalize()", ["Converts the first character to uppercase"], "what are YOU doing?")
        run_eg(self, "title()", ["Converts the first character of", "each word to uppercase"], "What are YOU doing?")

        leaving = self.define_word(
            "Whitespace Characters", [
                'They are the characters that are not visible on screen',
                'e.g. $\\backslash t, \\backslash n, \\backslash r, \\backslash f, \\backslash v, (space)$'],
                scale=1.5, reactions=['happy', 'thinking'])
        self.wait()
        self.play(*[FadeOut(x) for x in leaving])

        run_eg(self, "rstrip()", ["Returns a right trim version of the string", "i.e it removes whitespaces from right"], "  \\tSome string\\n  ")
        run_eg(self, "lstrip()", ["Returns a left trim version of the string", "i.e it removes whitespaces from left"], "  \\tSome string\\n  ")
        run_eg(self, "strip()", ["Returns a trim version of the string", "i.e it removes whitespaces from left \\& right"], "  \\tSome string\\n  ")
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.wait()

def run_beg(self, function, info, egs):
    leaving = self.define_function_egs(
        function,
        info,
        [f"\"{eg}\".{function}" for eg in egs],
        reactions=['happy', 'thinking'],
        scale=1.5, example_scale=1.2, intro=False, color_tf=1)
    self.wait(duration=2)
    self.play(*[FadeOut(x) for x in leaving])

class Str2(AdvancedScene):
    def construct(self):
        self.play(DrawBorderThenFill(self.create_ninja()))
        run_beg(self, "islower()", ["Returns True if all characters are lowercase"], [
            "", "already", "POWER", "Pi", "the world", "x45", "K@KaR0t"
        ])
        run_beg(self, "isupper()", ["Returns True if all characters are uppercase"], [
            "", "already", "POWER", "Pi", "THE WORLD", "X45", "K@KaR0t"
        ])
        run_beg(self, "istitle()", ["Returns True if the string is same as title()"], [
            "", "This is nice.", "Cs Glitz", "all lowercase characters"
        ])
        run_beg(self, "isalpha()", ["Returns True if all characters are alphabet"], [
            "", "already", "POWER", "the world", "x45", "K@KaR0t"
        ])
        run_beg(self, "isdigit()", ["Returns True if all characters are digit"], [
            "", "x45", "Pi", "123", "+45", "3.1415"
        ])
        run_beg(self, "isalnum()", ["Returns True if all characters are alpha-numeric"], [
            "", "already", "The World", "12345", "Bm45", "K@KaR0t"
        ])
        run_beg(self, "isspace()", ["Returns True if all characters are whitespace"], [
            "", "\\t", "Nice\\n", "  \\t  \\n  ", "wow"
        ])
        run_beg(self, "isprintable()", ["Returns True if all characters are non-whitespace"], [
            "", "\\t", "Nice\\n", "Over here!", "wow"
        ])
        run_beg(self, "isidentifier()", ["Returns True if the string is an identifier"], [
            "", "Bye!", "Cs Glitz", "aVariable", "_start45", "_", "45"
        ])
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.wait()

class Test(AdvancedScene):
    def construct(self):
        filepath = os.path.join(DIR, 'data', 'test.py')
        # code = Code(filepath, language='py', tab_width=2, font='Consolas').scale(2).center()
        code = CodeMobject(
            "import numpy as np",
            "class Small:",
            "    def __init__(self):",
            "        pass",
            "for x in range(10):",
            "    print(x)").scale(2).center()
        self.play(DrawBorderThenFill(code[0]))
        self.play(Write(code[1]))
        text = VGroup(*code[2:])
        cursor = Cursor(text) #.stretch_to_fit_width(0.2)
        self.play(Type(text, cursor))
        cursor.start_blink()
        self.wait(duration=5)
        cursor.stop_blink()
        self.wait(duration=5)
        self.play(FadeOut(code), FadeOut(cursor))
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


class Recap(AdvancedScene):
    def construct(self):
        # # sc = ScreenGrabber(self)
        leaving_objects = self.create_slide(
            "What we learned today?",
            [
                "How string index works",
                "Slicing (substring)",
                "How to manipulate string",
                "String methods",
            ],
            animation=DrawBorderThenFill,
            # screenshot=sc,
            reactions=['happy', 'thinking'])
        self.wait()
        self.play(*[FadeOut(x) for x in leaving_objects])

        objs = self.define_word(
            "Practice Makes Progress",
            [
                "Links to the example source",
                "code and assignments are",
                "in the description.",
            ],
            # screenshot=sc,
            reactions=['happy', 'cool', 'cool'])
        self.wait()
        self.play(*[FadeOut(x) for x in objs])

        # sc.save()

        end = TextMobject("Thanks", "for", "watching!").arrange_submobjects(DOWN).scale(1.8)
        self.play(Write(end))
        self.wait(duration=2.5)
        self.play(*[FadeOut(x) for x in [end, self.ninja]])
        self.wait()


# python -m manim from_rahul\05_str.py IndexInfo -t -pm -r 1080
class IndexInfo(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["I am listing both", "index and negative index"]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


class ForValues(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["Variable $i$ will take", "values 0, 3, 6, ..."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


class Slice(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["\\texttt{msg[i:i+1]} will give", "us a substring of 3", "starting from i"]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


class Count(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["This will ignore", "the last $a$"]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


class Replace(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["Notice that middle $n$", "is not changed."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


class Reverse(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('cool', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["\\texttt{s[::-1]} for reverse", "is so cool."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
