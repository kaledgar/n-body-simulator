from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation, PillowWriter
import seaborn as sns
from datetime import datetime

from .n_body import *

animation_space_index_step = 30  # choose every 10th for animation

if __name__ == "__main__":
    plt.style.use("dark_background")
    n = 3
    # Initialize three bodies: Earth, Sun, and a third body
    earth = Body(m=1, r_0=(1, 0), v_0=(0, np.sqrt(333000)), name="earth")
    sun = Body(m=333000, r_0=(0, 0), v_0=(0, 0), name="sun")

    p1 = 0.513938
    p2 = 0.304736

    # http://three-body.ipb.ac.rs/sol.php?id=13
    system = System(
        Body(m=1, r_0=(-1, 0), v_0=(p1 * 1.1, p2), name="b1"),
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
    print(len(sol))
    print(type(sol))
    print(sol.shape)
    print(sol)

    # Extract position data for all bodies from the solution
    num_bodies = len(system.bodies)
    positions = sol[:, : 2 * num_bodies]

    def animate_evolution(solution_matrix: np.ndarray):
        """
        solution_matrix should be np.ndarray of shape: (number_of_time_points, m),
        where m - even number

        [
            [ # x_1_list(t) ],
            [ # y_1_list(t) ],
            [ # x_2_list(t) ],
            [ # y_2_list(t) ],
                ...
            [ # x_n_list(t) ],
            [ # y_n_list(t) ],
        ],

        where: n - # bodies in the System
        """
        assert solution_matrix.shape[1] % 2 == 0
        print("Ok")

    # Plot the trajectories of each body
    x1 = positions[:, 0]
    y1 = positions[:, 1]
    x2 = positions[:, 2]
    y2 = positions[:, 3]
    x3 = positions[:, 4]
    y3 = positions[:, 5]

    plt.plot(x1, label="x1")
    plt.plot(y1, label="y1")
    plt.plot(x2, label="x2")
    plt.plot(y2, label="y2")
    plt.plot(x3, label="x3")
    plt.plot(y3, label="y3")
    plt.legend()
    plt.show()

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
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    plt.grid(True, lw=0.3)

    animated_plots_list: List[Tuple] = [(ax.plot([], []),) for _ in range(n)]

    print(f"animated_plots_list = {animated_plots_list}")

    (animated_plot_l1,) = ax.plot([], [])
    (animated_plot_l2,) = ax.plot([], [])
    (animated_plot_l3,) = ax.plot([], [])

    print(animated_plot_l1)

    def automatic_animation(i):
        for plot_tuple in animated_plots_list:
            pass

    def animate(i):
        # plot lines
        animated_plot_l1.set_data(
            x1[0 : i * animation_space_index_step],
            y1[0 : i * animation_space_index_step],
        )
        animated_plot_l2.set_data(
            x2[0 : i * animation_space_index_step],
            y2[0 : i * animation_space_index_step],
        )
        animated_plot_l3.set_data(
            x3[0 : i * animation_space_index_step],
            y3[0 : i * animation_space_index_step],
        )
        """animated_plot.set_data(
            x1[i * animation_space_index_step], y1[i * animation_space_index_step]
        )
        animated_plot.set_data(
            x2[0 : i * animation_space_index_step],
            y2[0 : i * animation_space_index_step],
        )
        animated_plot.set_data(
            x2[i * animation_space_index_step], y2[i * animation_space_index_step]
        )"""

        return animated_plot_l1, animated_plot_l2, animated_plot_l3

    animation = FuncAnimation(
        fig,
        animate,
        repeat=True,
        interval=1,
        frames=int(len(t) / animation_space_index_step),
    )

    plt.show()
    # animation.save(f"animation_{datetime.now()}.gif", dpi=200, writer=PillowWriter(fps=25))
