from compas.geometry import Vector


def compute_attractors(mesh, points, attraction_force):
    for attractor_point in points:
        for vertex in mesh.vertices():
            neighbors = mesh.vertex_neighbors(vertex)

            if len(neighbors) <= 2:
                continue

            vertex_point = mesh.vertex_point(vertex)
            direction = Vector.from_start_end(vertex_point, attractor_point)
            attraction_force_vector = direction * (1 / direction.length) * attraction_force
            force = mesh.vertex_attribute(vertex, "force")
            force += attraction_force_vector
            mesh.vertex_attribute(vertex, "force", force)


def compute_forces(mesh, damping=0.2):
    for vertex in mesh.vertices():
        neighbors = mesh.vertex_neighbors(vertex)

        if not neighbors:
            continue

        if len(neighbors) == 2:
            mesh.vertex_attribute(vertex, "force", Vector(0, 0, 0))
            continue

        force = Vector(0, 0, 0)
        for neighbor in neighbors:
            neighbor_force = mesh.edge_vector((vertex, neighbor))
            neighbor_force *= mesh.edge_length((vertex, neighbor))
            force += neighbor_force * damping / len(neighbors)

        mesh.vertex_attribute(vertex, "force", force)


def compute_gravity(mesh, gravity_vector=Vector(0, 0, 0.0068)):
    for vertex in mesh.vertices():
        neighbors = mesh.vertex_neighbors(vertex)

        if len(neighbors) < 3:
            continue

        force = mesh.vertex_attribute(vertex, "force")
        force += gravity_vector
        mesh.vertex_attribute(vertex, "force", force)


def apply_forces(mesh):
    for vertex in mesh.vertices():
        force = mesh.vertex_attribute(vertex, "force")
        vertex_point = mesh.vertex_point(vertex)
        new_point = vertex_point + force

        mesh.vertex_attributes(vertex, "xyz", list(new_point))
