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

# python -m manim from_rahul\06_list.py Intro -pl
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
            "Basics of list",
            [
                "Create, modify, and iterate lists, len()",
                "How references work",
                "id() function and identity operators",
                "copy() and list slicing",
                "list() constructor",
                "Adding: append(), insert(), and extend()",
                "Removing: remove(), pop(), del, and clear()",
                "+ (concatenation) and * (repeat) operators"
            ],
            write_speed=35,
            reactions=['happy', 'thinking'])
        self.wait()
        self.play(*[FadeOut(x) for x in leaving_objects])

        leaving_objects = self.create_slide(
            "Advanced methods and topics",
            [
                "count(), index() and membership operators",
                "reverse(), sort() and comparison operators",
                "Sequence packing and unpacking",
                "enumerate() and zip()",
                "Modifying multiple elements using slice",
                "split() and join() for string list",
                "List comprehensions"
            ],
            write_speed=35,
            reactions=['happy', 'thinking'])
        self.wait()
        leaving_objects.append(self.ninja)
        self.play(*[FadeOut(x) for x in leaving_objects])
        self.wait()

def Darker(color, factor=0.5):
    return rgb_to_color(color_to_rgb(color)*factor)

def Brighter(color, factor=1.5):
    return rgb_to_color(color_to_rgb(color)*factor)

class Tag(SVGMobject):
    CONFIG = {
        "sheen_direction": RIGHT,
    }
    def __init__(self, color=RED, thread_color=WHITE, thread_width=2, flipped=False):
        filepath = os.path.join(SDIR, "tag.svg")
        if flipped:
            self.sheen_direction = LEFT
        super().__init__(filepath)
        if flipped:
            self.flip()
        self.scale(0.33)
        # colors = [color, Darker(color)]
        for obj in self.submobjects[1::2]:
            obj.set_fill(
                color=color, opacity=1
            ).set_stroke(
                color=None, width=0, opacity=0)
        self.submobjects[1].set_color_by_gradient([color, Darker(color)])
        # self.submobjects[1].set_colors_by_radial_gradient(center=np.array([0, 0, 0]), radius=5, inner_color=color, outer_color=Darker(color))
        for obj in self.submobjects[0::2]:
            obj.set_fill(
                color=None, opacity=0
                ).set_stroke(
                color=thread_color, width=thread_width, opacity=1)

class Table3D(VGroup):
    def __init__(self):
        super().__init__()
        color = MCOLORS.WildWasabi
        plane = Polygon([-6,-1,0], [6,-1,0], [4,1,0], [-4,1,0], sheen_direction=UP)
        plane.set_stroke(color=None, width=0, opacity=0).set_fill(color=None, opacity=1)
        plane.set_color_by_gradient([color, Darker(color, 0.2)])
        self.add(plane)
        front = Polygon([-6,-1,0], [-6,-1.2,0], [6,-1.2,0], [6,-1,0])
        front.set_stroke(color=None, width=0, opacity=0).set_fill(color=Brighter(color), opacity=1)
        self.add(front)


