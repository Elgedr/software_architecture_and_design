from collections.abc import Iterator
from math import sqrt

from geom import Point


class SierpinskiTriangle:
    def __init__(self, centre: Point, side_length: float):
        self.centre = centre
        self.side_length = side_length

    def __iter__(self):
        return self.generate_points(self.centre, self.side_length)

    def generate_points(self, centre: Point, side_length: float) -> Iterator[Point]:
        if side_length <= 1:
            # Base case: if side length is very small, yield only the center point
            yield centre
        else:
            # Calculate the height of the triangle
            height = side_length * sqrt(3) / 2

            # Calculate the centers of the three sub-triangles
            top_centre = Point(centre.x(), centre.y() + height / 2)
            left_centre = Point(centre.x() - side_length / 2, centre.y() - height / 2)
            right_centre = Point(centre.x() + side_length / 2, centre.y() - height / 2)

            # Create three smaller SierpinskiTriangles
            sub_triangles = [
                SierpinskiTriangle(top_centre, side_length / 2),
                SierpinskiTriangle(left_centre, side_length / 2),
                SierpinskiTriangle(right_centre, side_length / 2)
            ]

            # Recursively yield points from each sub-triangle
            for triangle in sub_triangles:
                yield from triangle
