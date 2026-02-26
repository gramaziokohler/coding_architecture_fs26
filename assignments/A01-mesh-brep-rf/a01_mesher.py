import Rhino.Geometry as rg  # type: ignore
from compas.datastructures import Mesh
from compas.geometry import NurbsSurface
from compas.geometry import Point
from compas.geometry import Polyline
from compas.itertools import linspace
from compas_rhino.conversions import polyline_to_compas


class BaseMesher:
    """Small shared base class for Brep-based meshers."""

    def __init__(self, u_count: int, v_count: int, brep: rg.Brep):
        self.u_count = u_count
        self.v_count = v_count
        self.brep = brep
        self.mesh = Mesh()

    @property
    def face(self) -> rg.BrepFace:
        return self.brep.Faces[0]

    @property
    def surface(self) -> NurbsSurface:
        return NurbsSurface.from_native(self.face.UnderlyingSurface())

    def is_vertex_on_face(self, vertex_key) -> bool:
        # CHALLENGE 01:
        # Get the point of the vertex and check if it's on the face using Rhino's `IsPointOnFace` method.
        # Remember to convert between COMPAS and Rhino geometry when needed.
        # ...

        # Return True if the point is on the face (either interior or boundary), False otherwise.
        return False

    def _vertex_key(self, u_index: int, v_index: int) -> int:
        return next(self.mesh.vertices_where({"u": u_index, "v": v_index}))

    def _filtered_face_vertices(self, vertex_keys: list[int]) -> list[int]:
        # CHALLENGE 02:
        # A useful helper method would be to filter a list of vertex keys, keeping only those that are on the face.
        # ...
        return []


class QuadMesher(BaseMesher):
    """Generate a quad mesh from a single-face Brep.

    Parameters
    ----------
    u_count : int
        Number of cells in the U direction.
    v_count : int
        Number of cells in the V direction.
    brep : rg.Brep
        Input Brep. Only the first face is used.
    full_quads : bool, optional
        If ``True``, keep only complete quads.
        If ``False``, allow clipped boundary polygons.

    Attributes
    ----------
    mesh : compas.datastructures.Mesh
        Output mesh.
    """

    def __init__(self, u_count: int, v_count: int, brep: rg.Brep, full_quads: bool = False):
        super().__init__(u_count=u_count, v_count=v_count, brep=brep)
        self.full_quads = full_quads

    def generate_vertices(self) -> None:
        """Sample the surface on a regular UV grid and store mesh vertices."""
        # Create evenly spaced sample values in the U domain of the surface
        # Use `self.u_count + 1` values so you get the grid vertices (not just cells)
        # ...

        # Create evenly spaced sample values in the V domain of the surface
        # Use `self.v_count + 1` values for the same reason
        # ...

        # Loop over all U samples (keep both the index `ui` and the parameter value `u`)
        # ...
            # Loop over all V samples (keep both `vi` and `v`)
            # ...

                # Evaluate the surface at (u, v) to get a 3D point
                # ...

                # Add a mesh vertex at that point
                # Also store the grid indices as attributes: `u=ui`, `v=vi`
                # ...

        # Explicitly return None (optional, but kept for clarity)
        return None

    def generate_mesh(self) -> Mesh:
        # First, generate the grid vertices on the surface
        # ...

        # Loop over each grid cell in U (there are `self.u_count` cells)
        # ...
            # Loop over each grid cell in V (there are `self.v_count` cells)
            # ...

                # Get the four corner vertex keys of the current cell
                # Follow a consistent order around the face (v1, v2, v3, v4)
                # ...

                # Filter out corners that are not actually on the Brep face
                # (important near trimmed boundaries)
                # ...

                # If fewer than 3 vertices remain, we cannot make a face
                # Skip this cell
                # ...

                # If `self.full_quads` is True, only keep complete 4-sided faces
                # Skip clipped boundary polygons
                # ...

                # Add the face to the mesh
                # ...

        # Clean up any vertices that were generated but never used by a face
        # ...

        # Return the completed mesh
        # ...
