import numpy as np
from scipy.integrate import odeint
from typing import List, Dict, Tuple, Self, Any
from itertools import chain, combinations

G = 1  # Gravitational constant


class Body:
    def __init__(
        self,
        m: float,
        r_0: Tuple[float, float],
        v_0: Tuple[float, float],
        name: str = "body",
    ) -> None:
        self.m = m  # Mass of the body
        self.r_0 = r_0  # Initial position (x, y)
        self.v_0 = v_0  # Initial velocity (vx, vy)
        self.name = name  # Name of the body

    def distance(self, other: Self) -> float:
        """Calculate the distance between two bodies."""
        return np.sqrt(
            (self.r_0[0] - other.r_0[0]) ** 2 + (self.r_0[1] - other.r_0[1]) ** 2
        )


class System:
    def __init__(self, *bodies: Body) -> None:
        self.bodies: List[Body] = list(bodies)
        self.bodies_dict: Dict[str, Body] = {body.name: body for body in bodies}
        self.interactions = self.calculate_interactions()

    def prepare_initial_data(self) -> Dict[str, Any]:
        """Prepare initial positions and velocities for all bodies."""
        positions = [[body.r_0[0], body.r_0[1]] for body in self.bodies]
        velocities = [[body.v_0[0], body.v_0[1]] for body in self.bodies]

        # Flatten the lists and prepare the state vector
        s_0 = list(chain(*positions, *velocities))
        return {"s_0": s_0}

    def get_all_unique_bodies_combinations(self) -> List[Tuple[Body, Body]]:
        """Get all unique body pairs for interaction calculation."""
        return list(combinations(self.bodies, 2))

    def calculate_interactions(self) -> Dict[str, Dict[str, float]]:
        """Calculate initial accelerations due to gravitational interactions."""
        epsilon_space = 1e-9
        accs = {body.name: {"a_x": 0.0, "a_y": 0.0} for body in self.bodies}

        for body1, body2 in self.get_all_unique_bodies_combinations():
            r_x = body2.r_0[0] - body1.r_0[0]
            r_y = body2.r_0[1] - body1.r_0[1]
            distance = body1.distance(body2)
            if distance - epsilon_space < 0:
                continue

            acc1 = G * body2.m / distance**3
            acc2 = G * body1.m / distance**3

            # Update accelerations
            accs[body1.name]["a_x"] += acc1 * r_x
            accs[body1.name]["a_y"] += acc1 * r_y
            accs[body2.name]["a_x"] -= acc2 * r_x
            accs[body2.name]["a_y"] -= acc2 * r_y

        return accs

    def derivatives(self, s: List[float], t: float) -> List[float]:
        """Calculate the derivatives of the system at time t."""
        num_bodies = len(self.bodies)
        positions = np.reshape(s[: 2 * num_bodies], (num_bodies, 2))
        velocities = np.reshape(s[2 * num_bodies :], (num_bodies, 2))
        accelerations = np.zeros_like(positions)

        for i, body1 in enumerate(self.bodies):
            for j, body2 in enumerate(self.bodies):
                if i != j:
                    r = positions[j] - positions[i]
                    distance = np.linalg.norm(r)
                    if distance < 1e-6:
                        continue
                    acc = G * body2.m * r / distance**3
                    accelerations[i] += acc

        # Flatten velocities and accelerations for the return value
        dsdt = np.concatenate((velocities, accelerations)).flatten()
        return dsdt

    def solve(self, t: np.ndarray) -> np.ndarray:
        """Solve the system of ODEs."""
        initial_data = self.prepare_initial_data()
        s_0 = initial_data["s_0"]
        solution = odeint(self.derivatives, s_0, t)
        return solution