# python -m manim from_rahul\06_list.py References -pl
class References(AdvancedScene):
    def construct(self):
        h, u, info = self.define_word(
            "Object References",
            [
                "All variables in python are object references.",
                "The objects are stored in the memory, and",
                "contain associated values \\& methods.",
                "While references just store the address of the",
                "objects not the values."
            ],
            question="What are references?",
            speed=19,
            scale=1.3,
            reactions=['happy', 'dunno', 'thinking', 'confused'])
        self.wait(duration=3)
        self.play(FadeOut(info))
        self.play(self.change_ninja('thinking'))
        plane = Table3D()
        text_memory = TextMobject("Memory").set_x(-3).set_y(1.2)
        self.play(FadeIn(plane), Write(text_memory))
        line_1 = TextMobject("\\texttt{a = \\textquotesingle by\\textquotesingle}", color=MCOLORS.PeekabooPeach)
        line_1.move_to(plane, aligned_edge=LEFT).set_y(-line_1.get_height() / 2 - 1.5)
        self.play(Write(line_1))
        text_1 = TextMobject("\\texttt{\\textquotesingle by\\textquotesingle}").scale(2).set_x(-2)
        self.play(DrawBorderThenFill(text_1))
        tag_a = Tag().move_to(text_1.get_corner(DL)).shift([-.4, 0, 0])
        self.play(Write(tag_a))
        text_a = TextMobject("$a$", color=MCOLORS.Background).move_to(tag_a[-1])
        self.play(Write(text_a))
        self.wait()
        line_2 = TextMobject("\\texttt{b = a}", color=MCOLORS.PeekabooPeach)
        line_2.move_to(plane, aligned_edge=LEFT).set_y(-line_2.get_height() / 2 - 2)
        self.play(Write(line_2))
        tag_b = Tag(color=BLUE, flipped=True).move_to(text_1.get_corner(DR)).shift([.4, 0, 0])
        self.play(Write(tag_b))
        text_b = TextMobject("$b$", color=MCOLORS.Background).move_to(tag_b[-1])
        self.play(Write(text_b))
        self.wait()
        line_3 = TextMobject("\\texttt{b = a + \\textquotesingle te\\textquotesingle}", color=MCOLORS.PeekabooPeach)
        line_3.move_to(plane, aligned_edge=LEFT).set_y(-line_3.get_height() / 2 - 2.5)
        self.play(Write(line_3))
        text_2 = TextMobject("\\texttt{\\textquotesingle byte\\textquotesingle}")
        text_2.scale(2).move_to(text_1, aligned_edge=UP).set_x(2)
        self.play(DrawBorderThenFill(text_2))
        vg_b = VGroup(tag_b, text_b)
        self.play(vg_b.shift, [4.3, 0, 0])
        self.wait()
        line_4 = TextMobject("\\texttt{a = b}", color=MCOLORS.PeekabooPeach)
        line_4.move_to(plane, aligned_edge=LEFT).set_y(-line_4.get_height() / 2 - 3)
        self.play(Write(line_4))
        vg_a = VGroup(tag_a, text_a)
        self.play(vg_a.shift, [3.5, 0, 0])
        self.wait()
        self.play(FadeOutAndShift(text_1, UP), self.change_ninja('happy'))
        self.wait()
        self.play(*[FadeOut(x) for x in [tag_a, tag_b, text_2, text_a, text_b, line_1, line_2, line_3, line_4]])
        self.wait()
        line_1 = TextMobject("\\texttt{a = [1, 2, 3]}", color=MCOLORS.PeekabooPeach)
        line_1.move_to(plane, aligned_edge=LEFT).set_y(-line_1.get_height() / 2 - 1.5)
        self.play(Write(line_1))
        text_1 = TextMobject("\\texttt{[1, 2, 3]}").scale(2)
        self.play(DrawBorderThenFill(text_1))
        tag_a = Tag().move_to(text_1.get_corner(DL)).shift([-.5, -.2, 0])
        self.play(Write(tag_a))
        text_a = TextMobject("$a$", color=MCOLORS.Background).move_to(tag_a[-1])
        self.play(Write(text_a))
        self.wait()
        line_2 = TextMobject("\\texttt{b = a}", color=MCOLORS.PeekabooPeach)
        line_2.move_to(plane, aligned_edge=LEFT).set_y(-line_2.get_height() / 2 - 2)
        self.play(Write(line_2))
        tag_b = Tag(color=BLUE, flipped=True).move_to(text_1.get_corner(DR)).shift([.5, -.2, 0])
        self.play(Write(tag_b))
        text_b = TextMobject("$b$", color=MCOLORS.Background).move_to(tag_b[-1])
        self.play(Write(text_b))
        self.wait()
        line_3 = TextMobject("\\texttt{b[1] = 5}", color=MCOLORS.PeekabooPeach)
        line_3.move_to(plane, aligned_edge=LEFT).set_y(-line_3.get_height() / 2 - 2.5)
        self.play(Write(line_3))
        self.wait()
        text_2 = TextMobject("\\texttt{[1, 5, 3]}")
        text_2.scale(2).move_to(text_1)
        self.play(ReplacementTransform(text_1, text_2), Flash(text_2[0].submobjects[3], flash_radius=0.6), self.change_ninja('surprised'))
        self.play(self.change_ninja('happy'))
        leaving = [tag_a, tag_b, text_2, text_a, text_b, line_1, line_2, line_3, self.ninja, plane, text_memory, h, u]
        self.play(*[FadeOut(x) for x in leaving])
        self.wait()

def get_box(val):
    value = TextMobject(f"\\texttt{val}").scale(4)
    value.add_background_rectangle(stroke_opacity=1, stroke_width=1, buff=0.5)
    return value

class Variable(VGroup):
    def __init__(self, text, value, transform=None, **kwargs):
        super().__init__(**kwargs)
        self.transform = transform
        self.text = TextMobject(f"\\texttt{{{text}}}")
        self.add(self.text)
        self.equals = TextMobject("\\texttt{=}")
        self.add(self.equals)
        self.value = TextMobject(f"\\texttt{{{value}}}")
        self.add(self.value)
        self.arrange_submobjects()
        if transform:
            transform(self)

    def change_value(self, value):
        old_value = self.value
        self.remove(self.value)
        self.value = TextMobject(f"\\texttt{{{value}}}")
        if self.transform:
            self.transform(self.value)
        self.value.move_to(old_value, aligned_edge=LEFT)
        # self.add(self.value)
        return ReplacementTransform(old_value, self.value)

