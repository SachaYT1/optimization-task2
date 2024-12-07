def gradient_ascent(f_prime, x0, alpha, N):
    x = x0
    for _ in range(N):
        x += alpha * f_prime(x) # Update x based on gradient and learning rate

    return x

def main():
    # Define the derivative of the function
    f_prime = lambda x: -2 * x + 4

    # Define the original function for evaluation
    f = lambda x: -x**2 + 4 * x + 1

    # Input initial guess, learning rate, and iterations
    x0 = float(input("Enter the initial guess x0: "))
    alpha = float(input("Enter the learning rate (alpha): "))
    N = int(input("Enter the number of iterations (N): "))

    # Perform gradient ascent
    xmax = gradient_ascent(f_prime, x0, alpha, N)

    # Output results
    print(f"Approximate xmax: {xmax}")
    print(f"f(xmax): {f(xmax)}")

if __name__ == "__main__":
    main()
