#!/usr/bin/env python
import subprocess
from manimlib.imports import *
# from manimlib.utils.rate_functions import linear
from from_rahul.ninja import Ninja
from from_rahul.extend import *
from from_rahul.table import Table


# python -m manim from_rahul\04_loop.py Test -c #151520 -pl
DIR = os.path.dirname(os.path.abspath(__file__))
SDIR = os.path.join(DIR, 'svgs')

prog1 = '''
...
while condition:
    statement-1
    statement-2
    ...
    statement-n
...
...
'''

class WhileLoop(AdvancedScene):
    def construct(self):
        h, hu = self.show_heading(
            "while loop",
            scale=1.4,
            animation=DrawBorderThenFill,
            reactions=['happy', 'thinking'])
        code = prog1[1:]
        text = CodeMobject(*code.split('\n'))
        # text = CodeMobject("\\texttt{Hello}", "\\texttt{testing}", "\\texttt{1 2 3 ...}").arrange_submobjects(DOWN)
        cursor = Cursor(text)
        text1 = text.copy()
        self.play(Type(text, cursor), run_time=8)
        cursor.start_blink()
        self.wait()
        true = TextMobject("True", color=MCOLORS.WildWasabi).next_to(text1.submobjects[1], RIGHT)
        false = TextMobject("False", color=MCOLORS.PeekabooPeach).next_to(text1.submobjects[1], RIGHT)
        rect = RunCode(self, text1, [0, 0,
            [1, FadeIn(true)], 1, [2, FadeOut(true)], 3, 4, 5,
            [1, FadeIn(true)], 1, [2, FadeOut(true)], 3, 4, 5,
            [1, FadeIn(false)], 1, [6, FadeOut(false)], 7, 7])
        self.play(self.change_ninja('happy'))
        self.wait()
        cursor.stop_blink()
        self.play(*[FadeOut(x) for x in [text, cursor, rect, h, hu, self.ninja]])
        self.wait()


def calculate_output(program):
    result = subprocess.run(['python', '-c', program], stdout=subprocess.PIPE)
    return result.stdout.decode()

class CodeEditor(VGroup):
    def __init__(self, **kwargs):
        width = kwargs.pop('width', 10)
        height = kwargs.pop('height', 2)
        super().__init__(**kwargs)
        self.editor = RoundedRectangle(width=width, height=height,
            corner_radius=0.2, stroke_width=0, fill_color=BLACK, fill_opacity=1)
        self.text_editor = TextMobject("Code").rotate(PI/2).next_to(self.editor, LEFT)
        self.terminal = self.editor.copy().next_to(self.editor, DOWN)
        self.text_terminal = TextMobject("Output").rotate(PI/2).next_to(self.terminal, LEFT)
        self.add(self.editor)
        self.add(self.text_editor)
        self.add(self.terminal)
        self.add(self.text_terminal)
        self.to_edge(LEFT)


class Escape(AdvancedScene):
    def construct(self):
        # h, hu, info = self.define_word(
        #     "Escape characters",
        #     [
        #         "The escape character allows you to use",
        #         "some special characters which you",
        #         "normally can not type in code."
        #     ],
        #     animation=DrawBorderThenFill,
        #     scale=1.3,
        #     reactions=['happy', 'thinking'])
        # self.wait()
        # self.play(*[FadeOut(x) for x in [info]])
        # self.wait()

        slides = [
            ("\\'", 'Single Quote', "print('I got Ram\\'s bow')"),
            ('\\"', 'Double Quote', 'print("\\"Thank you!\\", he said")'),
            ('\\n', 'New Line', "print('abcd\\nef')"),
            ('\\t', 'Tab', "print('abcd\\tef')"),
            ('\\b', 'Backspace', "print('abcd\\bef')"),
            ('\\r', 'Carriage Return', "print('abcd\\ref')"),
            ('\\f', 'Form Feed', "print('abcd\\fef')"),
            ('\\v', 'Vertical Tab', "print('abcd\\vef')"),
        ]

        # editor = RoundedRectangle(width=10, height=2, stroke_width=0)
        # print('pr', pr)
        # pr.set_fill(color=BLACK, opacity=1)
        ide = CodeEditor()
        self.play(DrawBorderThenFill(ide))
        for ch, tx, eg in slides:
            # msg = TextMobject(f'{eg} (\\texttt{{{ch}}})').to_corner(UL, buff=2)
            code = CodeMobject(eg).move_to(ide.editor, aligned_edge=LEFT)
            code.set_x(code.get_x() + 0.4)
            cursor = Cursor(code)
            self.play(Type(code, cursor))
            out = calculate_output(eg).split('\r\n')
            print('out', out)
            # output = CodeMobject(*out).move_to(ide.terminal, aligned_edge=LEFT)
            # output.set_x(output.get_x() + 0.4)
            # self.play(Type(output, cursor))
            # cursor.start_blink()
            # self.wait()
            # cursor.stop_blink()
            self.play(*[FadeOut(x) for x in [code]])
            # break

        # self.play(*[FadeOut(x) for x in [h, hu, self.ninja]])
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
                "Escape Characters",
                "Python shell",
                "while loop and shortcut operators",
                "Debug Code using VS Code",
                "Iterators, for loop and range function",
                "break, else and continue statements",
                "Loop within a loop (Nesting)",
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

        end = TextMobject("Thanks for watching!").scale(1.8)
        self.play(Write(end))
        self.wait(duration=2.5)
        self.play(*[FadeOut(x) for x in [end, self.ninja]])
        self.wait()


