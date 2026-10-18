"""Lab: formulate the 8-puzzle and solve it with breadth-first search.

State is a tuple of nine tiles. 0 is the blank.
Goal is (1, 2, 3, 4, 5, 6, 7, 8, 0).

A state is solvable when the number of inversions, ignoring the blank, is even.
BFS expands the shallowest node first, so the path it returns is a shortest path.
"""

from __future__ import annotations

import random
import sys
from collections import deque
from pathlib import Path

GOAL: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7, 8, 0)
OFFSETS = {"Up": -3, "Down": 3, "Left": -1, "Right": 1}
OPPOSITE = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}


def header(title: str) -> None:
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def actions(state: tuple[int, ...]) -> list[str]:
    index = state.index(0)
    row, col = divmod(index, 3)
    found: list[str] = []
    if row > 0:
        found.append("Up")
    if row < 2:
        found.append("Down")
    if col > 0:
        found.append("Left")
    if col < 2:
        found.append("Right")
    return found


def result(state: tuple[int, ...], action: str) -> tuple[int, ...]:
    index = state.index(0)
    swap = index + OFFSETS[action]
    tiles = list(state)
    tiles[index], tiles[swap] = tiles[swap], tiles[index]
    return tuple(tiles)


def goal_test(state: tuple[int, ...]) -> bool:
    return state == GOAL


def inversion_count(state: tuple[int, ...]) -> int:
    tiles = [tile for tile in state if tile != 0]
    return sum(1 for i, tile in enumerate(tiles) for later in tiles[i + 1 :] if tile > later)


def is_solvable(state: tuple[int, ...]) -> bool:
    return inversion_count(state) % 2 == 0


def solve_bfs(start: tuple[int, ...]) -> tuple[list[str], int] | None:
    """Return the shortest action list and the number of nodes expanded."""
    if not is_solvable(start):
        return None
    frontier: deque[tuple[tuple[int, ...], list[str]]] = deque([(start, [])])
    seen = {start}
    expanded = 0
    while frontier:
        state, path = frontier.popleft()
        expanded += 1
        if goal_test(state):
            return path, expanded
        for action in actions(state):
            child = result(state, action)
            if child not in seen:
                seen.add(child)
                frontier.append((child, path + [action]))
    return None


def format_board(state: tuple[int, ...]) -> str:
    lines = []
    for row in range(3):
        cells = []
        for col in range(3):
            tile = state[row * 3 + col]
            cells.append(" ." if tile == 0 else f"{tile:2d}")
        lines.append(" ".join(cells))
    return "\n".join(lines)


def print_solution(start: tuple[int, ...], path: list[str]) -> None:
    print("Start")
    print(format_board(start))
    state = start
    for step, action in enumerate(path, start=1):
        state = result(state, action)
        print(f"Move {step}: {action}")
        print(format_board(state))
        print()


def scramble(moves: int, seed: int) -> tuple[int, ...]:
    """Apply `moves` legal steps from the goal, without immediately undoing one."""
    rng = random.Random(seed)
    state = GOAL
    previous: str | None = None
    for _ in range(moves):
        choices = [action for action in actions(state) if action != OPPOSITE.get(previous or "")]
        action = rng.choice(choices)
        state = result(state, action)
        previous = action
    return state


def theory() -> None:
    header("Problem Formulation")
    print("Initial state: a permutation of the eight tiles and the blank.")
    print("Actions: slide the blank Up, Down, Left, or Right when the edge allows it.")
    print("Transition: swap the blank with the neighboring tile.")
    print("Goal test: the tiles read 1 through 8, with the blank last.")
    print("Path cost: 1 for every slide. BFS therefore returns a shortest solution.")
    print("Solvable states have an even number of inversions. The blank is ignored.")


def task_known_start() -> tuple[int, ...] | None:
    header("Task 1: Solve (8, 1, 3, 4, 0, 2, 7, 6, 5)")
    start = (8, 1, 3, 4, 0, 2, 7, 6, 5)
    print(format_board(start))
    print(f"Inversions: {inversion_count(start)}")
    print(f"Solvable: {is_solvable(start)}")
    solved = solve_bfs(start)
    if solved is None:
        print("No solution.")
        return None
    path, expanded = solved
    print(f"Shortest path has {len(path)} moves.")
    print(f"Nodes expanded: {expanded}")
    print("Actions:", " ".join(path))
    return start


def task_print_path(start: tuple[int, ...]) -> None:
    header("Task 2: Board after Every Move")
    solved = solve_bfs(start)
    if solved is None:
        print("No path to print.")
        return
    path, _ = solved
    print_solution(start, path)


