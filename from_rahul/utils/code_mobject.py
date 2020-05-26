from manimlib.imports import *

class CodeMobject(TexMobject):
    CONFIG = {
        "alignment": "\\centering",
        "arg_separator": " ",
    }

    def get_indentation(self, string):
        for i, c in enumerate(string):
            if c != ' ':
                return i
        return 0

    def get_indexes(self, string):
        result, idx = [], 0
        for i, c in enumerate(string):
            if c != ' ':
                result.append(idx)
                idx += 1
            else:
                result.append(-1)
        # print(string, result)
        return result

    KEYWORDS = set(("False await else import pass None break except in raise True class" \
        " finally is return and continue for lambda try as def from nonlocal while" \
        " assert del global not with async elif if or yield").split())
    KEYWORD_COLOR = "#ffffaf"

    def set_color(self, obj, code):
        indexes = self.get_indexes(code)
        for key in self.KEYWORDS:
            idx, n = code.find(key), len(key)
            if idx >= 0 and (idx == 0 or code[idx - 1] == ' ') \
                and (idx + n < len(code) or code[idx + n] == ' '):
                for i in range(idx, idx + n):
                    obj.submobjects[indexes[i]].set_color(color=self.KEYWORD_COLOR)
        # print(words)

    def __init__(self, *code_string, **kwargs):
        self.code_font = kwargs.pop('code_font', True)
        self.code_coloring = kwargs.pop('code_coloring', True)
        text_string = []
        indentations = []
        for code in code_string:
            text = code.replace('\\', '$\\backslash$').replace("'", "\\textquotesingle ")
            if self.code_font:
                text = "\\texttt{" + text + "}"
            else:
                text = "\\text{" + text + "}"
            text_string.append(text)
            print(text_string)
            indentations.append(self.get_indentation(code))
            print(indentations[-1])
        super().__init__(*text_string, **kwargs)
        self.arrange_submobjects(DOWN, aligned_edge=LEFT)
        width = max([max([y.get_width() for y in x.submobjects]) for x in self.submobjects])
        # print('self.submobjects', len(self.submobjects))
        for obj, ind, code in zip(self.submobjects, indentations, code_string):
            # print(len(obj.submobjects), obj.tex_string)
            # print(code, max(a) if a else 0)
            # print(len(obj.submobjects), max(self.get_indexes(code_string[ind])))
            obj.set_x(obj.get_x() + width*ind)
            if self.code_coloring:
                self.set_color(obj, code)
