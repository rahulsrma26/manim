#!/usr/bin/env python

from manimlib.imports import *
from from_rahul.ninja import Ninja
from from_rahul.utils import *
from from_rahul.table import Table

# python -m manim from_rahul\03_ifelse.py ComparisonOperators -c #151520 -pl
DIR = os.path.dirname(os.path.abspath(__file__))
SDIR = os.path.join(DIR, 'svgs')


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


class ComparisonOperators(AdvancedScene):
    def construct(self):
        operandsL = [('12', '11'), ('12', '12'), ('12', '123'), ('12', '13')]
        operandsR = [("'as'", "'an'"), ("'as'", "'as'"), ("'as'", "'ask'"), ("'as'", "'at'")]
        operators = [
            ('<', 'Less than'),
            ('<=', 'Less than or Equal to'),
            ('>', 'Greater than'),
            ('>=', 'Greater than or Equal to'),
            ('==', 'Equal to'),
            ('!=', 'Not equal to'),
        ]

        h, hu, info = self.define_word(
            "Comparison operators",
            [
                "Comparison operators takes two values and compares them.",
                "They return either \\texttt{True} or \\texttt{False}",
                "For \\texttt{str} they use lexicographical (dictionary) ordering.",
            ],
            fade=False,
            scale=1.3,
            reactions=['happy', 'thinking'])

        self.wait()
        self.play(FadeOut(info))

        texts = [[x, '..', y, '.....', a, '..', b, '.....']
            for (x, y), (a,b) in zip(operandsL, operandsR)]
        table = Table(
            [[f'\\texttt{{{t}}}'.replace("'","\\textquotesingle ") for t in row] for row in texts],
            widths=[1, 0.5, 1, 2.5, 1.2, 0.7, 1, 2],
            align='rrrlllll'
        )
        self.play(Write(table), run_time=5)
        msg = TextMobject('\\texttt{[Pause if you wanna take a closer look]}').scale(0.8)
        msg.to_edge(DOWN)
        self.play(FadeIn(msg), self.change_ninja('thinking'))

        for op, txt in operators:
            h1 = TextMobject(txt).scale(1.3).to_corner(UL, buff=1)
            hu1 = Underline(h1)
            self.play(ReplacementTransform(h, h1), ReplacementTransform(hu, hu1))
            h, hu = h1, hu1

            new_objs = []
            for i, (x, y) in enumerate(operandsL + operandsR):
                k = i*8 + 1 if i < 4 else (i-4)*8 + 5
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


class LogicalOperators(AdvancedScene):
    def construct(self):
        operators = [
            ('and', 'AND operator', 'If both the operands are true only then condition becomes true.'),
            ('or', 'OR operator', 'If both the operands are false only then condition becomes false.'),
            ('not', 'NOT operator', 'Used to reverse the logical state of its operand.'),
        ]

        h, hu, info = self.define_word(
            "Logical operators",
            [
                "Logical operators are used to combine conditional statements.",
                "They allows to make a decision based on multiple conditions."
            ],
            fade=False,
            scale=1.3,
            reactions=['happy', 'thinking'])

        self.wait()
        self.play(FadeOut(info))

        msg = TextMobject('\\texttt{[Pause if you wanna take a closer look]}').scale(0.8)
        msg.to_edge(DOWN)
        self.play(FadeIn(msg), self.change_ninja('thinking'))

        hi = TextMobject('.').next_to(hu, DOWN, buff=0.3)
        for op, txt, info in operators:
            h1 = TextMobject(txt).scale(1.3).to_corner(UL, buff=1)
            hu1 = Underline(h1)
            hi1 = TextMobject(f"\\textit{{{info}}}").scale(0.7).next_to(hu1, DOWN, aligned_edge=LEFT, buff=0.3)
            self.play(
                ReplacementTransform(h, h1),
                ReplacementTransform(hu, hu1),
                ReplacementTransform(hi, hi1))
            h, hu, hi = h1, hu1, hi1

            data = [
                ['Operand', 'Operator', 'Operand', 'Result'],
                ['False', '', 'False', ''],
                ['False', '', 'True', ''],
                ['True', '', 'False', ''],
                ['True', '', 'True', ''],
            ]
            if op == 'not':
                data = [row[1:] for row in data][:-2]
                for row in data[1:]:
                    row[0] = op
                    row[2] = str(eval(f"{op} {row[1]}"))
            else:
                for row in data[1:]:
                    row[1] = op
                    row[3] = str(eval(f"{row[0]} {op} {row[2]}"))

            table = Table(data, header=True, useTex=False).next_to(hi, DOWN, buff=0.5)
            table.set_x(-5 + table.get_width() / 2)

            div = 4 if op != 'not' else 3
            for i, obj in enumerate(table.submobjects):
                if hasattr(obj, 'tex_strings') and i%div == 0:
                    if obj.tex_strings[0] in ['True', 'False']:
                        color = MCOLORS.WildWasabi if obj.tex_strings[0] == 'True' else MCOLORS.PeekabooPeach
                        obj.set_color(color=color)
                self.play(Write(obj), run_time=0.2)

            self.wait(duration=3)
            fade_objs = [table]
            if op == 'not':
                fade_objs.extend([h, hu, hi, msg])
            self.play(*[FadeOut(x) for x in fade_objs])

        self.play(self.change_ninja('happy'))
        self.play(FadeOut(self.ninja))
        self.wait()


