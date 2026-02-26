from a01_rf_system import RFSystem
from compas.datastructures import Mesh
from compas_timber.connections import JointTopology
from compas_timber.connections import LMiterJoint
from compas_timber.connections import TButtJoint
from compas_timber.connections import TStepJoint
from compas_timber.connections import XLapJoint
from compas_timber.design import CategoryRule
from compas_timber.design import DirectRule
from compas_timber.design import JointRuleSolver
from compas_timber.design import TopologyRule
from compas_timber.elements import Beam
from compas_timber.model import TimberModel


class TimberModelCreator:
    """
    A helper class to create a Timber Model from an instance of `RFSystem` class.

    This class demonstrates the three main steps of computational timber design:
    1. INPUT: Converting abstract centerlines (geometric lines extracted from an RFSystem's mesh) into physical objects (Beams).
    2. RULES: Defining how these objects should connect where they intersect (Joints).
    3. SOLVING: Calculating the geometry of those connections (Processing).
    """

    def __init__(self, rf_system: RFSystem, beam_width: float = 0.08, beam_height: float = 0.10, tolerance: float = 0.02):
        self.rf_system = rf_system
        self.timber_model = TimberModel()
        self.beam_width = beam_width
        self.beam_height = beam_height
        self.joining_errors = []

        # Rule solver settings.
        self.tolerance = tolerance  # The maximum distance between lines to consider them as "touching"
        self._rules = []

    def create_timber_model(self, process_joinery: bool = True) -> TimberModel:
        """
        The main recipe for generating the model.
        """
        print(f"--- Starting Timber Model Generation ---")

        # Step 1: Geometry
        # Call the method that creates beams
        # ...
        print(f"Generated {len(list(self.timber_model.beams))} beams.")

        # Step 2: Definitions
        # Reset rules and call the method that adds rules
        # Two options: add general rules based on categories/topology
        # Or, alternatively, define rules based on the RF edge graph
        # ...

        # Step 3: Calculation
        # Call the method that applies rules
        # ...

        print("Model generation complete.")

        return self.timber_model

    # --------------------------------------------------------------------------
    # Beam creation
    # --------------------------------------------------------------------------

    def _create_beams(self) -> None:
        """
        Convert every RF edge into a `Beam` and store the beam back on the edge.
        """
        # Get the mesh from the RF system
        # ...

        # Loop through all edges in the mesh
        # for ..
        #    Read the edge centerline
        #     ..

        #    Read the edge normal
        #    ...

        #    Create a Beam from the centerline using the configured width/height
        #    ...

        #    Store a category attribute on the beam (e.g. "boundary" or "interior")
        #    Use `self._edge_category(edge)` to compute it
        #    ...

        #    Add the beam to `self.timber_model`
        #    ...

        #    Store the created beam back on the mesh edge as an attribute
        #    ...

    def _edge_category(self, edge) -> str:
        if self.rf_system.mesh.is_edge_on_boundary(edge):
            return "boundary"

        return "interior"

    # --------------------------------------------------------------------------
    # Rule definition
    # --------------------------------------------------------------------------

    def _add_rules(self) -> None:
        """
        Defines the 'logic' of connections.
        """
        # Case 1: TWO INTERIOR BEAMS (CATEGORY)
        # When two interior beams meet, assign a lap joint (X-Lap)
        # ...

        # Case 2: AN INTERIOR BEAM MEETS A BOUNDARY BEAM (CATEGORY)
        # When an interior beam meets a boundary beam, assign a butt or step joint
        # ...

        # Case 3: TWO BOUNDARY BEAMS (CATEGORY)
        # When two boundary beams meet (usually at the corners), assign a miter joint
        # ...

        # Case 4: MEETING (T-Shape)
        # The default rule for topological T-joints (one beam ends against the face of another)
        # ...

    def _apply_rules(self, process_joinery: bool) -> None:
        """
        Runs the solver to find intersections and apply the rules we defined above.
        """
        # Reset the list of joining errors before running the solver
        # ...

        # Create a JointRuleSolver instance
        # ...

        # Ask the solver to apply the rules to `self.timber_model`
        # It returns: (joining_errors, unjoined_clusters)

        # If there are joining errors, print a header and then print each error on its own line
        # ...

        # If `process_joinery` is True, process/cut the joint geometry
        # ...

    # --------------------------------------------------------------------------
    # Optional: direct joint strategies (more explicit, less scalable)
    # --------------------------------------------------------------------------

    def _add_rules_direct(self) -> None:
        """
        Alternative workflow: create rules directly from the RF edge graph instead of
        relying on categories/topology inference.
        """
        self._add_direct_joint_rules()
        self._add_direct_boundary_joint_rules()

    def _add_direct_joint_rules(self) -> None:
        mesh: Mesh = self.rf_system.mesh

        for edge in mesh.edges():
            if mesh.is_edge_on_boundary(edge):
                continue

            beam = mesh.edge_attribute(edge, "beam")
            next_edge = mesh.edge_attribute(edge, "next_edge")
            prev_edge = mesh.edge_attribute(edge, "prev_edge")

            next_beam = mesh.edge_attribute(next_edge, "beam") if next_edge else None
            prev_beam = mesh.edge_attribute(prev_edge, "beam") if prev_edge else None

            if beam is None:
                continue

            # Transition from interior to boundary: combine butt + lap logic.
            if next_edge and mesh.is_edge_on_boundary(next_edge):
                if next_beam:
                    self._rules.append(DirectRule(TButtJoint, [beam, next_beam], self.tolerance))
                if prev_beam:
                    self._rules.append(DirectRule(XLapJoint, [prev_beam, beam], self.tolerance))
                continue

            if prev_edge and mesh.is_edge_on_boundary(prev_edge):
                if prev_beam:
                    self._rules.append(DirectRule(TButtJoint, [beam, prev_beam], self.tolerance))
                if next_beam:
                    self._rules.append(DirectRule(XLapJoint, [next_beam, beam], self.tolerance))
                continue

            # Interior-interior transitions: use lap joints on both sides.
            if next_beam:
                self._rules.append(DirectRule(XLapJoint, [next_beam, beam], self.tolerance))
            if prev_beam:
                self._rules.append(DirectRule(XLapJoint, [prev_beam, beam], self.tolerance))

    def _add_direct_boundary_joint_rules(self) -> None:
        mesh: Mesh = self.rf_system.mesh

        for vertex in mesh.vertices_on_boundary():
            # Find boundary edges connected to this vertex
            boundary_edges = []
            for edge in mesh.vertex_edges(vertex):
                if mesh.is_edge_on_boundary(edge):
                    boundary_edges.append(edge)

            if len(boundary_edges) != 2:
                continue

            beam_a = mesh.edge_attribute(boundary_edges[0], "beam")
            beam_b = mesh.edge_attribute(boundary_edges[1], "beam")
            if beam_a and beam_b:
                self._rules.append(DirectRule(LMiterJoint, [beam_a, beam_b], self.tolerance))
