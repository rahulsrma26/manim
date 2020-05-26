from manimlib.imports import *
from from_rahul.utils.advanced_scene import AdvancedScene
from from_rahul.utils.code_mobject import CodeMobject
from from_rahul.utils.cursor import Cursor


def RunCode(self: AdvancedScene, code: CodeMobject, sequence, gap=0.2, corner=0.2, color=WHITE):
    def Rect(obj):
        h = max(obj.get_height() + gap, corner*2.5)
        w = max(obj.get_width() + gap, corner*2.5)
        rect = RoundedRectangle(width=w, height=h, corner_radius=corner).move_to(obj)
        rect.set_stroke(width=0).set_fill(color=color, opacity=0.5)
        return rect

    rect = Rect(code.submobjects[sequence[0]])
    self.play(GrowFromCenter(rect))
    for idx in sequence:
        animations = []
        if isinstance(idx, list):
            animations = idx[1:]
            idx = idx[0]
        rect1 = Rect(code.submobjects[idx])
        self.play(*([ReplacementTransform(rect, rect1)] + animations))
        rect = rect1
    return rect