class OperatorPrecedence(AdvancedScene):
    def construct(self):
        h = TextMobject('Operator Precedence').scale(2.5)
        self.play(Write(h), DrawBorderThenFill(self.create_ninja('happy')))
        self.wait()
        self.play(FadeOut(h))
        table = Table([
                ['Operator', 'Description'],
                ['$($ $)$', 'Parentheses'],
                ['$**$', 'Exponentiation'],
                ['$*$ $/$ $//$ $\\%$', 'Multiplication \\& Divisions'],
                ['$+$ $-$', 'Addition \\& subtraction'],
                ['$<$ $<=$ $>$ $>=$ $==$ $!=$', 'Comparisons'],
                ['not', 'Logical NOT'],
                ['and', 'Logical AND'],
                ['or', 'Logical OR'],
                ['$=$', 'Assignment'],
            ],
            useTex=False,
            header=True,
            scale=0.9,
            rgap=0.2,
            widths=5).to_edge(LEFT)

        top = table.submobjects[3].get_y()
        btm = table.submobjects[-1].get_y()
        for obj in table.submobjects[3:]:
            h = (obj.get_y() - btm) / (top - btm)
            c = rgb_to_color([min(h*2,1), min(2-h*2,1), 0.3])
            # print(h, c)
            obj.set_color(color=c)

        ind = VGroup()
        ind.add(Rectangle(width=5, height=1).set_color_by_gradient([GREEN, YELLOW, RED]).set_opacity(1).rotate(-PI/2))
        ind.add(TextMobject('High', color=RED).scale(2).next_to(ind[0], UP))
        ind.add(TextMobject('Low', color=GREEN).scale(2).next_to(ind[0], DOWN))
        ind.scale(0.3).to_corner(UR, buff=1)

        for i, x in enumerate(table.submobjects):
            self.play(Write(x))
            if i == 2:
                self.play(self.change_ninja('thinking'), DrawBorderThenFill(ind))
        self.play(self.change_ninja('happy'))
        self.wait()
        self.play(*[FadeOut(x) for x in [table, self.ninja, ind]])
        self.wait()


