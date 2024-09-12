from .n_body import *
from matplotlib import pyplot as plt
import numpy as np

if __name__ == "__main__":
    # Initialize three bodies: Earth, Sun, and a third body
    earth = Body(m=1, r_0=(1, 0), v_0=(0, np.sqrt(333000)), name="earth")
    sun = Body(m=333000, r_0=(0, 0), v_0=(0, 0), name="sun")

    p1 = 0.513938
    p2 = 0.304736

    # http://three-body.ipb.ac.rs/sol.php?id=13
    system = System(
        Body(m=1, r_0=(-1, 0), v_0=(p1, p2), name="b1"),
        Body(m=1, r_0=(1, 0), v_0=(p1, p2), name="b2"),
        Body(m=1, r_0=(0, 0), v_0=(-2 * p1, -2 * p2), name="b3"),
    )

    # Time points for solving the differential equations
    t = np.linspace(0, 20, 100000)

    # Solve the system's ODE
    sol = system.solve(t)

    # Extract position data for all bodies from the solution
    num_bodies = len(system.bodies)
    positions = sol[:, : 2 * num_bodies]

    # Plot the trajectories of each body
    plt.figure()
    for i, body in enumerate(system.bodies):
        x = positions[:, 2 * i]
        y = positions[:, 2 * i + 1]
        plt.plot(x, y, label=body.name)

    plt.legend()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Three-Body Problem Simulation")
    plt.show()
