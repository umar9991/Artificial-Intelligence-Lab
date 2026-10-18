"""Python basics assignment for the Artificial Intelligence lab.

Covers functions, validated input, conditionals, match-case, loops,
break/continue, lists, and a two-dimensional matrix.

Set LIVE_INPUT = True in Google Colab to type your own answers.
The default run uses a saved set of answers so the notebook has visible output.
"""

from __future__ import annotations

LIVE_INPUT = False

_DEMO_ANSWERS = [
    "Student",
    "21",
    "2",
    "NumPy",
    "1",
    "2",
    "0.75",
]
_answers = iter(_DEMO_ANSWERS)


def ask(prompt: str) -> str:
    """Read one line. Demo mode prints the prepared answer."""
    print(prompt, end="")
    if LIVE_INPUT:
        return input().strip()
    value = next(_answers)
    print(value)
    return value.strip()


def header(title: str) -> None:
    print()
    print("=" * 54)
    print(f"  {title}")
    print("=" * 54)


def read_name() -> str | None:
    """Keep asking until the name is non-empty. 'exit' stops the program."""
    while True:
        name = ask("Enter your name (or type 'exit' to quit): ")
        if name.lower() == "exit":
            return None
        if name:
            return name
        print("Name cannot be empty. Try again.")


def read_int(prompt: str, minimum: int | None = None) -> int:
    while True:
        raw = ask(prompt)
        try:
            value = int(raw)
        except ValueError:
            print("Enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print(f"Enter a number greater than or equal to {minimum}.")
            continue
        return value


def read_float(prompt: str) -> float:
    while True:
        raw = ask(prompt)
        try:
            return float(raw)
        except ValueError:
            print("Enter a numeric value.")


def age_group(age: int) -> str:
    if age < 13:
        return "Child"
    if age < 20:
        return "Teenager"
    if age < 60:
        return "Adult"
    return "Senior"


def describe_ai_field(choice: str) -> tuple[str, str]:
    """Python 3.10 match-case stands in for a switch statement."""
    match choice:
        case "1":
            return "Machine Learning", "Models that improve by finding patterns in data."
        case "2":
            return "Neural Networks", "Layers of simple units that learn weighted connections."
        case "3":
            return "Natural Language Processing", "Methods for reading and generating human language."
        case _:
            return "Unknown", "Choose 1, 2, or 3."


def show_tools(tools: list[str]) -> None:
    print("AI libraries in the list:")
    for tool in tools:
        print(f"  - {tool}")

    added = ask("Enter another library to append: ")
    tools.append(added)

    print()
    print("Walk the list. Skip 'spaCy'. Stop at 'NumPy'.")
    for tool in tools:
        if tool == "spaCy":
            print("  skip spaCy")
            continue
        if tool == "NumPy":
            print("  stop at NumPy")
            break
        print(f"  visit {tool}")


def show_matrix(matrix: list[list[float]]) -> None:
    for row in matrix:
        print("[ " + " | ".join(f"{value:5.2f}" for value in row) + " ]")


def update_weight(matrix: list[list[float]]) -> None:
    print("Change one weight. Rows and columns are numbered 0, 1, and 2.")
    while True:
        row = read_int("Row index (0-2): ")
        col = read_int("Column index (0-2): ")
        if 0 <= row <= 2 and 0 <= col <= 2:
            break
        print("That position is outside the matrix.")
    matrix[row][col] = read_float(f"New weight at [{row}][{col}]: ")


def countdown(start: int = 3) -> None:
    value = start
    while value > 0:
        print(f"T-minus {value}")
        value -= 1
    print("Ready.")


def main() -> None:
    header("AI Python Basics")
    print("Variables, input, decisions, match-case, loops, lists, and a matrix.")

    name = read_name()
    if name is None:
        print("Goodbye.")
        return

    age = read_int(f"Hello {name}, enter your age: ", minimum=0)
    course = "Artificial Intelligence"
    lab_score = 92.5
    submitted = False
    print(f"Stored values: course={course!r} ({type(course).__name__}), "
          f"age={age} ({type(age).__name__}), "
          f"lab_score={lab_score} ({type(lab_score).__name__}), "
          f"submitted={submitted} ({type(submitted).__name__})")

    header("Age Group")
    print(f"Age {age} falls in the group: {age_group(age)}")

    header("Match-Case")
    print("1. Machine Learning")
    print("2. Neural Networks")
    print("3. Natural Language Processing")
    choice = ask("Choose a field (1-3): ")
    field, description = describe_ai_field(choice)
    print(f"Selected: {field}")
    print(f"Description: {description}")

    header("List, Continue, and Break")
    libraries = ["scikit-learn", "OpenCV", "spaCy", "pandas"]
    show_tools(libraries)
    print("List after append:", libraries)

    header("2D Matrix")
    weights = [
        [0.40, 0.15, 0.70],
        [0.25, 0.55, 0.10],
        [0.80, 0.35, 0.60],
    ]
    print("Starting weights:")
    show_matrix(weights)
    update_weight(weights)
    print("Updated weights:")
    show_matrix(weights)

    header("While Loop")
    countdown()
    print()
    print("Assignment run finished.")


if __name__ == "__main__":
    main()