class BinaryDecimals(AdvancedScene):
    def construct(self):
        self.play(DrawBorderThenFill(self.create_ninja('happy')))
        number = '123.45'
        n1 = TextMobject(number).scale(3)
        self.play(Write(n1))
        self.wait()
        nw = ' '.join(number)
        n2 = TextMobject(nw).scale(3.5)
        self.play(ReplacementTransform(n1, n2), self.change_ninja('thinking'))
        n3 = TexMobject(
            '10^2','10^1','10^0','.','10^{-1}','10^{-2}'
        ).scale(1.2).arrange_submobjects(RIGHT, buff=1)
        self.play(n2.to_edge, UP, 2)
        x_pos = n2.submobjects[0].submobjects[3].get_x()
        n3.set_x(n3.get_x() + x_pos - n3[3].get_x())
        self.play(Write(n3))
        self.wait()
        n4 = TexMobject(
            '1\\times 10^2 + 2\\times 10^1 + 3\\times 10^0'
            '+ 4\\times 10^{-1} + 5\\times 10^{-2}'
        ).scale(1).to_edge(DOWN, buff=2.5)
        n4.set_x(n4.get_x() + x_pos - n4.submobjects[0].submobjects[17].get_x())
        self.play(Write(n4))
        self.wait(duration=2)
        self.play(*[FadeOut(x) for x in [n2, n3, n4]], self.change_ninja('happy'))
        self.wait()

        f1 = TexMobject('\\frac{1}{3}').scale(3)
        self.play(Write(f1))
        f2 = TexMobject('\\frac{1}{3}').scale(2).to_edge(LEFT, buff=2)
        f3 = TexMobject(*[x for x in '= 0.333333333333'], '...').scale(2).to_edge(LEFT, buff=3)
        self.play(ReplacementTransform(f1, f2), self.change_ninja('thinking'))
        for k in f3.submobjects[:-1]:
            self.play(Write(k), run_time=0.3)
        self.play(Write(f3.submobjects[-1]), self.change_ninja('dunno'))
        self.wait()
        self.play(*[FadeOut(x) for x in [f2, f3]], self.change_ninja('happy'))
        self.wait()

        number = '101.01'
        n1 = TextMobject(number).scale(3)
        self.play(Write(n1))
        self.wait()
        nw = ' '.join(number)
        n2 = TextMobject(nw).scale(3.5)
        self.play(ReplacementTransform(n1, n2), self.change_ninja('thinking'))
        n3 = TexMobject(
            '2^2','2^1','2^0','.','2^{-1}','2^{-2}'
        ).scale(1.2).arrange_submobjects(RIGHT, buff=1)
        self.play(n2.to_edge, UP, 2)
        x_pos = n2.submobjects[0].submobjects[3].get_x()
        n3.set_x(n3.get_x() + x_pos - n3[3].get_x())
        self.play(Write(n3))
        self.wait()
        n4 = TexMobject(
            '1\\times 2^2 + 0\\times 2^1 + 1\\times 2^0 + 0\\times 2^{-1} + 1\\times 2^{-2}'
        ).scale(1).to_edge(DOWN, buff=2.5)
        # n4.set_x(n4.get_x() + x_pos - n4[3].get_x())
        n4.set_x(n4.get_x() + x_pos - n4.submobjects[0].submobjects[14].get_x())
        self.play(Write(n4))
        self.wait(duration=2)
        self.play(*[FadeOut(x) for x in [n2, n3, n4]], self.change_ninja('happy'))
        self.wait()

        f1 = TexMobject('\\frac{1}{3}').scale(3)
        self.play(Write(f1))
        f2 = TexMobject('\\frac{1}{3}').scale(2).to_edge(LEFT, buff=2)
        bin1 = TexMobject(*[x for x in '= 0.010101010101'], '...').scale(2).to_edge(LEFT, buff=3)
        self.play(ReplacementTransform(f1, f2), self.change_ninja('thinking'))
        for k in bin1.submobjects[:-1]:
            self.play(Write(k), run_time=0.3)
        self.play(Write(bin1.submobjects[-1]), self.change_ninja('dunno'))
        self.wait()
        faded_objects = bin1.submobjects[:1] + bin1.submobjects[7:]
        self.play(*[FadeOut(x) for x in faded_objects], self.change_ninja('thinking'))
        bin1.remove(*faded_objects)
        frac1 = TexMobject('1/3').scale(2).to_edge(LEFT, buff=3)
        self.play(ReplacementTransform(f2, frac1), bin1.to_edge, RIGHT, 4)
        self.play(frac1.to_edge, UP, {"buff": 1.5}, bin1.to_edge, UP, {"buff": 1.5})

        bin2 = bin1.copy().to_edge(UP, buff=3)
        frac2 = frac1.copy().to_edge(UP, buff=3)
        self.play(TransformFromCopy(frac1, frac2), TransformFromCopy(bin1, bin2))
        frac2.add(TextMobject('$+$').scale(2).next_to(frac2, LEFT, buff=0.3))
        bin2.add(TextMobject('$+$').scale(2).next_to(bin2, LEFT, buff=0.3))
        self.play(FadeIn(frac2[-1]), FadeIn(bin2[-1]))

        bin3 = bin2.copy().to_edge(UP, buff=4.5)
        frac3 = frac2.copy().to_edge(UP, buff=4.5)
        self.play(TransformFromCopy(frac2, frac3), TransformFromCopy(bin2, bin3))
        ul1 = Underline(frac3)
        ul2 = Underline(bin3).set_y(ul1.get_y())
        self.play(FadeIn(ul1), FadeIn(ul2))

        res1 = TextMobject('1').scale(2).next_to(ul1, DOWN, buff=0.3)
        res2 = TextMobject('0.1111').scale(2).next_to(ul2, DOWN, buff=0.3)
        res2.set_x(bin1.get_x())
        self.play(Write(res1), Write(res2), self.change_ninja('surprised'))
        self.wait()
        self.play(self.change_ninja('happy'))
        self.wait()
        self.play(*[FadeOut(x) for x in [
            frac1, frac2, frac3, bin1, bin2, bin3, ul1, ul2, res1, res2, self.ninja]])
        self.wait()



