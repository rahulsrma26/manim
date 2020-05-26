from manimlib.imports import *
from from_rahul.utils.colors import VSColors


class ExplainableTextObject:
    def __init__(self, text, hint, direction=DOWN):
        self.text = TextMobject(text)
        self.text.scale(1.5)
        self.braces = Brace(self.text, direction=direction).set_color(VSColors.class_name)
        self.hint = self.braces.get_text(hint).set_color(VSColors.comments)
        self.obj = Group(self.text, self.braces, self.hint)

        self.braces.add_updater(lambda d: d.next_to(self.text, direction))
        self.hint.add_updater(lambda d: d.next_to(self.braces, direction))
