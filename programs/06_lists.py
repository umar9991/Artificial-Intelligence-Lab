"""Lab 1 - Program 6: Lists (store numbers, then summarize them)."""

raw = input("Enter numbers separated by spaces: ")
numbers = [float(item) for item in raw.split()]

if not numbers:
    print("No numbers were entered.")
else:
    print("Numbers:", numbers)
    print("Count:", len(numbers))
    print("Sum:", sum(numbers))
    print("Average:", sum(numbers) / len(numbers))
    print("Minimum:", min(numbers))
    print("Maximum:", max(numbers))
    print("Sorted:", sorted(numbers))