# python -m manim from_rahul\06_list.py Example -pl
class Example(AdvancedScene):
    def construct(self):
        self.play(DrawBorderThenFill(self.create_ninja('thinking')))
        array = VGroup(*[get_box(x) for x in range(1, 5)])
        array.arrange_submobjects(RIGHT)
        self.play(DrawBorderThenFill(array))
        code = CodeMobject(
            "a = [1, 2, 3, 4]",
            "for i in range(len(a)):",
            "    if a[i] % 2 == 0:",
            "        a.pop(i)").scale(1.5).next_to(array, DOWN)
        self.play(DrawBorderThenFill(code[0]))
        codeG = VGroup(*code[2:])
        self.play(Type(codeG))
        index = VGroup(*[TextMobject(f"\\texttt{x}", color=MCOLORS.WildWasabi).scale(1.5) for x in range(4)])
        for src, dst in zip(index, array):
            src.next_to(dst, TOP, buff=0.1)
        self.play(Write(index))
        ub = BraceLabel(index, "index", UP, label_scale=1.6)
        for x in ub:
            x.set_color(color=MCOLORS.WildWasabi)
        self.play(GrowFromCenter(ub))
        self.wait()
        idx = Variable('i', 0, lambda x: x.scale(2)).to_corner(DL, 1)
        self.play(Write(idx))
        self.play(Flash(index[0], flash_radius=0.5))
        self.play(Indicate(array[0]))
        self.wait()
        self.play(Flash(index[1], flash_radius=0.5), idx.change_value(1))
        self.play(Indicate(array[1]))
        self.wait()
        self.play(FadeOut(array[1]))
        array.remove(array[1])
        self.play(array[1].next_to, array[0])
        self.play(array[2].next_to, array[1])
        self.wait()
        self.play(Flash(index[2], flash_radius=0.5), idx.change_value(2))
        self.play(Indicate(array[2]))
        self.wait()
        self.play(FadeOut(array[2]))
        array.remove(array[2])
        self.wait()
        self.play(Flash(index[3], flash_radius=0.5), idx.change_value(3))
        qm = TextMobject("\\texttt{?}").scale(4)
        qm.set_x(index[3].get_x()).set_y(array[1].get_y())
        self.play(SpinInFromNothing(qm), self.change_ninja('scared'))
        self.play(WiggleOutThenIn(qm))
        self.wait()
        objs = [array, index, ub, qm, idx, idx.value, code]
        self.play(*[FadeOut(x) for x in objs])
        self.play(self.change_ninja('thinking'))
        # return
        # -----------------------
        array = VGroup(*[get_box(x) for x in range(1, 5)])
        array.arrange_submobjects(RIGHT)
        self.play(DrawBorderThenFill(array))
        index = VGroup(*[TextMobject(f"\\texttt{x}", color=MCOLORS.WildWasabi).scale(1.5) for x in range(4)])
        for src, dst in zip(index, array):
            src.next_to(dst, TOP, buff=0.1)
        self.play(Write(index))
        ub = BraceLabel(index, "index", UP, label_scale=1.6)
        for x in ub:
            x.set_color(color=MCOLORS.WildWasabi)
        self.play(GrowFromCenter(ub))
        self.wait()
        # idx = Variable('i', 3, lambda x: x.scale(2)).to_corner(DL, 1)
        # self.play(Write(idx))
        self.play(Flash(index[3], flash_radius=0.5))
        self.play(Indicate(array[3]))
        self.wait()
        self.play(FadeOut(array[3]))
        array.remove(array[3])
        self.wait()
        self.play(Flash(index[2], flash_radius=0.5))
        self.play(Indicate(array[2]))
        self.wait()
        self.play(Flash(index[1], flash_radius=0.5))
        self.play(Indicate(array[1]))
        self.wait()
        self.play(FadeOut(array[1]))
        array.remove(array[1])
        self.play(array[1].next_to, array[0])
        self.wait()
        self.play(Flash(index[0], flash_radius=0.5))
        self.play(Indicate(array[0]))
        self.wait()
        self.play(FadeOut(index), FadeOut(ub))
        self.play(array.center, self.change_ninja('happy'))
        self.wait()
        objs = [array, self.ninja]
        self.play(*[FadeOut(x) for x in objs])
        self.wait()

