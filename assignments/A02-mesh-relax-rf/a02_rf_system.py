# ========================================================================
# CHALLENGE 01: Attractors
# To complete this challenge:
# 1. Implement the methods `eccentrize_centerlines_attractor_point`
#    and `eccentrize_centerlines_attractor_curve` located below.
# 2. Once implemented, apply these methods within the `RF System` section
#    of the Grasshopper canvas.
# ========================================================================
from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Vector


class RFSystem:
    """
    Reciprocal-frame helper built on top of a COMPAS mesh.
    All computed RF data is written back as edge attributes of the mesh.

    The mesh edges become the "members" of the RF system. This class stores extra
    edge attributes needed later for timber fabrication:
    - ``centerline``: geometric line used to create a beam
    - ``normal``: orientation vector for the beam cross-section
    - ``next_edge`` / ``prev_edge``: neighboring RF edges around the local face
    """

    def __init__(self, mesh: Mesh):
        self.mesh = mesh
        self.timber_model = None

    @property
    def centerlines(self) -> list:
        return [self.mesh.edge_attribute(edge, "centerline") for edge in self.mesh.edges()]

    def copy(self) -> "RFSystem":
        return RFSystem(mesh=self.mesh.copy())

    # --------------------------------------------------------------------------
    # RF DATASTRUCTURE SETUP
    # --------------------------------------------------------------------------

    def create_rf_datastructure(self) -> None:
        """
        Compute and store all RF edge attributes.
        """
        # Initialize centerline + normal for every edge.
        for edge in self.mesh.edges():
            self._set_centerline(edge)

            # Boundary edges are valid members, but they have incomplete RF neighborhood data,
            # so we can skip computing those attributes for them.
            if self.mesh.is_edge_on_boundary(edge):
                continue

            self._set_normal(edge)
            self._set_edge_neighborhood(edge)

    def _set_centerline(self, edge) -> None:
        """Store the geometric line representation of a mesh edge."""
        self.mesh.edge_attribute(edge, "centerline", self.mesh.edge_line(edge))

    def _set_normal(self, edge) -> None:
        """Store an orientation normal for an edge (averaged on interior edges, single-face on boundary)."""
        self.mesh.edge_attribute(edge, "normal", self._compute_edge_normal(edge))

    def _set_edge_neighborhood(self, edge) -> None:
        next_edge = self._compute_next_rf_edge(edge)
        prev_edge = self._compute_prev_rf_edge(edge)

        # Store local RF connectivity for interior edges
        self.mesh.edge_attribute(edge, "next_edge", next_edge)
        self.mesh.edge_attribute(edge, "prev_edge", prev_edge)

    def _compute_next_rf_edge(self, edge):
        """Return the next halfedge around the face of the given halfedge."""
        face = self.mesh.halfedge_face(edge)
        halfedges = self.mesh.face_halfedges(face)
        index = halfedges.index(edge)
        return halfedges[(index + 1) % len(halfedges)]

    def _compute_prev_rf_edge(self, edge):
        """Return the previous RF edge by walking the opposite halfedge's face cycle."""
        reversed_edge = (edge[1], edge[0])
        # Reversing first, then taking "next", is a neat way to get the previous RF relation
        return self._compute_next_rf_edge(reversed_edge)

    def _compute_edge_normal(self, edge) -> Vector:
        """
        Compute an edge orientation vector.

        Interior edges use the average of the two neighboring face normals.
        Boundary edges use the single adjacent face normal.
        """
        face_a, face_b = self.mesh.edge_faces(edge)
        normal_a = self.mesh.face_normal(face_a)
        normal_b = self.mesh.face_normal(face_b)

        edge_normal = normal_a + normal_b
        edge_normal.unitize()

        return edge_normal

    # --------------------------------------------------------------------------
    # RF SYSTEM CENTERLINES ROTATION
    # --------------------------------------------------------------------------

    def eccentrize_centerlines(self, eccentricity: float) -> Mesh:
        """
        Shift interior centerlines so beams overlap like a reciprocal frame.

        Positive values push line ends in the local RF directions.
        """
        for edge in self.mesh.edges():
            if self.mesh.is_edge_on_boundary(edge):
                continue

            next_edge = self.mesh.edge_attribute(edge, "next_edge")
            prev_edge = self.mesh.edge_attribute(edge, "prev_edge")
            centerline = self.mesh.edge_attribute(edge, "centerline")

            next_direction = self.mesh.edge_direction(next_edge).unitized()
            prev_direction = self.mesh.edge_direction(prev_edge).unitized()

            start_shift = prev_direction * eccentricity
            end_shift = (-start_shift) + next_direction * eccentricity

            centerline.start += start_shift
            centerline.end += end_shift
            self.mesh.edge_attribute(edge, "centerline", centerline)

        return self.mesh

    def extend_centerlines(self, extension: float) -> None:
        """
        Extend interior centerlines and trim them at adjacent boundary edges when needed.
        """
        for edge in self.mesh.edges():
            if self.mesh.is_edge_on_boundary(edge):
                continue
            extend_start = not self.mesh.is_vertex_on_boundary(edge[0])
            extend_end = not self.mesh.is_vertex_on_boundary(edge[1])

            centerline: Line = self.mesh.edge_attribute(edge, "centerline")
            direction = centerline.direction.unitized()
            if extend_start and extend_end:
                centerline.start += direction * (-extension)
                centerline.end += direction * extension * 2
            elif extend_start and not extend_end:
                centerline.start += direction * (-extension)
                centerline.end += direction * extension
            elif not extend_start and extend_end:
                centerline.end += direction * extension

            self.mesh.edge_attribute(edge, "centerline", centerline)

    # ========================================================================
    # CHALLENGE 01: Attractors
    # ========================================================================

    def eccentrize_centerlines_attractor_point(self, point: Point, factor: float) -> None:
        """
        Moves the centerlines of the RF system edges towards or away from an attractor point.
        The amount of movement is determined by the distance to the point.
        """
        # 1. Iterate over all edges in the mesh
        # 2. Skip boundary edges
        # 3. Get the next_edge, prev_edge, and centerline attributes for the current edge
        # 4. Calculate the unitized direction vectors for next_edge and prev_edge
        # 5. Get the vertex points for the start and end of the current edge
        # 6. Calculate the distance from each vertex to the attractor point
        # 7. Multiply the distances by the factor to get the eccentricity values
        # 8. Calculate the start and end displacements using the direction vectors and eccentricity values
        # 9. Apply the displacements to the start and end of the centerline
        # 10. Update the centerline attribute for the current edge
        pass

    def eccentrize_centerlines_attractor_curve(self, curve, factor: float) -> None:
        """Eccentrize centerlines base on the distance to an attractor curve."""
        # 1. Iterate over all edges in the mesh
        # 2. Skip boundary edges
        # 3. Get the next_edge, prev_edge, and centerline attributes for the current edge
        # 4. Calculate the unitized direction vectors for next_edge and prev_edge
        # 5. Get the vertex points for the start and end of the current edge
        # 6. Find the closest points on the attractor curve from each vertex
        # 7. Calculate the distance between each vertex and its closest point on the curve
        # 8. Multiply the distances by the factor to get the eccentricity values
        # 9. Calculate the start and end displacements using the direction vectors and eccentricity values
        # 10. Apply the displacements to the start and end of the centerline
        # 11. Update the centerline attribute for the current edge
        pass
