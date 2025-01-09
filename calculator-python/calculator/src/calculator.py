pi_string = "3.14159265358979323846264338327950288419716939937510"

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Error: Division by zero.")
    return a / b

def calculate_pi(digits):
    if digits < 1:
        return "3"
    if digits > len(pi_string) - 2:
        digits = len(pi_string) - 2
    return pi_string[:digits + 2]  # +2 to include "3."

def calculate_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def calculate_compound_interest(principal, rate, time, n):
    return principal * (1 + rate / n) ** (n * time)

def calculate_simple_interest(principal, rate, time):
    return principal * rate * time