from compas.datastructures import Mesh
from compas.geometry import Line
from compas.geometry import Vector
from compas.geometry import intersection_segment_segment


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

            next_edge = self.mesh.edge_attribute(edge, "next_edge")
            prev_edge = self.mesh.edge_attribute(edge, "prev_edge")

            centerline = self.mesh.edge_attribute(edge, "centerline")
            direction = centerline.direction.unitized()
            centerline.start += direction * (-extension)
            centerline.end += direction * extension * 2

            self._trim_centerline_at_boundary(edge, centerline, next_edge, prev_edge)

    def _trim_centerline_at_boundary(self, edge, centerline, next_edge, prev_edge) -> None:
        # Cap extensions at the boundaries
        boundary_edge = None
        if self.mesh.is_edge_on_boundary(prev_edge):
            boundary_edge = prev_edge
        elif self.mesh.is_edge_on_boundary(next_edge):
            boundary_edge = next_edge

        if boundary_edge is not None:
            intersection = intersection_segment_segment(centerline, self.mesh.edge_line(boundary_edge))[0]

            if centerline.end.distance_to_point(intersection) < centerline.start.distance_to_point(intersection):
                centerline = Line(centerline.start, intersection)
            else:
                centerline = Line(centerline.end, intersection)

        centerline = self.mesh.edge_attribute(edge, "centerline", centerline)
