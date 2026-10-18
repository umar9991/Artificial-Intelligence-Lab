"""Lab 1 - Program 3: Simple arithmetic calculator."""

print("Simple Calculator")
print("Operations: +  -  *  /")

first = float(input("Enter the first number: "))
operator = input("Enter an operator (+, -, *, /): ").strip()
second = float(input("Enter the second number: "))

if operator == "+":
    result = first + second
elif operator == "-":
    result = first - second
elif operator == "*":
    result = first * second
elif operator == "/":
    if second == 0:
        print("Cannot divide by zero.")
        result = None
    else:
        result = first / second
else:
    print("Unknown operator.")
    result = None

if result is not None:
    print(f"{first} {operator} {second} = {result}")
