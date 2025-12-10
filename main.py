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
H = -2
K = 0
X_TERMINUS = 17
Y_TERMINUS = 6.88574
PIXELS_PER_METER = 6.4

def parabola(x: float, y: float) -> float:
    # original equation: x^2 = 4(P)y
    # this function will be used like this: parabola(x,y)=0
    return (x-H)**2 - (4*P)*(y-K)

def parabola_x(x: float) -> float:
    # original equation: x^2 = 4(P)y
    return (x-H)**2/(4*P)

class ConicsProject(VoiceoverScene):
    def __init__(self, **kwargs):
        super().__init__(camera_class=MovingCamera, **kwargs)
    def construct(self):
        self.set_speech_service(GTTSService())
        self.camera.background_color = '#040b1c'
        dsn_sideview = ImageMobject(IMAGES["dsn_sideview"])
        dsn_sideview.scale(0.5)
        coordinate_plane = Axes(
            x_range=[-X_TERMINUS,X_TERMINUS,3],
            y_range=[-Y_TERMINUS,Y_TERMINUS,3],
            x_length=3.5,
            y_length=2,
            color=BLUE_B,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 17},
            
        )
        length_brace = Brace(coordinate_plane, DOWN)
        length_label = length_brace.put_at_tip(Tex(f"${X_TERMINUS*2}$ m"))
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
        graph += length_brace
        graph += length_label
        graph.save_state()
        graph.move_to(dsn_sideview)
        graph.shift(RIGHT*0.2)
        graph.shift(DOWN*0.1)
        graph.rotate(1/8*PI)
        with self.voiceover("How is this connected to conics?") as v:
            self.play(FadeIn(dsn_sideview), run_time=v.duration)
        with self.voiceover("It turns out that the best cross-section for a radio transmitter dish—at least for long distances—is" \
        "a parabola.") as v:
            self.play(Write(coordinate_plane), Write(line), run_time=v.duration)
        with self.voiceover("Note that the actual dish is 34 meters in diameter.") as v:
            self.play(Write(length_brace), FadeIn(length_label), run_time=v.duration)
        self.wait(1.2)
        self.play(self.camera.frame.animate.shift(RIGHT*5), run_time=1.4)
        self.play(graph.animate.move_to(self.camera.frame_center), FadeOut(dsn_sideview), run_time=1.5)
        self.play(graph.animate.restore(), run_time=0.5)
        self.play(graph.animate.scale(2), run_time=3/8)
        with self.voiceover("Let's examine what a parabola is in detail.") as v:
            self.play(Write(focus), Write(directrix), run_time=v.duration+0.3)
        focus_label = Tex("Focus: ", f"$(0, {P})$")
        focus_label.next_to(focus, RIGHT, buff=0.1)
        directrix_label = Tex("Directrix: ", f"$y={P}$")
        directrix_label.next_to(directrix, DOWN, buff=0.1)
        vertex_label = Tex("Vertex: ", "$(0,0)$")
        vertex_label.next_to(vertex, DOWN)
        for label in [focus_label, directrix_label]:
            self.play(Write(label), run_time=0.3)
        self.play(Create(vertex), Write(vertex_label), run_time=0.5)
        with self.voiceover("Here we have the focus and the directrix, on opposite sides of the vertex.") as v:
            self.wait(v.duration)
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
                Line(animated_point.get_center(), coordinate_plane@[animated_point.get_center()[0], -P, 0])
            )
        )
        line_to_focus = Line(color=YELLOW_A)
        line_to_focus.add_updater(lambda lf: lf.become(Line(animated_point, focus)))
        self.play(Create(animated_point), Write(line_to_directrix), Write(line_to_focus), run_time=0.3)
        with self.voiceover("In essence, we can define this shape as all of the points where it doesn't matter whether you" \
        "you measure the distance between the focus or the nearest point on the directrix; they are the same.") as v:
            self.play(animated_point_tracker_x.animate.set_value(17), run_time=v.duration)
        standard_form = MathTex(f"(x-h)^2", "=", f"4(p)(y-k)")
        standard_form.move_to(self.camera.frame)
        p_value_eqn = MathTex(f"p={P}")
        p_value_eqn.next_to(standard_form, UP)
        eqn = MathTex(f"(x-{H})^2", "=", f"4({P})(y-{K})")
        eqn.next_to(standard_form, DOWN)
        self.camera.frame.animate.shift(DOWN*5)
        for mob in self.mobjects:
            self.play(FadeOut(mob), run_time=0.3)
        self.wait(1.2)
        self.play(Write(standard_form), run_time=1)
        with self.voiceover("This is the standard form for a parabola.") as v:
            self.wait(v.duration)
        with self.voiceover("Here I am just substituting the key value (called the focal length), p, into the equation.") as v:
            time = v.duration/2
            self.play(Write(p_value_eqn), run_time=time)
            self.play(Write(eqn), run_time=time)
        self.wait(1.2)
        self.play(FadeOut(standard_form), FadeOut(p_value_eqn), run_time=0.6)
        generalization_steps = VGroup(eqn)
        general_eqn_step1 = MathTex(f"(x-{H})(x-{H})-{4*P}(y-{K})=0")
        generalization_steps += general_eqn_step1
        general_eqn_step2 = MathTex(f"x^2-{H}x-{H}x-{4*P}y+{4*P}{f'({K})' if K > 0 else ''}=0")
        generalization_steps += general_eqn_step2
        general_eqn_step3 = MathTex(f"x^2-2({H})x-{4*P}y+{4*P*(K if K != 0 else 1)}=0")
        generalization_steps += general_eqn_step3
        generalization_steps.arrange(DOWN)
        generalization_steps.move_to(self.camera.frame)
        with self.voiceover("Now to convert to general form, we simply expand, moving over the right side to the left.") as v:
            self.wait(v.duration)
        with self.voiceover("First, we expand the squared expression and take the right side to the left." \
        "We also evaluate four times P.") as v:
            self.play(Write(general_eqn_step1), run_time=v.duration)
        with self.voiceover("We now multiply out the binomials, giving us a 4-term polynomial. Added on to this" \
        "is the y-term which we distributed the 4 times P on to.") as v:
            self.play(Write(general_eqn_step2), run_time=v.duration)
        with self.voiceover("Lastly, we can combine the two identical terms from the perfect square, leaving" \
        "a perfect square trinomial. We also multiply K by 4 times P.") as v:
            self.play(Write(general_eqn_step3), run_time=v.duration)
        self.wait(1.2)
        steps_reversed = generalization_steps.submobjects
        steps_reversed.reverse()
        for mob in steps_reversed:
            self.play(FadeOut(mob), run_time=0.3)
        titles = VGroup()
        eqn_with_title = VGroup()
        eqn_title = Text("STANDARD FORM of a PARABOLA")
        eqn_with_title += eqn_title
        titles += eqn_title
        eqn_with_title += eqn
        general_with_title = VGroup()
        general_title = Text("GENERAL FORM")
        titles += general_title
        general_with_title += general_title
        general_with_title += general_eqn_step3
        
        self.play(eqn_with_title.animate.arrange(DOWN), general_with_title.animate.arrange(DOWN), run_time=0.8)
        self.play(graph.animate.next_to(eqn, DOWN), FadeIn(graph), run_time=0.6)
        with self.voiceover("Well that's the equations.") as v:
            self.wait(v.duration)
        cone1 = Triangle(color=BLUE_B)
        cone1.set_fill(BLUE_B)
        cone1.rotate(PI)
        cone2 = Triangle(color=BLUE_B)
        cone2.set_fill(BLUE_B)
        cones = VGroup(cone1, cone2)
        cones.arrange(DOWN, buff=0)
        cones.scale(3)
        self.play(self.camera.frame.animate.shift(RIGHT*5))
        cones.move_to(self.camera.frame)
        self.play(Write(cones), run_time=1.3)
        with self.voiceover("We can see here the double cone. It can be used to make many conic sections.") as v:
            self.wait(v.duration)
        point1 = Point().move_to(cone1)
        point2 = point1.copy()
        point1.shift(2*DOWN)
        point2.shift(2*RIGHT+2*UP)
        plane = Line(point1, point2, color=YELLOW_B)
        disclaimer = Text("Note: the parabola created here isn't the parabola I showed earlier.")
        disclaimer.next_to(cones,DOWN, buff=0.25)
        self.play(GrowFromCenter(plane), run_time=1.4)
        with self.voiceover("We can see that this plane (viewed from the side) goes through the bottom cone and passes " \
        "through its base. This forms a parabola.") as v:
            self.wait(v.duration)
        fadeouts1 = []
        for mob in self.mobjects:
            fadeouts1.append(FadeOut(mob))
        self.play(fadeouts1, run_time=1)
        # with self.voiceover("That's all for parabolas. Now ")