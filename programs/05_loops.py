"""Lab 1 - Program 5: Loops (multiplication table, sum, and factorial)."""

number = int(input("Enter a positive integer: "))

print(f"\nMultiplication table of {number}")
for i in range(1, 11):
    print(f"{number} x {i} = {number * i}")

total = 0
count = 1
while count <= number:
    total += count
    count += 1
print(f"\nSum of numbers from 1 to {number} = {total}")

factorial = 1
for i in range(1, number + 1):
    factorial *= i
print(f"Factorial of {number} = {factorial}")
