import numpy as np
from scipy.interpolate import interp1d
from manimlib.imports import *


class Simulation(VGroup):
    CONFIG = {
        'number_of_vertices': 10,
        'max_iterations_count': 25,
        'speed_up_at': 3,
        'speed_up_to': .2,
        'zoom_at': 10,
        'zoom_scale': .2,
        'primary_color': WHITE,
        'secondary_color': BLUE,
        'scene_margin': {
            'top': 1,
            'right': 3,
            'bottom': 1,
            'left': 3
        },
        'styles': {
            'edges': {
                'stroke_width': 2
            }
        }
    }

    def __init__(self, scene, **kwargs):
        super().__init__(**kwargs)

        self.scene = scene

        self.default_radius = .15

        self.time = 0
        self.last_update_time = 0

        self.time_scale = 1
        self.iterations = 0

        self.scale = 1

        self.vertices = VGroup()
        self.polygon_edges = VGroup()

        self.mid_vertices = VGroup()
        self.mid_polygon_edges = VGroup()

        self._create_random_vertices()
        self._create_edges_from_vertices()
        self._create_new_polygon_in_mid_points()

        self.add(self.vertices)
        self.add(self.polygon_edges)

    def _create_dot(self, x, y, color):
        dot = Dot()
        dot.set_style(fill_color=color)

        dot.move_to(np.array([x, y, 0]))

        dot.set_height(self.default_radius * self.scale)

        return dot

    def _create_random_vertices(self):
        for i in range(self.number_of_vertices):
            x = np.random.uniform(
                -FRAME_WIDTH / 2 + self.scene_margin['left'],
                FRAME_WIDTH / 2 - self.scene_margin['right']
            )
            y = np.random.uniform(
                -FRAME_HEIGHT / 2 + self.scene_margin['bottom'],
                FRAME_HEIGHT / 2 - self.scene_margin['top']
            )

            self.vertices.add(self._create_dot(
                x, y, self.primary_color
            ))

            self.scene.play(
                FadeIn(self.vertices[-1], run_time=.5)
            )

    def _create_edges_from_vertices(self):
        for i in range(len(self.vertices)):
            start_point = self.vertices[i].get_center()
            end_point = self.vertices[0].get_center()

            if i != len(self.vertices) - 1:
                end_point = self.vertices[i + 1].get_center()

            line = Line(start=start_point, end=end_point)
            line.set_style(**self.styles['edges'])

            self.scene.play(
                ShowCreation(line, run_time=.3)
            )

            self.polygon_edges.add(line)

    def _switch_colors(self):
        animations = []

        for obj in list(self.vertices) + list(self.polygon_edges):
            animations.append(
                UpdateFromAlphaFunc(
                    obj,
                    lambda obj, a: obj.set_style(fill_color=interpolate_color(
                        self.secondary_color, self.primary_color, a), stroke_color=interpolate_color(
                        self.secondary_color, self.primary_color, a)),
                    run_time=.4 * self.time_scale
                )
            )

        self.scene.play(*animations)

    def _switch_all(self):
        self.vertices.remove(*list(self.vertices))
        self.polygon_edges.remove(*list(self.polygon_edges))

        self.vertices.add(*list(self.mid_vertices))
        self.polygon_edges.add(*list(self.mid_polygon_edges))

        self.mid_vertices.remove(*list(self.mid_vertices))
        self.mid_polygon_edges.remove(*list(self.mid_polygon_edges))

    def _zoom(self):
        frame = self.scene.camera.frame
        frame_width, frame_height = frame.get_width(), frame.get_height()
        frame_position = frame.get_center()
        path_func = path_along_arc(45 * DEGREES)

        vertices = list(map(lambda dot: dot.get_center(), self.vertices))
        polygon = Polygon(*vertices)

        poly_size = max(polygon.get_width(), polygon.get_height())

        poly_frame = Square()
        poly_frame.set_width(poly_size + .5)
        poly_frame.move_to(polygon.get_center())

        self.scene.play(
            ShowCreation(poly_frame)
        )

        animations = []

        for dot in self.vertices:
            animations.append(
                UpdateFromAlphaFunc(
                    dot,
                    lambda obj, a: obj.set_height(interpolate(
                        self.default_radius * self.scale,
                        self.default_radius * self.zoom_scale,
                        a
                    ))
                )
            )

        for line in self.polygon_edges:
            animations.append(
                UpdateFromAlphaFunc(
                    line,
                    lambda obj, a: obj.set_style(stroke_width=interpolate(
                        self.scale, self.zoom_scale, a) *
                        self.styles['edges']['stroke_width'])
                )
            )

        animations.append(
            UpdateFromAlphaFunc(
                frame,
                lambda obj, a: frame.set_height(interpolate(
                    frame_height,
                    poly_frame.get_height(),
                    a
                ))
            )
        )
        animations.append(
            UpdateFromAlphaFunc(
                frame,
                lambda obj, a: frame.set_width(interpolate(
                    frame_width,
                    poly_frame.get_width() - .2,
                    a
                ))
            )
        )
        animations.append(
            UpdateFromAlphaFunc(
                frame,
                lambda obj, a: frame.move_to(path_func(
                    frame_position, polygon.get_center(), a
                ))
            )
        )

        self.scene.play(*animations)

        self.scale = self.zoom_scale

    def _create_new_polygon_in_mid_points(self):
        for i, edge in enumerate(self.polygon_edges):
            edge_start_point = edge.get_start()
            edge_end_point = edge.get_end()

            x = interpolate(edge_start_point[0], edge_end_point[0], .5)
            y = interpolate(edge_start_point[1], edge_end_point[1], .5)

            dot = self._create_dot(
                x, y, self.secondary_color
            )

            self.mid_vertices.add(dot)

        for i in range(len(self.mid_vertices)):
            start_point = self.mid_vertices[i].get_center()
            end_point = self.mid_vertices[0].get_center()

            if i != len(self.mid_vertices) - 1:
                end_point = self.mid_vertices[i + 1].get_center()

            line = Line(start=start_point, end=end_point)
            line.set_style(stroke_color=self.secondary_color,
                           stroke_width=self.scale * self.styles['edges']['stroke_width'])

            self.mid_polygon_edges.add(line)

        self.add(self.mid_vertices)

        self.scene.play(
            FadeIn(self.mid_vertices, run_time=self.time_scale),
            FadeIn(self.mid_polygon_edges, run_time=self.time_scale)
        )

        self.scene.play(
            FadeOut(self.vertices, run_time=self.time_scale),
            FadeOut(self.polygon_edges, run_time=self.time_scale)
        )

        self._switch_all()
        self._switch_colors()

        self.iterations += 1

        if self.iterations == self.speed_up_at:
            self.time_scale = self.speed_up_to

        if self.iterations == self.zoom_at:
            self._zoom()

        if self.iterations != self.max_iterations_count:
            self._create_new_polygon_in_mid_points()
