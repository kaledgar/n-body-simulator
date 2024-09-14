from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation, PillowWriter
import seaborn as sns
from datetime import datetime

from .n_body import *

animation_space_index_step = 30  # choose every 10th for animation

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
    t_min = 0
    t_max = 20
    t_points_count = 100_000

    t = np.linspace(t_min, t_max, t_points_count)

    # Solve the system's ODE
    sol = system.solve(t)

    # Extract position data for all bodies from the solution
    num_bodies = len(system.bodies)
    positions = sol[:, : 2 * num_bodies]

    # Plot the trajectories of each body
    plt.figure()
    """for i, body in enumerate(system.bodies):
        x = positions[:, 2 * i]
        y = positions[:, 2 * i + 1]
        plt.plot(x, y, label=body.name)
    """

    x1 = positions[:, 0]
    y1 = positions[:, 1]
    x2 = positions[:, 2]
    y2 = positions[:, 3]
    x3 = positions[:, 4]
    y3 = positions[:, 5]

    print(len(x1))
    """
    plt.plot(x1, y1, label="b1")
    plt.plot(x2, y2, label="b2")
    plt.plot(x3, y3, label="b3")

    plt.legend()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Three-Body Problem Simulation")
    plt.show()"""

    fig, ax = plt.subplots()
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)

    (animated_plot,) = ax.plot([], [])

    print(animated_plot)

    def animate(i):
        animated_plot.set_data(
            x1[0 : i * animation_space_index_step],
            y1[0 : i * animation_space_index_step],
        )

        return (animated_plot,)

    animation = FuncAnimation(
        fig,
        animate,
        repeat=True,
        interval=1,
        frames=int(len(t) / animation_space_index_step),
    )

    plt.show()
    # animation.save(f"animation_{datetime.now()}.gif", dpi=200, writer=PillowWriter(fps=25))
