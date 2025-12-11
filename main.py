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
H = -1.5
K = 0
X_TERMINUS = 17
Y_TERMINUS = 6.88574
PIXELS_PER_METER = 6.4

def parabola(x: float, y: float) -> float:
    # original equation: x^2 = 4(P)y
    # this function will be used like this: parabola(x,y)=0
    return (x-H)**2 - (4*P)*(y-K)

def parabola_x(x: float) -> float:
    # original equation: (x-H)^2 = 4(P)(y-K)
    return ((x-H)**2)/(4*P)+K

class ConicsProject(VoiceoverScene, MovingCameraScene):
    def construct(self):
        self.set_speech_service(RecorderService())
        self.camera.background_color = '#040b1c'
        cover = ImageMobject(IMAGES["dsn_overview"])
        cover.scale(0.5)
        cover_location = Text(f"Found at <span fgcolor={GREEN_B}>681 North First Avenue, Barstow, CA</span>")
        self.play(FadeIn(cover), run_time=1.6)
        with self.voiceover("In Goldstone, California, NASA has set up a very important yet unassuming piece of infrastructure.") as v:
            self.wait(v.duration)
            self.wait(1)
        with self.voiceover("This is a communications station, called the Deep Space Network Communications Complex," \
        " which is sued by space missions to communicate.") as v:
            self.wait(v.duration)
        self.play(self.camera.frame.animate.shift(UP*5))
        self.play(FadeOut(cover), run_time=1.6)
        self.wait(1.5)
        dsn_sideview = ImageMobject(IMAGES["dsn_sideview"])
        dsn_sideview.scale(0.5)
        dsn_sideview.move_to(self.camera.frame)
        coordinate_plane = Axes(
            x_range=[-X_TERMINUS+H,X_TERMINUS+H,3],
            y_range=[-Y_TERMINUS+K,Y_TERMINUS+K,3],
            x_length=X_TERMINUS*2,
            y_length=Y_TERMINUS*2,
            color=BLUE_B,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 17*10},
        )
        coordinate_plane.scale(0.1)
        print(coordinate_plane.get_x_unit_size())
        print(coordinate_plane.get_y_unit_size())
        # length_brace = Brace(coordinate_plane, DOWN)
        # length_label = length_brace.put_at_tip(Tex(f"${X_TERMINUS*2}$ m"))
        line = coordinate_plane.plot_implicit_curve(parabola)
        graph = VGroup(coordinate_plane, line)
        graph_detail = graph.copy()
        # graph += length_brace
        # graph += length_label
        x_label = coordinate_plane.get_x_axis_label(Text("width (meters)", font_size=17))
        y_label = coordinate_plane.get_y_axis_label(Text("height (meters)", font_size=17))
        graph += x_label
        graph += y_label
        graph_detail.save_state()
        graph.move_to(dsn_sideview)
        graph.shift(RIGHT*0.75)
        graph.shift(UP*0.5)
        graph.rotate(1/8*PI)
        with self.voiceover("How is this connected to conics?") as v:
            self.play(FadeIn(dsn_sideview), run_time=v.duration)
        with self.voiceover("It turns out that the best cross-section for a radio transmitter dish, at least for long distances, is " \
        "a parabola.") as v:
            self.play(Write(coordinate_plane), Write(line), Write(x_label), Write(y_label), run_time=v.duration)
        self.wait(1.2)
        self.play(self.camera.frame.animate.shift(RIGHT*5), run_time=1.4)
        self.play(Unwrite(x_label), Unwrite(y_label), run_time=0.9)
        graph -= x_label
        graph -= y_label
        graph_detail.restore().move_to(self.camera.frame_center)
        self.play(graph.animate.become(graph_detail), FadeOut(dsn_sideview), run_time=1.5)
        self.remove(graph_detail)
        self.play(graph.animate.scale(2), run_time=1.3)
        focus = Dot(point=coordinate_plane@(H,P,0), color=BLUE_B, radius=0.1)
        directrix = coordinate_plane.plot(lambda x: -P+K, color=BLUE_B)
        vertex = Dot(point=coordinate_plane@(H,K,0), color=BLUE_B, radius=0.1)
        animated_point = Dot(point=coordinate_plane@(H,K,0), color=BLUE_B)
        graph += focus
        graph += directrix
        graph += vertex
        graph += animated_point
        with self.voiceover("Let's examine what a parabola is in detail.") as v:
            self.play(Write(focus), Write(directrix), run_time=v.duration+0.3)
        focus_label = Tex("Focus: ", f"$(0, {P})$").scale(0.5)
        focus_label.next_to(focus, RIGHT, buff=0.1)
        directrix_label = Tex("Directrix: ", f"$y={P}$").scale(0.5)
        directrix_label.next_to(directrix, DOWN, buff=0.1)
        vertex_label = Tex("Vertex: ", f"$({H},{K})$").scale(0.5)
        vertex_label.move_to(vertex)
        vertex_label.shift(3*LEFT+2*DOWN)
        for label in [focus_label, directrix_label]:
            self.play(Write(label), run_time=1.2)
        self.play(Create(vertex), Write(vertex_label), run_time=1.2)
        with self.voiceover("Here we have the focus and the directrix, on opposite sides of the vertex.") as v:
            self.wait(v.duration)
        animated_point_tracker_x = ValueTracker(H)
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
                Line(animated_point.get_center(), coordinate_plane@[animated_point_tracker_x.get_value(), -P+K, 0],
                color=YELLOW_A)
            )
        )
        line_to_focus = Line(color=YELLOW_A)
        line_to_focus.add_updater(lambda lf: lf.become(Line(animated_point, focus, color=YELLOW_A)))
        # directrix_dist = MathTex(animated_point.get_center())
        self.play(Create(animated_point), Write(line_to_directrix), Write(line_to_focus), run_time=1.2)
        with self.voiceover("In essence, we can define this shape as all of the points where it doesn't matter whether you" \
        " measure the distance to the focus or the nearest point on the directrix; the distances are the same.") as v:
            self.play(animated_point_tracker_x.animate.set_value(X_TERMINUS+H), run_time=v.duration)
        standard_form = MathTex(f"(x-h)^2", "=", f"4(p)(y-k)")
        standard_form.move_to(self.camera.frame)
        p_value_eqn = MathTex(f"p={P}")
        p_value_eqn.next_to(standard_form, UP)
        eqn = MathTex(f"(x+{-H})^2", "=", f"4({P})(y-{K})")
        eqn.next_to(standard_form, DOWN)
        self.camera.frame.animate.shift(DOWN*5)
        line_to_focus.clear_updaters()
        line_to_directrix.clear_updaters()
        animated_point.clear_updaters()
        fadeouts2 = []
        for mob in self.mobjects:
            fadeouts2.append(FadeOut(mob))
        self.play(fadeouts2, run_time=1.2)
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
        general_eqn_step1 = MathTex(f"(x+{-H})(x+{-H})-{4*P}(y-{K})=0")
        generalization_steps += general_eqn_step1
        general_eqn_step2 = MathTex(f"x^2+{-H}x+{-H}x+{H*H}-{4*P}y+{4*P}{f'({K})' if K > 0 else ''}=0")
        generalization_steps += general_eqn_step2
        general_eqn_step3 = MathTex(f"x^2-{2*H}x-{4*P}y+{4*P*(K if K != 0 else 1)+H*H}=0")
        generalization_steps += general_eqn_step3
        generalization_steps.arrange(DOWN)
        generalization_steps.move_to(self.camera.frame)
        with self.voiceover("Now to convert to general form, we simply expand, moving over the right side to the left.") as v:
            self.wait(v.duration)
        with self.voiceover("First, we expand the squared expression and take the right side to the left." \
        "We also evaluate four times P.") as v:
            self.play(Write(general_eqn_step1), run_time=v.duration)
        with self.voiceover("We now multiply out the binomials, giving us a 4-term polynomial. Added on to this" \
        " is the y-term which we distributed the 4 times P on to.") as v:
            self.play(Write(general_eqn_step2), run_time=v.duration)
        with self.voiceover("Lastly, we can combine the two identical terms from the perfect square, leaving" \
        " a perfect square trinomial. We also multiply K by 4 times P.") as v:
            self.play(Write(general_eqn_step3), run_time=v.duration)
        self.wait(1.2)
        steps_reversed = generalization_steps.submobjects
        steps_reversed.reverse()
        for mob in steps_reversed:
            self.play(FadeOut(mob), run_time=0.6)
        eqns = VGroup()
        eqn2 = eqn.copy().scale(0.75)
        eqns += eqn2
        general2 = general_eqn_step3.copy().scale(0.75)
        eqns += general2
        eqns.arrange(RIGHT, buff=1)
        eqns.move_to(self.camera.frame)

        self.play(Write(Text("STANDARD FORM").next_to(eqn2, UP)), Write(Text("GENERAL FORM").next_to(general2, UP)),
                  eqn.animate.become(eqn2), general_eqn_step3.animate.become(general2), run_time=1.2)
        with self.voiceover("Well those are the equations.") as v:
            self.wait(v.duration)
        self.wait(2)
        for mob in self.mobjects:
            self.play(FadeOut(mob), run_time=0.6)
        cone1 = Triangle(color=BLUE_B)
        cone1.set_fill(BLUE_B, 1)
        cone1.rotate(PI)
        cone2 = Triangle(color=BLUE_B)
        cone2.set_fill(BLUE_B, 1)
        cones = VGroup(cone1, cone2)
        cones.arrange(DOWN, buff=0)
        cones.scale(2)
        self.play(self.camera.frame.animate.shift(RIGHT*5))
        cones.move_to(self.camera.frame)
        self.play(Write(cones), run_time=1.3)
        with self.voiceover("We can see here the double cone. It can be used to make many conic sections.") as v:
            self.wait(v.duration)
        point1 = Point().move_to(cone2)
        point2 = point1.copy()
        point1.next_to(cone2, DOWN, buff=2)
        point2.shift(2*RIGHT+2*UP)
        plane = Line(point1, point2, color=YELLOW_B)
        disclaimer = Text("Note: the parabola created here isn't the parabola I showed earlier.", font_size=20)
        disclaimer.next_to(cones,UP, buff=0.25)
        self.play(GrowFromCenter(plane), FadeIn(disclaimer), run_time=1.4)
        with self.voiceover("We can see that this plane (viewed from the side) goes through the bottom cone and passes " \
        "through its base. This forms a parabolic cross section.") as v:
            self.wait(v.duration)
        fadeouts1 = []
        for mob in self.mobjects:
            fadeouts1.append(FadeOut(mob))
        self.play(fadeouts1, run_time=1)
        with self.voiceover("That's all for parabolas. I learned a lot during this project.") as v:
            self.wait(v.duration)
        logo = ManimBanner()

        with self.voiceover("For instance, I familiarized myself with a new piece of animation software: Manim. " \
        "I also really have never created animated videos, so I learned a lot there too!") as v:
            time = v.duration/3
            self.play(logo.create(), run_time=time)
            self.play(logo.expand(), run_time=time)
            self.wait(time)
        
        citations = VGroup()
        citations += Text("\"Goldstone Deep Space Communication Complex.\". NASA, 1990.")
        citations += Text("\"Tracks of a Giant\". NASA, 2024.")
        citations.arrange(DOWN, buff=0.25)
        citations.move_to(self.camera.frame)
        with self.voiceover("The images I used of the DSN station come from NASA.") as v:
            time = v.duration/2
            self.play(Write(citations))
            self.wait(time)