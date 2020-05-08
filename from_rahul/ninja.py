#!/usr/bin/env python

import os
from manimlib.imports import *

NINJA_DIR = os.path.dirname(os.path.abspath(__file__))

def get_blink_fn(m):
    def blink(m, dt):
        blink.time += dt
        if 3.5 < blink.time < 4:
            gap = math.pi * abs(blink.time - 3.75) / 0.625
            print(gap)
            m.set_height(blink.height*math.sin(gap))
        elif blink.time > 4:
            m.set_height(blink.height)
            blink.time = 0
    blink.time = 0
    blink.height = m.get_height()*2
    return blink

class Ninja(SVGMobject):
    BODY_MAP = {
        "face": [5],
        "body": [4],
        "hands": [13, 14],
        "band": [6],
        "ribbons": [2, 3],
        "skin": [8],
        "eyes": [9, 10],
        "pupils": [11, 12],
        "sword": [0],
        "handle": [1],
        "mouth": [7],
        "ai": [15, 16]
    }
    COLOR_MAP = {
        "face": "#41464E",
        "body": "#363C46",
        "hands": "#27323A",
        "band": "#E36566",
        "ribbons": "#D2606F",
        "skin": "#F6CDB5",
        "eyes": "#000000",
        "pupils": "#FFFFFF",
        "sword": "#A58B7D",
        "handle": "#72565F",
        "mouth": "#766D57",
        "ai": "#E36566"
    }
    LEADER_MAP = {**COLOR_MAP, **{
        "face": "#414E46",
        "body": "#394940",
        "hand": "#313E36",
    }}

    def __init__(self, emotion='happy', leader=False):
        self.emotion = emotion
        self.leader = leader
        self.blinking_functions = []
        filepath = os.path.join(NINJA_DIR, "ninja", f"{emotion}.svg")
        super().__init__(filepath)
        # self.svg = SVGMobject(filepath)
        for obj in self.submobjects:
            obj.set_stroke(color=WHITE, width=0).set_fill(color=RED, opacity=0)

        total = len(self.submobjects)
        self.body = {}
        for part, indexes in Ninja.BODY_MAP.items():
            self.body[part] = [self.submobjects[i] for i in indexes if i < total]
            for idx in indexes:
                if idx < total:
                    color = (Ninja.LEADER_MAP if leader else Ninja.COLOR_MAP)[part]
                    self.submobjects[idx].set_fill(color=color, opacity=1)
                    # if hasattr(self.submobjects[idx], 'svg_attributes'):
                    #     print('A', self.svg.submobjects[idx].svg_attributes)

        if emotion == 'confused':
            self.body['eyes'][0].add_updater(lambda m, dt: m.rotate(-3*dt))
            self.body['eyes'][1].add_updater(lambda m, dt: m.rotate(3*dt))

        # if emotion == 'wave':
        #     print(OUT)
        #     def wave(m, dt):
        #         wave.angle += dt / 4
        #         a = OUT + np.array([0, -m.get_height()/2, 0])
        #         print(a)
        #         r = math.sin(math.sin(wave.angle*16) / 4)
        #         m.rotate(r, axis=a)
        #     wave.angle = 0
        #     self.body['hands'][0].add_updater(wave)

    def wave(self, scene: Scene, waves, duration=0.3, angle=0.6):
        hand = self.body['hands'][0]
        pin = hand.get_center()
        pin[1] = hand.get_coord(1, direction=DOWN)
        scene.play(Rotate(hand, angle=angle/2, about_point=pin), run_time=duration/2)
        for i in range(waves):
            scene.play(Rotate(hand, angle=-angle, about_point=pin), run_time=duration)
            scene.play(Rotate(hand, angle=angle, about_point=pin), run_time=duration)
        scene.play(Rotate(hand, angle=-angle/2, about_point=pin), run_time=duration/2)

    def start_blinking(self):
        if self.blinking_functions:
            parts = self.body['eyes'] + self.body['pupils']
            for e in parts:
                f = get_blink_fn(e)
                self.blinking_functions.append(f)
                e.add_updater(f)

    def stop_blinking(self):
        if not self.blinking_functions:
            parts = self.body['eyes'] + self.body['pupils']
            for e, f in zip(parts, self.blinking_functions):
                e.remove_updater(f)
            self.blinking_functions.clear()

    def get_bubble(self, type_='thought', dir_=LEFT):
        filepath = os.path.join(NINJA_DIR, "ninja", f"bubble_{type_}.svg")
        bubble = SVGMobject(filepath)
        bubble.set_width(self.get_width()*8/5)
        bubble.set_height(self.get_height())
        if dir_ is LEFT:
            bubble = bubble.flip()
        center = self.get_corner(UL) + np.array([0, self.get_height(), 0]) / 2
        return bubble.move_to(center)


class EmojiTest(Scene):
    def construct(self):
        emotions = ['happy', 'thinking', 'dunno', 'sad', 'confused', 'cool', 'poker', 'surprised', 'scared', 'stars']

        last = emotions[0]
        last_ninja = Ninja(last).scale(2)
        self.play(DrawBorderThenFill(last_ninja))

        for cur in emotions[1:]:
            cur_ninja = Ninja(cur).scale(2)
            self.play(ReplacementTransform(last_ninja, cur_ninja))
            last_ninja = cur_ninja
            self.wait(duration=2)

        self.play(*[FadeOutAndShiftDown(x) for x in [last_ninja]])
        self.wait()
