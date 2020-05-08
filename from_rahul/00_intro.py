#!/usr/bin/env python
from manimlib.imports import *
from rahul.ninja import Ninja
from rahul.utils import *

# python -m manim rahul\00_intro.py WhatIsPython -c #151520 -pl
# python -m manim rahul\00_intro.py Logo -t -s

DIR = os.path.dirname(os.path.abspath(__file__))
SVG_DIR = os.path.join(DIR, 'svgs')

class Logo(AdvancedScene):
    def construct(self):
        t = TextMobject("\\texttt{csglitz}").scale(2.5)
        w = Ninja("wave")
        c = Group(t, w).arrange_submobjects(RIGHT, buff=1)
        self.play(DrawBorderThenFill(w), Write(t))
        w.wave(self, 1)
        self.play(FadeOut(t), ReplacementTransform(w, Ninja("happy").to_corner(DR)))
        self.wait()


class WhatIsPython(AdvancedScene):
    def construct(self):
        self.create_slide(
            "What is Python?",
            [
                "High-level general-purpose programming language",
                "Fastest growing programing language",
                "Used by Engineers, Mathematicians, Data Analyst, Scientist ...",
                "Supports Procedural, OOP and Functional",
                "One of the most wanted languages by the developers (\\& loved)",
            ],
            screenshot=ScreenGrabber(self),
            question="What is python?",
            reactions=['happy', 'dunno', 'thinking'])
        self.wait()

class WhyPython(AdvancedScene):
    def construct(self):
        self.create_slide(
            "Why Python?",
            [
                "Easy and Quick yet Powerful",
                "Free, Open Source and can be used in all major platforms",
                "Batteries included",
                "GUI/Web/Mobile app, Backend services, Automation, ",
                "Data Analysis, AI, Machine Learning, Testing ...",
                "Huge library available (pypi 232K+)",
                "Goto language for Data science and Machine learning",
                "Large community for helping you out"
            ],
            screenshot=ScreenGrabber(self),
            question="Why Python?",
            reactions=['happy', 'dunno', 'thinking'])
        self.wait()

class WhenNotPython(AdvancedScene):
    def construct(self):
        self.create_slide(
            "When NOT to use Python?",
            [
                "System level softwares",
                "Creating low level libraries for number crunching",
                "Performance is critical",
                "Robustness is critical",
            ],
            screenshot=ScreenGrabber(self),
            question="When not Python?",
            reactions=['happy', 'scared', 'thinking'])
        self.wait()

class Companies(AdvancedScene):
    def construct(self):
        self.create_slide(
            "Which companies use Python?",
            [
                "Google, Facebook, Microsoft, Amazon …",
                "Many tech startups",
                "Tensorflow, PyTorch, Django, scikit, OpenCV, Selenium …",
                "Instagram, Spotify, Netflix, Dropbox, Pinterest, Reddit …",
            ],
            screenshot=ScreenGrabber(self),
            question="Companies? Industries?",
            reactions=['happy', 'dunno', 'thinking'])
        self.wait()

class Jobs(AdvancedScene):
    def construct(self):
        self.create_slide(
            "What job profiles can I get into after learning it?",
            [
                "Software developer",
                "Quality Assurance Engineer",
                "Backend Developer (Server APIs)",
                "Data Analyst, Data Scientist, Machine Learning Engineer …",
                "Higher salaries than Java, C++ or C\\#",
            ],
            screenshot=ScreenGrabber(self),
            question="Jobs? Career options?",
            reactions=['happy', 'dunno', 'cool'])
        self.wait()

class WhereLearn(AdvancedScene):
    def construct(self):
        self.create_slide(
            "Where can I learn?",
            [
                "Python-3 youtube tutorial series",
                "www.python.org/doc",
                "www.programiz.com",
                "www.learnpython.org",
                "Practice python online on repl.it",
                "Many tutorials build by others",
            ],
            screenshot=ScreenGrabber(self),
            question="How to learn?",
            reactions=['happy', 'dunno', 'happy'])
        self.wait()

class WhoAmI(AdvancedScene):
    def construct(self):
        self.create_slide(
            "Who am I?",
            [
                "Masters in Computer Science from IISc, Bangalore",
                "GATE AIR 35, JEST top 30 (Chennai Mathematical Institute)",
                "Worked with one of the top 5 tech MNC",
                "Worked on cutting edge technologies in startup",
                "Cracked online contests",
                "Interviewed candidates from top colleges for hiring",
            ],
            screenshot=ScreenGrabber(self),
            question="Who are you?",
            reactions=['happy', 'dunno', 'thinking'])
        self.wait()

class Projects(AdvancedScene):
    def construct(self):
        sc = ScreenGrabber(self)
        self.create_slide(
            "This python tutorial series includes",
            [
                "Collecting data from web scraping",
                "Building ML model",
                "Build a web app",
                "Backend server",
                "GUI app (Game)",
                "Interactive demo using OpenCV",
            ],
            screenshot=sc,
            question="Tutorial projects?",
            reactions=['happy', 'dunno', 'surprised'])

        sc.save()
        ninja = Ninja('cool').to_corner(DR)

        end = TextMobject("Thanks for watching!").scale(1.8)
        self.play(Write(end), ReplacementTransform(self.ninja, ninja))
        self.wait()
        self.play(*[FadeOut(x) for x in [end, ninja]])
        self.wait()
