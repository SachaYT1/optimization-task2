import numpy as np


def bisection_method(f, a, b, tol):
    # Check if a and b bound a root, i.e., f(a) * f(b) < 0
    # This is a necessary condition for the Bisection Method to work
    if np.sign(f(a)) == np.sign(f(b)):
        raise Exception(
            "The scalars a and b do not bound a root"
        )

    # Compute the midpoint of the interval [a, b]
    c = (a + b) / 2

    # Check if the midpoint is a root or if the tolerance condition is met
    if np.abs(f(c)) < tol:
        return c
    # If f(c) has the same sign as f(a), narrow the interval to [c, b]
    elif np.sign(f(a)) == np.sign(f(c)):
        return bisection_method(f, c, b, tol)
    # If f(c) has the same sign as f(b), narrow the interval to [a, c]
    elif np.sign(f(b)) == np.sign(f(c)):
        return bisection_method(f, a, c, tol)


def main():
    f = lambda x: x ** 3 - 6 * x ** 2 + 11 * x - 6
    a, b = map(float, input("Enter the interval [a, b]: ").split())
    tolerance = float(input("Enter the tolerance (e): "))
    root = bisection_method(f, a, b, tolerance)

    print(root)


if __name__ == '__main__':
    main()
