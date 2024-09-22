from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation, PillowWriter
import seaborn as sns
from datetime import datetime

from .n_body import *
from .constants import animation_index_multiplier
from .initial_conditions import yin_yang_1a, earth_sun_system


def get_positions_from_solution(solution_arr: np.ndarray) -> Tuple[np.ndarray, int]:
    """
    Extracts array with positions from the solution_array.
    solution_arr should be np.ndarray of shape: (number_of_time_points, 4*n),
    where: n - # bodies in the System.

    Output of this function has the following form:

    [
        [ # x_1_list(t) ],
        [ # y_1_list(t) ],
        [ # x_2_list(t) ],
        [ # y_2_list(t) ],
            ...
        [ # x_n_list(t) ],
        [ # y_n_list(t) ],
    ]

    Args:
        solution_arr (np.ndaray) - Output of system.solve() or np.odeint().

    Returns:
        positions_arr (np.ndarray) - array containing positons of the bodies.
    """
    assert solution_arr.shape[1] % 2 == 0
    body_count: int = int(sol.shape[1] / 4)
    print(f"Ok, body_cout = {body_count}")
    return solution_arr[:, : 2 * body_count], body_count


def prepare_animation_from_solution_arr(solution_arr: np.ndarray) -> None:
    """Responsible for generating animation"""
    solution_arr, n = get_positions_from_solution(solution_arr)
    print(f"solution_arr = {solution_arr.shape}, n = {n}")

    animated_plots_list: List[Tuple] = [(ax.plot([], []),) for _ in range(n)]
    return solution_arr, n


if __name__ == "__main__":
    plt.style.use("dark_background")

    # Time points for solving the differential equations
    t_min = 0
    t_max = 20
    t_points_count = 100_000

    t = np.linspace(t_min, t_max, t_points_count)

    # Solve the system's ODE
    sol = yin_yang_1a.solve(t)
    positions, n = get_positions_from_solution(sol)

    # Plot the trajectories of each body
    x1 = positions[:, 0]
    y1 = positions[:, 1]
    x2 = positions[:, 2]
    y2 = positions[:, 3]
    x3 = positions[:, 4]
    y3 = positions[:, 5]

    print(len(x1))

    fig, ax = plt.subplots()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    plt.grid(True, lw=0.3)

    animated_plots_list: List[Tuple] = [(ax.plot([], []),) for _ in range(n)]
    for i, plot_tuple in enumerate(animated_plots_list):
        print(f"i={i}, plot_tuple={plot_tuple[0]}, type = {type(plot_tuple)}")
    print(f"animated_plots_list = {animated_plots_list}")

    (animated_plot_l1,) = ax.plot([], [])
    (animated_plot_l2,) = ax.plot([], [])
    (animated_plot_l3,) = ax.plot([], [])

    print(animated_plot_l1)

    def automatic_animation(i):
        # Prepare Line2D objects
        print(f"Message from automatic_animation: ")
        animation_list = []
        for i, plot_tuple in enumerate(animated_plots_list):
            print(f"i = {i}, plot_tuple[0][0] = {plot_tuple[0][0]}")
            animation_object = plot_tuple[0][0].set_data(
                positions[:, 2 * i][0 : i * animation_index_multiplier],
                positions[:, 2 * i + 1][0 : i * animation_index_multiplier],
            )
            animation_list.append(animation_object)

        print(animation_list)
        return animation_list

    automatic_animation(1)

    def animate(i):
        # plot lines
        animated_plot_l1.set_data(
            x1[0 : i * animation_index_multiplier],
            y1[0 : i * animation_index_multiplier],
        )
        animated_plot_l2.set_data(
            x2[0 : i * animation_index_multiplier],
            y2[0 : i * animation_index_multiplier],
        )
        animated_plot_l3.set_data(
            x3[0 : i * animation_index_multiplier],
            y3[0 : i * animation_index_multiplier],
        )
        """animated_plot.set_data(
            x1[i * animation_index_multiplier], y1[i * animation_index_multiplier]
        )
        animated_plot.set_data(
            x2[0 : i * animation_index_multiplier],
            y2[0 : i * animation_index_multiplier],
        )
        animated_plot.set_data(
            x2[i * animation_index_multiplier], y2[i * animation_index_multiplier]
        )"""

        return animated_plot_l1, animated_plot_l2, animated_plot_l3

    animation = FuncAnimation(
        fig,
        animate,
        repeat=True,
        interval=1,
        frames=int(len(t) / animation_index_multiplier),
    )
    plt.title(yin_yang_1a.name)
    plt.show()
    # animation.save(f"animation_{datetime.now()}.gif", dpi=200, writer=PillowWriter(fps=25))
