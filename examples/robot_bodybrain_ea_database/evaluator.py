"""Evaluator class."""

from revolve2.ci_group import fitness_functions, terrains
from revolve2.ci_group.simulation_parameters import make_standard_batch_parameters
from revolve2.modular_robot import ModularRobot
from revolve2.modular_robot_simulation import (
    ModularRobotScene,
    Terrain,
    simulate_scenes,
)
from revolve2.simulators.mujoco_simulator import LocalSimulator
from revolve2.simulation.scene.geometry import GeometryBox, GeometryPlane
from pyrr import Quaternion, Vector3
from revolve2.simulation.scene import AABB, Color, Pose
from revolve2.simulators.mujoco_simulator.textures import Checker, Flat, Gradient
from revolve2.simulation.scene.geometry.textures import MapType
import math

# def make_custom_terrain() -> Terrain:
#     """
#     Create a custom terrain.

#     :returns: The created terrain.
#     """
#     # A terrain is a collection of static geometries.
#     # Here we create a simple terrain uses some boxes.
#     return Terrain(
#         static_geometry=[
#             GeometryPlane(
#                 pose=Pose(position=Vector3(), orientation=Quaternion()),
#                 mass=0.0,
#                 size=Vector3([20.0, 20.0, 0.0]),
#                 texture=Checker(
#                     primary_color=Color(170, 170, 180, 255),
#                     secondary_color=Color(150, 150, 150, 255),
#                     map_type=MapType.MAP2D,
#                 ),
#             ),
#             GeometryBox(
#                 pose=Pose(position=Vector3([1.0, 0.0, 0.1]), orientation=Quaternion()),
#                 mass=0.0,
#                 texture=Flat(primary_color=Color(0, 255, 0, 255)),
#                 aabb=AABB(size=Vector3([0.5, 0.5, 0.2])),
#             ),
#             GeometryBox(
#                 pose=Pose(
#                     position=Vector3([-0.8, 0.4, 0.125]), orientation=Quaternion()
#                 ),
#                 mass=0.0,
#                 texture=Gradient(
#                     primary_color=Color(0, 200, 100, 255),
#                     secondary_color=Color(0, 100, 200, 255),
#                 ),
#                 aabb=AABB(size=Vector3([0.5, 0.5, 0.25])),
#             ),
#             GeometryBox(
#                 pose=Pose(
#                     position=Vector3([-0.8 + 0.38, 0.3, 0.125]),
#                     orientation=Quaternion.from_eulers([0.0, math.pi / 4.0, 0.0]),
#                 ),
#                 mass=0.0,
#                 texture=Flat(primary_color=Color(50, 80, 180, 255)),
#                 aabb=AABB(size=Vector3([0.5, 0.4, 0.02])),
#             ),
#             GeometryBox(
#                 pose=Pose(position=Vector3([-0.1, 0.9, 0.5]), orientation=Quaternion()),
#                 mass=0.0,
#                 texture=Flat(
#                     primary_color=Color(100, 0, 100, 255),
#                     base_color=Color(255, 255, 255, 100),
#                 ),
#                 aabb=AABB(size=Vector3([0.2, 0.2, 1.0])),
#             ),
#         ]
#     )

class Evaluator:
    """Provides evaluation of robots."""

    _simulator: LocalSimulator
    _terrain: Terrain

    def __init__(
        self,
        headless: bool,
        num_simulators: int,
    ) -> None:
        """
        Initialize this object.

        :param headless: `headless` parameter for the physics simulator.
        :param num_simulators: `num_simulators` parameter for the physics simulator.
        """
        self._simulator = LocalSimulator(headless=headless, num_simulators=num_simulators)
        self._terrain = terrains.flat()

    def evaluate(
        self,
        robots: list[ModularRobot],
    ) -> list[float]:
        """
        Evaluate multiple robots.

        Fitness is the distance traveled on the xy plane.

        :param robots: The robots to simulate.
        :returns: Fitnesses of the robots.
        """
        # Create the scenes.
        scenes = []
        for robot in robots:
            scene = ModularRobotScene(terrain=terrains.flat())
            scene.add_robot(robot)
            scenes.append(scene)

        # Simulate all scenes.
        scene_states = simulate_scenes(
            simulator=self._simulator,
            batch_parameters=make_standard_batch_parameters(),
            scenes=scenes,
        )

        # Calculate the xy displacements.
        xyz_displacements = [
            fitness_functions.xy_displacement(
                states[0].get_modular_robot_simulation_state(robot),
                states[-1].get_modular_robot_simulation_state(robot),
            )
            for robot, states in zip(robots, scene_states)
        ]

        return xyz_displacements