# python -m manim from_rahul\06_list.py Comparison -pl
class Comparison(AdvancedScene):
    def construct(self):
        operands = [
            ('[]', '[1]'),
            ('[1]', '[1, 2]'),
            ('[1, 2]', '[1, 1]'),
            ('[1, 2]', '[1, 2]'),
            ('[1, 2]', '[1, 3]'),
            ('[1, 2]', '[1, 2, 1]')]
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


# python -m manim from_rahul\06_list.py Outro -pl
class Outro(AdvancedScene):
    def construct(self):
        objs = self.define_word(
            "Practice Makes Progress",
            [
                "Links to the example source",
                "code and assignments are",
                "in the description.",
            ],
            scale=1.5,
            reactions=['happy', 'cool', 'cool'])
        self.wait()
        self.play(*[FadeOut(x) for x in objs])

        # sc.save()

        end = TextMobject("Thanks", "for", "watching!").arrange_submobjects(DOWN).scale(1.8)
        self.play(Write(end))
        self.wait(duration=3)
        self.play(*[FadeOut(x) for x in [end, self.ninja]])
        self.wait()


# python -m manim from_rahul\06_list.py Rearrangement -t -pm -r 1080
class Rearrangement(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["This way rearrangement after delete", "can never effect future elements."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


# python -m manim from_rahul\06_list.py Rearrange -t -pm -r 1080
class Rearrange(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["Let's rearrange the code."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.8)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


# python -m manim from_rahul\06_list.py Epoch -t -pm -r 1080
class Epoch(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["Check `Epoch'", "in the description."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.8)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


# python -m manim from_rahul\06_list.py IndexError -t -pm -r 1080
class IndexError(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["Index Error"]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


# python -m manim from_rahul\06_list.py Fstring -t -pm -r 1080
class Fstring(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["Check tutorial 02", "for f-string."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.8)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


# python -m manim from_rahul\06_list.py EqualTo -t -pm -r 1080
class EqualTo(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["Using $=$ after variable will", "print both variable name and value."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


# python -m manim from_rahul\06_list.py ConvertMarks -t -pm -r 1080
class ConvertMarks(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["We need marks", "as a list of integers."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


# python -m manim from_rahul\06_list.py ShoppingList -t -pm -r 1080
class ShoppingList(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["We are trying to create", "a shopping list."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


# python -m manim from_rahul\06_list.py EnumerateZip -t -pm -r 1080
class EnumerateZip(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["enumerate is taking the", "inputs from zip and returning", "them alongside counter"]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.6)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


# python -m manim from_rahul\06_list.py Timeline -t -pm -r 1080
class Timeline(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        ninja = self.create_ninja('thinking')
        # self.play(FadeInFrom(ninja, RIGHT))
        txt = ["Check the", "description for", "the timeline."]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.6)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait(duration=3)
        # self.play(FadeOutAndShift(self.ninja, UP))
        self.play(*[FadeOutAndShift(x, UP) for x in [info, rect, tail]])

# python -m manim from_rahul\06_list.py Join -t -pm -r 1080
class Join(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["join will return", "a single string object"]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.6)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


# python -m manim from_rahul\06_list.py Sorcery -t -pm -r 1080
class Sorcery(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["What kind of sorcery is this?"]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.6)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info), self.change_ninja('scared', edge=RIGHT))
        self.wait()
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


# python -m manim from_rahul\06_list.py ChallengeAccepted -t -pm -r 1080
class ChallengeAccepted(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["Challenge Accepted!"]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.6)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info), self.change_ninja('cool', edge=RIGHT))
        self.wait(duration=2)
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


# python -m manim from_rahul\06_list.py PackUnpack -t -pm -r 1080
class PackUnpack(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        txt = ["If we have written \\texttt{c = [a]}", "then $c$ would have been \\texttt{[[1, 2, 3]]}"]
        info = TextMobject(*txt, fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.6)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info), self.change_ninja('cool', edge=RIGHT))
        self.wait(duration=2)
        self.play(FadeOutAndShift(self.ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])


# python -m manim from_rahul\06_list.py ComeIn -t -m -r 1080
class ComeIn(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        sc = ScreenGrabber(self)
        happy = self.create_ninja('happy')
        self.play(FadeInFrom(happy, RIGHT))
        sc.save()

class No(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        sc = ScreenGrabber(self)
        self.add(self.create_ninja('happy'))
        self.play(self.change_ninja('no'))
        sc.save()

class Yes(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        sc = ScreenGrabber(self)
        self.add(self.create_ninja('no'))
        self.play(self.change_ninja('yes'))
        sc.save()

class GoOut(AdvancedScene):
    CONFIG = AdvancedScene.TRANSPARENT
    def construct(self):
        self.add(self.create_ninja('yes'))
        self.play(self.change_ninja('happy'))
        self.play(FadeOutAndShift(self.ninja, RIGHT))


