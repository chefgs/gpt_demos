import os
from manim import *

class BookstoreArchitecture(Scene):
    def construct(self):
        # Create nodes
        user = Text("User").shift(UP * 3)
        dns = Text("DNS (Route 53)").shift(UP * 1.5)
        lb = Text("Load Balancer").shift(UP * 0)
        frontend = Text("Frontend (React)").shift(DOWN * 1.5 + LEFT * 2)
        backend = Text("Backend (Node.js)").shift(DOWN * 1.5 + RIGHT * 2)
        db = Text("MongoDB Database").shift(DOWN * 3 + RIGHT * 2)
        prometheus = Text("Prometheus").shift(DOWN * 3 + LEFT * 2)
        grafana = Text("Grafana").shift(DOWN * 4.5 + LEFT * 2)

        # Create edges
        edge1 = Arrow(user, dns, buff=0.1)
        edge2 = Arrow(dns, lb, buff=0.1)
        edge3 = Arrow(lb, frontend, buff=0.1)
        edge4 = Arrow(lb, backend, buff=0.1)
        edge5 = Arrow(backend, db, buff=0.1)
        edge6 = Arrow(backend, prometheus, buff=0.1)
        edge7 = Arrow(frontend, prometheus, buff=0.1)
        edge8 = Arrow(prometheus, grafana, buff=0.1)

        # Add nodes and edges to the scene
        self.play(FadeIn(user), FadeIn(dns), FadeIn(lb))
        self.play(FadeIn(frontend), FadeIn(backend))
        self.play(FadeIn(db), FadeIn(prometheus), FadeIn(grafana))
        self.play(GrowArrow(edge1), GrowArrow(edge2))
        self.play(GrowArrow(edge3), GrowArrow(edge4))
        self.play(GrowArrow(edge5), GrowArrow(edge6))
        self.play(GrowArrow(edge7), GrowArrow(edge8))

        # Hold the final frame
        self.wait(2)

if __name__ == "__main__":
    from manim import *
    config.media_width = "75%"
    config.verbosity = "WARNING"
    script_name = f"{__file__}"
    os.system(f"manim {script_name} BookstoreArchitecture")
