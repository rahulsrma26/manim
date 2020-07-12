#!/usr/bin/env python

import os
from manimlib.imports import *

# python -m manim from_rahul\table.py Test -c #151520 -pl

class Table(VGroup):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        header = kwargs.pop('header', False)
        rowwise = kwargs.pop('rowwise', True)
        useTex = kwargs.pop('useTex', True)
        scale = kwargs.pop('scale', 1)
        heights = kwargs.pop('heights', 0.5)
        widths = kwargs.pop('widths', 1)
        cgap = kwargs.pop('cgap', 0.3)
        rgap = kwargs.pop('rgap', 0.2)
        alignment = kwargs.pop('align', 'c')

        rows = len(data)
        cols = max([len(row) for row in data])
        col_width = widths if isinstance(widths, list) else [widths]*cols
        row_height = heights if isinstance(heights, list) else [heights]*rows
        alignments = alignment if len(alignment) > 1 else alignment*cols

        objs = []
        for r, row in enumerate(data):
            robjs = []
            for c, txt in enumerate(row):
                obj = TexMobject(txt) if useTex else TextMobject(txt)
                obj.scale(scale)
                col_width[c] = max(obj.get_width(), col_width[c])
                row_height[r] = max(obj.get_height(), row_height[r])
                robjs.append(obj)
            objs.append(robjs)

        x, y = 0, 0
        for r, row in enumerate(objs):
            for c, obj in enumerate(row):
                if alignments[c] == 'c':
                    obj.set_x(x).set_y(y)
                elif alignments[c] == 'r':
                    obj.set_x(x + col_width[c] - obj.get_width()/2).set_y(y)
                else:
                    obj.set_x(x + obj.get_width()/2).set_y(y)
                self.add(obj)
                x += col_width[c] + cgap
            if header and r == 0:
                ul = Underline(self)
                ul.set_width(x)
                self.add(ul)
                y -= rgap
            x = 0
            y -= row_height[r] + rgap

        self.center()
        self.rows = rows
        self.cols = cols
        self.text_objects = objs

        # def change_cell(self, r, c, text, scene:Scene):
        #     obj = self.text_objects[r][c]
        #     new = 


class Test(Scene):
    def construct(self):
        table = Table([
                ['h1', 'h2', 'h3'],
                ['a11', 'a12', 'a13'],
                ['b11', 'b12', 'b13'],
            ],
            alignment='right',
            header=True
        )

        self.play(Write(table))
        self.wait()
