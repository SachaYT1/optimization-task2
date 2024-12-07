import numpy as np

def golden_section(f, a, b, tol):
    # Constants for the golden ratio
    gr = (np.sqrt(5) - 1) / 2  # Golden ratio conjugate (0.618...)


    c = b - gr * (b - a)
    d = a + gr * (b - a)

    while (b - a) > tol:
        if f(c) < f(d):
            b = d
            d = c
            c = b - gr * (b - a)
        else:
            a = c  # Narrow to [c, b]
            c = d
            d = a + gr * (b - a)

    # Approximation of the minimum point and function value
    xmin = (a + b) / 2
    return xmin, f(xmin)

def main():
    f = lambda x: (x - 2)**2 + 3

    # Input interval and tolerance
    a, b = map(float, input("Enter the interval [a, b]: ").split())
    tolerance = float(input("Enter the tolerance (e): "))

    xmin, fmin = golden_section(f, a, b, tolerance)

    # Output the result
    print(f"Approximate xmin: {xmin}")
    print(f"f(xmin): {fmin}")

if __name__ == "__main__":
    main()