class ClsCommand(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["cls command is similar", "to clear command in", "mac and linux."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()


class ASCII(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["Check descriptions", "for ASCII characters."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()


class Range(AdvancedScene):
    def construct(self):
        sc = ScreenGrabber(self)
        txt = ["Note: range() does not return iterator.", "    It will return an iterator when", "    iter() is called on its return value."]
        info = CodeMobject(*txt, code_font=False, code_coloring=False)
        for obj in info.submobjects:
            obj.set_fill(color="#151520").set_color(color="#151520")
        # info = VGroup(*[TextMobject(obj, fill_color="#151520", color="#151520") for obj in txt])
        # info.arrange_submobjects(DOWN, aligned_edge=LEFT)
        info.scale(0.7)

        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        sc.save()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()


class CtrlC(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["In terminal, Ctrl + C", "can be used to abort", "the current task."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()


class Prime(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["Since 5 is prime", "our loop is not breaking."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()


class NotPrime(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["Since 10 is not a prime", "our loop is breaking at 2."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()


class Import(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["You need to import", "a function before", "you can call it."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()


class NoElse(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["Notice that we", "don't need to", "use else here."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()


class Nesting(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["Everytime inner loop", "will run one more", "times than before."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()

class Later(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["We will learn about", "them in detail", "in later videos."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()

class Remembering(AdvancedScene):
    def construct(self):
        happy = self.create_ninja('happy')
        self.play(FadeInFrom(happy, RIGHT))
        self.wait()
        self.play(self.change_ninja('thinking'))
        self.wait()
        self.play(self.change_ninja('happy'))
        self.wait()
        self.play(FadeOutAndShift(self.ninja, RIGHT))

class ComeIn(AdvancedScene):
    def construct(self):
        sc = ScreenGrabber(self)
        happy = self.create_ninja('happy')
        self.play(FadeInFrom(happy, RIGHT))
        sc.save()

class GoOut(AdvancedScene):
    def construct(self):
        happy = self.create_ninja('happy')
        self.add(happy)
        self.play(FadeOutAndShift(self.ninja, RIGHT))

class Agreeing(AdvancedScene):
    def construct(self):
        sc = ScreenGrabber(self)
        happy = self.create_ninja('happy')
        self.add(happy)
        self.play(self.change_ninja('yes'))
        sc.save()
        self.wait()
        self.play(self.change_ninja('happy'))

class Dunno(AdvancedScene):
    def construct(self):
        sc = ScreenGrabber(self)
        happy = self.create_ninja('happy')
        self.add(happy)
        self.play(self.change_ninja('dunno'))
        sc.save()
        self.wait()
        self.play(self.change_ninja('happy'))

class Thinking(AdvancedScene):
    def construct(self):
        sc = ScreenGrabber(self)
        happy = self.create_ninja('happy')
        self.add(happy)
        self.play(self.change_ninja('thinking'))
        sc.save()
        self.wait()
        self.play(self.change_ninja('happy'))
