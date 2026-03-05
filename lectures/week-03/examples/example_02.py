from compas.geometry import Vector


def compute_forces(mesh_out, damping=0.2):
    for vertex in mesh_out.vertices():
        nbrs = mesh_out.vertex_neighbors(vertex)

        if not nbrs:
            continue

        if len(nbrs) == 2:
            mesh_out.vertex_attribute(vertex, "force", Vector(0, 0, 0))
            continue

        force = Vector(0, 0, 0)
        neighbors = mesh_out.vertex_neighbors(vertex)
        for neighbor in neighbors:
            neighbor_force = mesh_out.edge_vector((vertex, neighbor))
            neighbor_force *= mesh_out.edge_length((vertex, neighbor))
            force += neighbor_force * damping / len(neighbors)

        mesh_out.vertex_attribute(vertex, "force", force)


def compute_gravity(mesh_out, gravity_vector=Vector(0, 0, 0.0068)):
    for vertex in mesh_out.vertices():
        nbrs = mesh_out.vertex_neighbors(vertex)

        if len(nbrs) < 3:
            continue

        force = mesh_out.vertex_attribute(vertex, "force")
        force += gravity_vector
        mesh_out.vertex_attribute(vertex, "force", force)


def apply_forces(mesh_out):
    for vertex in mesh_out.vertices():
        force = mesh_out.vertex_attribute(vertex, "force")
        vertex_point = mesh_out.vertex_point(vertex)
        new_point = vertex_point + force

        mesh_out.vertex_attributes(vertex, "xyz", list(new_point))