class Recap(AdvancedScene):
    def construct(self):
        # # sc = ScreenGrabber(self)
        self.create_slide(
            "What we learned today?",
            [
                "Comparison Operators",
                "if, if-else and elif statements",
                "Nested if-else",
                "Logical Operators",
                "Operator Precedence",
                "Single line if-else",
                "Top beginner mistakes",
            ],
            animation=DrawBorderThenFill,
            # screenshot=sc,
            reactions=['happy', 'thinking'])
        self.wait()

        objs = self.define_word(
            "Practice Makes Progress",
            [
                "Checkout source code for examples.",
                "Assignments related to the tutorial.",
                "[Links are in the description.]",
            ],
            # screenshot=sc,
            reactions=['happy', 'surprised'])
        self.wait()
        self.play(*[FadeOut(x) for x in objs])

        # sc.save()

        end = TextMobject("Thanks for watching!").scale(1.8)
        self.play(Write(end), self.change_ninja('cool'))
        self.wait(duration=2.5)
        self.play(*[FadeOut(x) for x in [end, self.ninja]])
        self.wait()


class PeekAssociativity(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        info = TextMobject("This is called", "associativity of", "the operator.", fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()

class RightAssociative(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        info = TextMobject("** operator is", "right associative.", fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()

class Abs(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        info = TextMobject("abs() is same as", "$|x|$ in maths.", fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()

class ShortcutComments(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        info = TextMobject(
            "You can use \\texttt{Ctrl + /}",
            "key in VSCode to make", "current line a comment",
            fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()

class ShortCircuiting(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        info = TextMobject("This is called", "Short Circuiting.", fill_color="#151520", color="#151520").arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6, gap=0.8)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()

class Confused(AdvancedScene):
    def construct(self):
        happy = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(happy, RIGHT))
        self.wait()
        confused = self.create_ninja('confused', edge=RIGHT)
        self.play(ReplacementTransform(happy, confused))
        self.wait(duration=2)
        self.play(FadeOutAndShift(confused, RIGHT))

class UsingQuote(AdvancedScene):
    def construct(self):
        ninja = self.create_ninja('happy', edge=RIGHT)
        self.play(FadeInFrom(ninja, RIGHT))
        info = TextMobject("using (\") to", "print (\\textquotesingle) inside", fill_color="#151520", color="#151520")
        info.arrange_submobjects(DOWN).scale(0.7)
        rect, tail = ninja.get_speech(info, buff=0.6)
        self.play(DrawBorderThenFill(rect))
        self.play(GrowFromCenter(tail), Write(info))
        self.wait()
        self.play(FadeOutAndShift(ninja, RIGHT))
        self.play(*[FadeOutAndShift(x, RIGHT) for x in [info, rect, tail]])
        self.wait()