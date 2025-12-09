from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
from manim_voiceover.services.gtts import GTTSService
from numpy import *

IMAGES = {
    "rocket1": "assets/rocket1.jpg",
    "dsn_overview": "assets/goldstone_dsn_overview.jpg",
    "submarine_cables": "assets/submarine_cable.jpg",
    "dsn_sideview": "assets/goldstone_dsn_sideview.jpg"
}

P = 10.4927

def parabola(x: float, y: float) -> float:
    # original equation: x^2 = 4(P)y
    # this function will be used like this: parabola(x,y)=0
    return x*x - (4*P)*y

def parabola_x(x: float) -> float:
    # original equation: x^2 = 4(P)y
    return (x*x)/(4*P)

class ConicsProject(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        self.camera_class = MovingCamera
        self.camera.background_color = '#040b1c'
        rocket = ImageMobject(IMAGES["rocket1"])
        rocket.scale(0.5)
        with self.voiceover("NASA's space missions are different from most things that need to communicate...") as v:
            self.play(FadeIn(rocket), run_time=v.duration)
        text_space = Text("SPACE")
        submarine_cables = VGroup()
        cable1 = Rectangle(ORANGE, 0.75, 7)
        cable1.set_fill(ORANGE, 1)
        submarine_cables += cable1
        cable2 = Rectangle(ORANGE, 0.75, 7).next_to(cable1, direction=DOWN, buff=1.5)
        cable2.set_fill(ORANGE, 1)
        submarine_cables += cable2
        signal1 = Arc(start_angle=75*DEGREES, angle=125*DEGREES, color=YELLOW, stroke_width=4).next_to(cable1, direction=LEFT, buff=0.05)
        with self.voiceover("...because they are IN space.") as v:
            time = v.duration/2
            self.play(rocket.animate.next_to(text_space, DOWN, buff=0.1), run_time=time)
            self.play(Write(text_space), run_time=time)
        cover = ImageMobject(IMAGES["dsn_overview"])
        cover.scale(0.3)
        cover.move_to(rocket)
        self.play(Unwrite(text_space), FadeOut(rocket), run_time=0.3)
        self.play(Create(submarine_cables), run_time=0.3)
        with self.voiceover("These cables—how the internet connects—don't run in space." \
        " This means that these space missions need something else to help them connect.") as v:
            first = v.duration*(3/4)
            last = v.duration-first
            self.play(signal1.animate.next_to(cable1, direction=RIGHT, buff=0.05), run_time=first)
            self.play(Uncreate(signal1), run_time=last)
        with self.voiceover("This is where the Deep Space Network comes in.") as v:
            self.play(FadeIn(cover), run_time=v.duration)
        with self.voiceover("It allows space missions, probes, and other devices to communicate back with Earth.") as v:
            self.wait(v.duration)
        self.play([FadeOut(mob) for mob in self.mobjects], run_time=0.75)
        dsn_sideview = ImageMobject(IMAGES["dsn_sideview"])
        dsn_sideview.scale(0.5)
        coordinate_plane = Axes(
            x_range=[-6,6,3],
            y_range=[-17,17,1],
            x_length=3.5,
            y_length=2,
            color=BLUE_B,
            tips=False
        )
        line = coordinate_plane.plot_implicit_curve(parabola)
        graph = VGroup(coordinate_plane, line)
        focus = Dot(point=coordinate_plane@(0,P,0), color=BLUE_B)
        directrix = coordinate_plane.plot(lambda x: -P, color=BLUE_B)
        vertex = Dot(point=coordinate_plane@(0,0,0), color=BLUE_B)
        animated_point = Dot(point=coordinate_plane@(0,0,0), color=BLUE_B)
        graph += focus
        graph += directrix
        graph += vertex
        graph += animated_point
        graph.save_state()
        graph.move_to(dsn_sideview)
        graph.shift(RIGHT*0.2)
        graph.shift(DOWN*0.1)
        graph.rotate(20*DEGREES)
        with self.voiceover("How is this connected to conics?") as v:
            self.play(FadeIn(dsn_sideview), run_time=v.duration)
        with self.voiceover("It turns out that the best cross-section for a radio transmitter dish—at least for long distances—is" \
        "a parabola."):
            self.play(Create(coordinate_plane), Create(line), run_time=0.4)
        self.play(graph.animate.restore(), FadeOut(dsn_sideview), run_time=3/8)
        self.play(graph.animate.scale(2), run_time=3/8)
        with self.voiceover("Let's examine what a parabola is in detail.") as v:
            self.play(Create(focus), Create(directrix), run_time=v.duration+0.3)
        focus_label = Tex("Focus: ", f"$(0, {P})$")
        focus_label.next_to(focus, RIGHT, buff=0.1)
        directrix_label = Tex("Directrix: ", f"$y={P}$")
        directrix_label.next_to(directrix, DOWN, buff=0.1)
        vertex_label = Tex("Vertex: ", "$(0,0)$")
        for label in [focus_label, directrix_label]:
            self.play(Write(label), run_time=0.3)
        with self.voiceover("Here we have the focus and the directrix, on opposite sides of the vertex.") as v:
            self.play(Create(vertex), Write(vertex_label), run_time=v.duration)
        animated_point_tracker_x = ValueTracker(0)
        line_to_directrix = Line(color=YELLOW_A)
        animated_point.add_updater(lambda p: p.become(
            Dot(point=coordinate_plane@[
                        animated_point_tracker_x.get_value(),
                        parabola_x(animated_point_tracker_x.get_value()),
                        0
                    ]
                )
            )
        )
        line_to_directrix.add_updater(lambda ld: 
            ld.become(
                Line(animated_point.get_center(), coordinate_plane@[animated_point.get_x(), -P, 0])
            )
        )
        line_to_focus = Line(color=YELLOW_A)
        line_to_focus.add_updater(lambda lf: lf.become(Line(animated_point, focus)))
        self.play(Create(animated_point), Write(line_to_directrix), Write(line_to_focus), run_time=0.3)
        with self.voiceover("In essence, we can define this shape as all of the points where it doesn't matter whether you" \
        "you measure the distance between the focus or the nearest point on the directrix; they are the same.") as v:
            self.play(animated_point_tracker_x.animate.set_value(17), run_time=v)