"""Lab: intelligent agents in the vacuum world.

Tasks
1. Describe two real AI applications.
2. Give PEAS descriptions and environment properties.
3. Compare a simple reflex agent with a random agent on the same worlds.
4. Add a model-based agent that remembers cleaned squares.
5. Post-lab: a 3x3 model-based agent that visits every cell.

Performance
+10 when Suck removes dirt, -1 for a move, -1 for sucking a clean square.
NoOp scores 0. The same initial world is given to every agent in a trial.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field


CLEAN = 0
DIRTY = 1


def header(title: str) -> None:
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def task_applications() -> None:
    header("Task 1: Two AI Applications")
    print("Google Lens")
    print("  Input: a camera image of an object, plant, or sign.")
    print("  Output: a label, related pages, or translated text.")
    print("  Technique: a convolutional network trained for visual recognition.")
    print("  Limit: blur, darkness, and unusual objects reduce accuracy.")
    print()
    print("A conversational language model")
    print("  Input: a text prompt.")
    print("  Output: a written reply that follows the prompt.")
    print("  Technique: a transformer language model.")
    print("  Limit: it can state false details with a confident tone.")


def task_peas() -> None:
    header("Task 2: PEAS and Environment Properties")
    print("Chess program with a clock")
    print("  Performance: win the game and spend less clock time.")
    print("  Environment: the board, the opponent, and the clock.")
    print("  Actuators: the chosen move shown on the board.")
    print("  Sensors: piece positions, whose turn it is, and remaining time.")
    print("  Properties: fully observable, deterministic, sequential,")
    print("  semi-dynamic because the clock changes, discrete, multi-agent.")
    print()
    print("Online English tutor")
    print("  Performance: gains in grammar, vocabulary, and fluency.")
    print("  Environment: the learner, the lesson, and the network.")
    print("  Actuators: explanations, exercises, and scores.")
    print("  Sensors: typed answers, quiz results, and time on task.")
    print("  Properties: partially observable, stochastic, sequential,")
    print("  dynamic, discrete, multi-agent.")
    print()
    print("Parcel drone over Islamabad")
    print("  Performance: on-time delivery, safety, and battery use.")
    print("  Environment: airspace, buildings, weather, and other aircraft.")
    print("  Actuators: rotors, navigation commands, and the parcel release.")
    print("  Sensors: GPS, camera, lidar, and altitude.")
    print("  Properties: partially observable, stochastic, sequential,")
    print("  dynamic, continuous, multi-agent.")


@dataclass
class VacuumWorld:
    status: dict[str, int]
    location: str

    def percept(self) -> tuple[str, int]:
        return self.location, self.status[self.location]

    def execute(self, action: str) -> int:
        """Apply an action. Return the dirt removed by this action (0 or 1)."""
        if action == "Suck":
            removed = self.status[self.location]
            self.status[self.location] = CLEAN
            return removed
        if action == "Right":
            self.location = "B"
        elif action == "Left":
            self.location = "A"
        return 0

    def is_clean(self) -> bool:
        return self.status["A"] == CLEAN and self.status["B"] == CLEAN


def make_world(seed: int) -> VacuumWorld:
    rng = random.Random(seed)
    return VacuumWorld(
        status={"A": rng.randint(CLEAN, DIRTY), "B": rng.randint(CLEAN, DIRTY)},
        location=rng.choice(["A", "B"]),
    )


def reflex_action(percept: tuple[str, int]) -> str:
    location, dirt = percept
    if dirt == DIRTY:
        return "Suck"
    return "Right" if location == "A" else "Left"


def random_action(percept: tuple[str, int], rng: random.Random) -> str:
    del percept
    return rng.choice(["Left", "Right", "Suck"])


@dataclass
class ModelBasedVacuum:
    belief: dict[str, str] = field(default_factory=lambda: {"A": "Unknown", "B": "Unknown"})

    def act(self, percept: tuple[str, int]) -> str:
        location, dirt = percept
        self.belief[location] = "Dirty" if dirt == DIRTY else "Clean"
        if dirt == DIRTY:
            return "Suck"
        if self.belief["A"] == "Clean" and self.belief["B"] == "Clean":
            return "NoOp"
        return "Right" if location == "A" else "Left"


def score_step(action: str, dirt_removed: int) -> int:
    if action == "Suck":
        return 10 if dirt_removed else -1
    if action in {"Left", "Right", "Up", "Down"}:
        return -1
    return 0


def run_two_square(agent_name: str, seed: int, max_steps: int, stop_when_clean: bool) -> tuple[int, int]:
    world = make_world(seed)
    rng = random.Random(seed + 1000)
    agent = ModelBasedVacuum()
    score = 0
    steps = 0
    for _ in range(max_steps):
        if stop_when_clean and world.is_clean():
            break
        percept = world.percept()
        if agent_name == "reflex":
            action = reflex_action(percept)
        elif agent_name == "random":
            action = random_action(percept, rng)
        else:
            action = agent.act(percept)
        removed = world.execute(action)
        score += score_step(action, removed)
        steps += 1
        if action == "NoOp":
            break
    return score, steps


def compare_until_clean(trials: int = 10) -> None:
    header("Task 3: Reflex Agent and Random Agent until the World Is Clean")
    print(f"{'Trial':>5}  {'Start':<16}  {'Reflex':>14}  {'Random':>14}")
    reflex_scores: list[int] = []
    random_scores: list[int] = []
    reflex_steps: list[int] = []
    random_steps: list[int] = []
    for trial in range(1, trials + 1):
        start = make_world(trial)
        start_text = f"{start.location} A={start.status['A']} B={start.status['B']}"
        r_score, r_steps = run_two_square("reflex", trial, 100, stop_when_clean=True)
        n_score, n_steps = run_two_square("random", trial, 100, stop_when_clean=True)
        reflex_scores.append(r_score)
        random_scores.append(n_score)
        reflex_steps.append(r_steps)
        random_steps.append(n_steps)
        print(
            f"{trial:5d}  {start_text:<16}  "
            f"{r_score:4d} ({r_steps:2d} steps)  {n_score:4d} ({n_steps:2d} steps)"
        )
    print("-" * 70)
    print(f"Mean reflex score {sum(reflex_scores) / trials:.2f}, mean steps {sum(reflex_steps) / trials:.2f}")
    print(f"Mean random score {sum(random_scores) / trials:.2f}, mean steps {sum(random_steps) / trials:.2f}")
    if sum(reflex_steps) < sum(random_steps):
        print("The reflex agent finishes in fewer steps. It uses the current percept.")
    print("A random agent can still score well on a short lucky run. Steps are the fair measure.")


def compare_model_based(trials: int = 10, horizon: int = 20) -> None:
    header("Task 4: Model-Based Agent and Simple Reflex Agent over a Fixed Horizon")
    print("The reflex agent has no memory, so it keeps moving after the world is clean.")
    print(f"Horizon: {horizon} steps. NoOp ends the model-based episode early.")
    print(f"{'Trial':>5}  {'Model-based':>12}  {'Reflex':>8}")
    model_scores: list[int] = []
    reflex_scores: list[int] = []
    for trial in range(1, trials + 1):
        model_score, _ = run_two_square("model", trial, horizon, stop_when_clean=False)
        reflex_score, _ = run_two_square("reflex", trial, horizon, stop_when_clean=False)
        model_scores.append(model_score)
        reflex_scores.append(reflex_score)
        print(f"{trial:5d}  {model_score:12d}  {reflex_score:8d}")
    print("-" * 70)
    print(f"Mean model-based score {sum(model_scores) / trials:.2f}")
    print(f"Mean reflex score       {sum(reflex_scores) / trials:.2f}")

    header("Trace: Model-Based Agent, Seed 4")
    world = make_world(4)
    agent = ModelBasedVacuum()
    score = 0
    print(f"Start location {world.location}, status {world.status}")
    for step in range(1, 9):
        percept = world.percept()
        action = agent.act(percept)
        removed = world.execute(action)
        score += score_step(action, removed)
        print(f"Step {step}: percept={percept} action={action:<5} world={world.status} score={score}")
        if action == "NoOp":
            break


@dataclass
class GridWorld:
    grid: list[list[int]]
    row: int
    col: int

    def percept(self) -> tuple[int, int, int]:
        return self.row, self.col, self.grid[self.row][self.col]

    def execute(self, action: str) -> int:
        if action == "Suck":
            removed = self.grid[self.row][self.col]
            self.grid[self.row][self.col] = CLEAN
            return removed
        moves = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
        if action not in moves:
            return 0
        dr, dc = moves[action]
        next_row, next_col = self.row + dr, self.col + dc
        if 0 <= next_row <= 2 and 0 <= next_col <= 2:
            self.row, self.col = next_row, next_col
        return 0

    def all_clean(self) -> bool:
        return all(cell == CLEAN for row in self.grid for cell in row)


class GridModelAgent:
    """Remember what has been seen and walk to the nearest unknown cell."""

    def __init__(self) -> None:
        self.known: dict[tuple[int, int], int] = {}

    def act(self, percept: tuple[int, int, int]) -> str:
        row, col, dirt = percept
        self.known[(row, col)] = dirt
        if dirt == DIRTY:
            return "Suck"
        if len(self.known) == 9 and all(value == CLEAN for value in self.known.values()):
            return "NoOp"
        unknown = [
            (r, c)
            for r in range(3)
            for c in range(3)
            if (r, c) not in self.known
        ]
        if not unknown:
            return "NoOp"
        target = min(unknown, key=lambda cell: (abs(cell[0] - row) + abs(cell[1] - col), cell))
        return self._step_toward(row, col, target)

    @staticmethod
    def _step_toward(row: int, col: int, target: tuple[int, int]) -> str:
        target_row, target_col = target
        if row < target_row:
            return "Down"
        if row > target_row:
            return "Up"
        if col < target_col:
            return "Right"
        return "Left"


def make_grid(seed: int) -> GridWorld:
    rng = random.Random(seed)
    grid = [[rng.randint(CLEAN, DIRTY) for _ in range(3)] for _ in range(3)]
    return GridWorld(grid=grid, row=rng.randint(0, 2), col=rng.randint(0, 2))


def run_grid(seed: int, trace: bool) -> tuple[int, int, int]:
    world = make_grid(seed)
    agent = GridModelAgent()
    score = 0
    moves = 0
    cleaned = 0
    if trace:
        print("Initial grid:")
        for row in world.grid:
            print(f"  {row}")
        print(f"Start cell: ({world.row}, {world.col})")
    for step in range(1, 40):
        percept = world.percept()
        action = agent.act(percept)
        removed = world.execute(action)
        score += score_step(action, removed)
        if action == "Suck" and removed:
            cleaned += 1
        elif action in {"Up", "Down", "Left", "Right"}:
            moves += 1
        if trace:
            print(
                f"Step {step:2d}: percept={percept} action={action:<5} "
                f"cell=({world.row},{world.col}) score={score}"
            )
        if action == "NoOp" and world.all_clean():
            if trace:
                print("Every cell has been observed clean. The agent stops.")
            break
    return moves, cleaned, score


def task_grid() -> None:
    header("Post-Lab: 3x3 Model-Based Agent")
    print("The agent stores the cells it has seen and walks to the nearest unseen cell.")
    print("That works from any starting square. A one-way sweep would miss cells behind it.")
    run_grid(seed=42, trace=True)
    print()
    print(f"{'Seed':>5}  {'Moves':>6}  {'Cleaned':>8}  {'Score':>6}")
    totals = [0, 0, 0]
    for seed in range(1, 11):
        moves, cleaned, score = run_grid(seed, trace=False)
        totals[0] += moves
        totals[1] += cleaned
        totals[2] += score
        print(f"{seed:5d}  {moves:6d}  {cleaned:8d}  {score:6d}")
    print("-" * 40)
    print(
        f"Means over 10 grids: moves {totals[0] / 10:.2f}, "
        f"cleaned {totals[1] / 10:.2f}, score {totals[2] / 10:.2f}"
    )


def task_viva() -> None:
    header("Viva Notes")
    print("Agent function: the mapping from a percept sequence to the action it should take.")
    print("Agent program: the code that implements that mapping on a machine.")
    print()
    print("A simple reflex agent sees only the latest percept. In a partially")
    print("observable world that is not enough, because the hidden part of the")
    print("state still matters. A model supplies the missing memory.")
    print()
    print("In this vacuum world, Suck, Left, and Right have fixed results.")
    print("The initial dirt is chosen at random, so the episode starts from a")
    print("random state and then proceeds deterministically.")
    print()
    print("A navigation app is a utility-based agent: it trades off travel time,")
    print("distance, tolls, and traffic instead of following one fixed rule.")


def main() -> None:
    task_applications()
    task_peas()
    compare_until_clean()
    compare_model_based()
    task_grid()
    task_viva()
    print()
    print("Lab complete.")


if __name__ == "__main__":
    main()
