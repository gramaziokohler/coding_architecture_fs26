from compas.datastructures import Mesh
from compas.geometry import NurbsSurface
from compas.geometry import Point
from compas.geometry import Polyline
from compas.geometry import Vector
from compas.geometry import closest_point_on_polyline
from compas_rhino.conversions import polyline_to_compas


class MeshRelaxerGoals:
    """Collection of goals for the relaxation of the mesh.

    Attributes
    ----------
    target_boundary
        Optional boundary constraint passed to the mesh relaxer.
    target_corners
        Optional corners constraint passed to the mesh relaxer.
    target_surface
        Optional surface object (must provide ``closest_point``) used
        when snapping centerline endpoints to a surface.
    """

    def __init__(self, target_boundary: Polyline = None, target_corners: list[Point] = None, target_surface: NurbsSurface = None):
        self.target_boundary = target_boundary
        self.target_corners = target_corners
        self.target_surface = target_surface

    @classmethod
    def from_brep(cls, brep) -> "MeshRelaxerGoals":
        """Create a `MeshRelaxerGoals` object from a Brep."""
        curve = brep.Faces[0].OuterLoop.To3dCurve().ToPolyline(1, 1, 0, 0)
        curve = curve.TryGetPolyline()[1]

        target_boundary = polyline_to_compas(curve)
        vertices = [v.Location for v in brep.Vertices]
        target_corners = [Point(v.X, v.Y, v.Z) for v in vertices]

        target_surface = NurbsSurface.from_native(brep.Faces[0].UnderlyingSurface())
        return cls(target_boundary=target_boundary, target_corners=target_corners, target_surface=target_surface)


class MeshRelaxer:
    """
    Relax a mesh by moving its vertices to their average position of their neighbors.

    Parameters
    ----------
    mesh : Mesh
        The mesh to relax.
    iterations : int, optional
        The number of iterations to perform.
    damping : float, optional
        The damping factor.
    modifiers : list, optional
        A list of modifiers to apply during the relaxation.
    goals : MeshRelaxerGoals, optional
        The goals for the relaxation.
    snap_to_surface : bool, optional
        Whether to snap to the surface.

    Attributes
    ----------
    mesh : Mesh
        The mesh to relax.
    iterations : int
        The number of iterations to perform.
    damping : float
        The damping factor.
    modifiers : list
        A list of modifiers to apply during the relaxation.
    goals : MeshRelaxerGoals
        The goals for the relaxation.
    snap_to_surface : bool
        Whether to snap to the surface.
    snap_to_surface : bool
        Whether to snap to the surface.
    boundary_vertices : list[int]
        The boundary vertices.
    interior_vertices : list[int]
        The interior vertices.

    """

    def __init__(
        self,
        mesh: Mesh,
        iterations=50,
        damping=0.2,
        modifiers: list = None,
        goals: MeshRelaxerGoals = None,
        snap_to_surface: bool = True,
    ):
        self.mesh = mesh
        self.iterations = iterations
        self.damping = damping
        self.goals = goals
        self.modifiers = modifiers or []
        self.snap_to_surface = snap_to_surface

        self.assigned_vertices = set()
        self.step = 0

        self.set_vertices_default_attributes()

    @property
    def boundary_vertices(self):
        """Return the boundary vertices of the mesh."""
        bvs = [v for v in self.mesh.vertices() if self.mesh.is_vertex_on_boundary(v)]
        return bvs

    @property
    def interior_vertices(self):
        """Return the interior vertices of the mesh."""
        ivs = [v for v in self.mesh.vertices() if not self.mesh.is_vertex_on_boundary(v)]
        return ivs

    def set_vertices_default_attributes(self):
        """Set default attributes for all vertices."""
        for vertex in self.mesh.vertices():
            self.mesh.vertex_attribute(vertex, "fixed", False)

    # ========================================================================
    # MAIN TASK
    # ========================================================================

    def relax(self) -> Mesh:
        # 1. Start a loop that runs for the number of `self.iterations`
        # 2. Inside the loop, compute forces (for example, interior forces, boundary forced, etc)
        #    following the ideas that we explored the the examples of mesh relaxation.
        # 3. If there are any modifiers (`self.modifiers`), call the `apply` of each of them.
        # 4. Apply all accumulated forces to update the mesh vertices.
        # 5. Increment the iteration counter `self.step` by 1.
        # 6. After the loop finishes, return the relaxed `self.mesh`.
        pass
