from compas.geometry import Point
from compas.geometry import Vector


class AttractorPointModifier:
    def __init__(self, point: Point, force: float):
        self.point = point
        self.attraction_force = force
        self.type = "force_modifier"

    def apply(self, relaxer, mesh):
        for vertex in mesh.vertices():
            neighbors = mesh.vertex_neighbors(vertex)

            if len(neighbors) <= 2:
                continue

            vertex_point = mesh.vertex_point(vertex)
            direction = Vector.from_start_end(vertex_point, self.point)
            attraction_force = direction * (1 / direction.length) * self.attraction_force
            force = mesh.vertex_attribute(vertex, "force")
            force += attraction_force
            mesh.vertex_attribute(vertex, "force", force)


class DirectionalForceModifier:
    def __init__(self, direction: Vector, force: float):
        self.direction = direction
        self.force = force
        self.type = "force_modifier"

    def apply(self, relaxer, mesh):
        for vertex in mesh.vertices():
            neighbors = mesh.vertex_neighbors(vertex)

            if len(neighbors) <= 2:
                continue

            force = mesh.vertex_attribute(vertex, "force")
            directional_force = self.direction * self.force
            force += directional_force
            mesh.vertex_attribute(vertex, "force", force)
