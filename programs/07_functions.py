"""Lab 1 - Program 7: Functions."""


def rectangle_area(length, width):
    return length * width


def is_prime(value):
    if value < 2:
        return False
    for divisor in range(2, int(value ** 0.5) + 1):
        if value % divisor == 0:
            return False
    return True


def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


length = float(input("Enter rectangle length: "))
width = float(input("Enter rectangle width: "))
print("Area:", rectangle_area(length, width))

candidate = int(input("Enter an integer to test for prime: "))
if is_prime(candidate):
    print(f"{candidate} is prime.")
else:
    print(f"{candidate} is not prime.")

celsius = float(input("Enter temperature in Celsius: "))
print(f"{celsius} C = {celsius_to_fahrenheit(celsius)} F")