def task_scaling() -> None:
    header("Task 3: Scramble Depth and Nodes Expanded")
    print("Each start is the goal after N random moves that do not undo the previous move.")
    print("Solution length is the optimal BFS depth, which can be shorter than N.")
    print(f"{'Moves':>6}  {'Optimal':>8}  {'Expanded':>10}  Solvable")
    depths: list[int] = []
    expanded_counts: list[int] = []
    for moves in (5, 10, 15, 20, 25):
        start = scramble(moves, seed=moves)
        solved = solve_bfs(start)
        if solved is None:
            print(f"{moves:6d}  {'n/a':>8}  {'n/a':>10}  False")
            continue
        path, expanded = solved
        depths.append(len(path))
        expanded_counts.append(expanded)
        print(f"{moves:6d}  {len(path):8d}  {expanded:10d}  True")
    print()
    print("Nodes expanded")
    peak = max(expanded_counts) if expanded_counts else 1
    for moves, count in zip((5, 10, 15, 20, 25), expanded_counts):
        bar = "#" * max(1, round(40 * count / peak))
        print(f"  {moves:2d} | {bar} {count}")
    plot_scaling([5, 10, 15, 20, 25], expanded_counts)


def plot_scaling(moves: list[int], expanded_counts: list[int]) -> None:
    try:
        import matplotlib

        if "ipykernel" not in sys.modules and "google.colab" not in sys.modules:
            matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed. The text chart above is the record.")
        return
    figure, axis = plt.subplots(figsize=(7, 4))
    axis.plot(moves, expanded_counts, marker="o")
    axis.set_xlabel("Random moves from the goal")
    axis.set_ylabel("Nodes expanded by BFS")
    axis.set_title("8-puzzle: search cost grows with scramble length")
    axis.grid(True, alpha=0.3)
    figure.tight_layout()
    try:
        figure_path = Path(__file__).resolve().parents[1] / "notebooks" / "eight_puzzle_scaling.png"
        figure_path.parent.mkdir(exist_ok=True)
    except NameError:
        figure_path = Path("eight_puzzle_scaling.png")
    figure.savefig(figure_path, dpi=120)
    print(f"Saved plot: {figure_path}")
    plt.show()
    plt.close(figure)


def task_unsolvable() -> None:
    header("Task 4: An Unsolvable State")
    start = (1, 2, 3, 4, 5, 6, 8, 7, 0)
    print(format_board(start))
    print(f"Inversions: {inversion_count(start)} (one swap of 8 and 7)")
    print(f"Solvable: {is_solvable(start)}")
    print("BFS is not started. An odd inversion count cannot reach the goal,")
    print("and searching it would eventually exhaust the odd-parity half of the space.")


def missionaries() -> None:
    header("Post-Lab: Missionaries and Cannibals")
    print("State: (missionaries on the left, cannibals on the left, boat on the left).")
    print("Boat flag 1 means left bank. The right bank holds whoever is not on the left.")
    print("A bank is safe when it has no missionaries or at least as many missionaries as cannibals.")

    start = (3, 3, 1)
    goal = (0, 0, 0)
    loads = ((1, 0), (2, 0), (0, 1), (0, 2), (1, 1))

    def safe(missionaries: int, cannibals: int) -> bool:
        if not 0 <= missionaries <= 3 or not 0 <= cannibals <= 3:
            return False
        right_m, right_c = 3 - missionaries, 3 - cannibals
        left_ok = missionaries == 0 or missionaries >= cannibals
        right_ok = right_m == 0 or right_m >= right_c
        return left_ok and right_ok

    def neighbors(state: tuple[int, int, int]) -> list[tuple[tuple[int, int, int], str]]:
        missionaries, cannibals, boat_left = state
        direction = -1 if boat_left else 1
        bank = "right" if boat_left else "left"
        found = []
        for take_m, take_c in loads:
            next_state = (
                missionaries + direction * take_m,
                cannibals + direction * take_c,
                1 - boat_left,
            )
            if safe(*next_state[:2]):
                label = (
                    f"send {take_m} {'missionary' if take_m == 1 else 'missionaries'}"
                    f" and {take_c} {'cannibal' if take_c == 1 else 'cannibals'} to the {bank}"
                )
                found.append((next_state, label))
        return found

    frontier: deque[tuple[tuple[int, int, int], list[str]]] = deque([(start, [])])
    seen = {start}
    solution: list[str] | None = None
    expanded = 0
    while frontier:
        state, path = frontier.popleft()
        expanded += 1
        if state == goal:
            solution = path
            break
        for child, label in neighbors(state):
            if child not in seen:
                seen.add(child)
                frontier.append((child, path + [f"{label} -> {child}"]))
    if solution is None:
        print("No solution found.")
        return
    print(f"Shortest plan has {len(solution)} crossings. Nodes expanded: {expanded}")
    print(f"Start: {start}")
    for step, label in enumerate(solution, start=1):
        print(f"{step:2d}. {label}")


def main() -> None:
    theory()
    start = task_known_start()
    if start is not None:
        task_print_path(start)
    task_scaling()
    task_unsolvable()
    missionaries()
    print()
    print("Lab complete.")


if __name__ == "__main__":
    main()
