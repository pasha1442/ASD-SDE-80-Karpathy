"""Template for video mode. Silent explainer, text on screen tells the story.

Render:
    manim -ql manim_template.py Explainer                              # preview
    manim --resolution 1920,1080 --fps 30 manim_template.py Explainer  # final

Uses Text only, so LaTeX is not necessary. Replace the scenes with your storyboard.
"""
from manim import *

SANS = "Inter"            # falls back to the system sans font if Inter is not installed
MONO = "DejaVu Sans Mono"
INK, DIM = "#ECECEC", "#8A8F98"
BLUE_A, YELLOW_A, RED_A, GREEN_A = "#58C4DD", "#FFD866", "#FC6255", "#83C167"
config.background_color = "#0B0D10"


def T(s, size=36, color=INK, weight=NORMAL, font=SANS, **kw):
    """All words and numbers go through Text, never Tex."""
    return Text(s, font=font, font_size=size, color=color, weight=weight, **kw)


def fit(mob, max_width=12.4):
    """Keep an object inside the 14.2-unit frame."""
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


class Explainer(Scene):
    def heading(self, s):
        return T(s, 30, BLUE_A, weight=BOLD).to_edge(UP, buff=0.55)

    def clear_scene(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def construct(self):
        self.scene_question()
        self.scene_bars()
        self.scene_flow()
        self.scene_answer()

    # 1. The question -------------------------------------------------
    def scene_question(self):
        title = T("REPLACE: the question", 64, weight=BOLD)
        sub = T("REPLACE: why it matters, in one short sentence", 30, DIM).next_to(title, DOWN, buff=0.5)
        fit(title)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.2))
        self.wait(2.5)
        self.clear_scene()

    # 2. Compare two quantities with bars -----------------------------
    def scene_bars(self):
        self.play(FadeIn(self.heading("REPLACE: what the bars compare")))
        x0, unit = -2.0, 0.14          # one unit of data = 0.14 scene units
        rows = [("Option A", 8.5, GREEN_A, 0.8), ("Option B", 46.8, RED_A, -0.4)]
        for name, value, color, y in rows:
            label = T(name, 26).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=value * unit, height=0.6, stroke_width=0, fill_color=color, fill_opacity=1)
            bar.move_to([x0 + value * unit / 2, y, 0])
            number = T(f"{value}%", 30, color, weight=BOLD).next_to(bar, RIGHT, buff=0.25)
            self.play(FadeIn(label), run_time=0.4)
            self.play(GrowFromEdge(bar, LEFT), run_time=1.2)
            self.play(FadeIn(number), run_time=0.3)
        caption = T("REPLACE: what the viewer must conclude.", 26).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(caption, shift=UP * 0.2))
        self.wait(3)
        self.clear_scene()

    # 3. A flow: boxes, labelled arrows, a dot that moves ---------------
    def scene_flow(self):
        self.play(FadeIn(self.heading("REPLACE: what moves through the system")))
        names = ["Browser", "Resolver", "Server"]
        boxes = VGroup(*[
            VGroup(RoundedRectangle(corner_radius=0.12, width=2.8, height=1.1, stroke_color=INK, stroke_width=2),
                   T(n, 26)) for n in names
        ]).arrange(RIGHT, buff=1.8)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.1, color=DIM, stroke_width=3)
                          for i in range(len(names) - 1)])
        labels = VGroup(*[T(s, 20, DIM).next_to(a, UP, buff=0.12) for s, a in zip(["asks", "asks"], arrows)])
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in boxes], lag_ratio=0.25))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), FadeIn(labels))
        dot = Dot(boxes[0].get_right(), radius=0.12, color=YELLOW_A)
        self.play(FadeIn(dot))
        for a in arrows:
            self.play(dot.animate.move_to(a.get_end()), run_time=1.0)
        self.play(Indicate(boxes[-1], color=YELLOW_A))
        self.wait(2)
        self.clear_scene()

    # 4. The answer -----------------------------------------------------
    def scene_answer(self):
        answer = fit(T("REPLACE: the answer in one sentence.", 44, weight=BOLD))
        limit = T("REPLACE: the limit of this explanation.", 30, YELLOW_A).next_to(answer, DOWN, buff=0.6)
        self.play(Write(answer), run_time=1.5)
        self.play(FadeIn(limit, shift=UP * 0.2))
        self.wait(3.5)
        self.play(FadeOut(answer), FadeOut(limit))
