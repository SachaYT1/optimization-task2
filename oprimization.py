def min_value(vector):
    return min(vector)


def interior_point_method(C, A, b, x0, epsilon, alpha, max_iterations=10):
    x = x0[:]
    print("Iter.\t x1\t x2\t x3\t x4\t Z")

    for iteration in range(max_iterations):
        D = [[x[i] if i == j else 0 for j in range(len(x))] for i in range(len(x))]

        A_tilde = matrix_multiply(A, D)
        C_tilde = matrix_vector_multiply(D, C)
        A_tilde_T = transpose(A_tilde)

        I = identity_matrix(len(A_tilde_T))
        A_tilde_A_tilde_T = matrix_multiply(A_tilde, A_tilde_T)

        try:
            inv_A_tilde_A_tilde_T = invert_matrix(A_tilde_A_tilde_T)
        except ValueError:
            print("The method is not applicable due to a singular matrix.")
            return

        PA_part = matrix_multiply(A_tilde_T, matrix_multiply(inv_A_tilde_A_tilde_T, A_tilde))
        P = [[I[i][j] - PA_part[i][j] for j in range(len(I))] for i in range(len(I))]

        c_p = matrix_vector_multiply(P, C_tilde)
        v = min_value(c_p)

        if v == 0:
            print("v is zero; stopping to avoid division by zero.")
            break

        scaled_c_p = [(alpha / abs(v)) * val for val in c_p]
        x_tilde = [1 + scaled_c_p[i] for i in range(len(scaled_c_p))]
        x = matrix_vector_multiply(D, x_tilde)

        objective = sum(C[i] * x[i] for i in range(len(C)))

        x_values = "\t".join(f"{xi:.5f}" for xi in x)
        print(f"{iteration+1}\t {x_values}\t {objective:.5f}")
        if all(abs(x[i] - x0[i]) < epsilon for i in range(len(x))):
            print("Convergence reached.")
            break

        x0 = x[:]
    print("\n")


def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(cols_A))
    return result


def identity_matrix(size):
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)]


def invert_matrix(matrix):
    n = len(matrix)
    augmented = [row[:] + identity_row for row, identity_row in zip(matrix, identity_matrix(n))]
    for i in range(n):
        if augmented[i][i] == 0:
            raise ValueError("The matrix has no inverse")
        lead = augmented[i][i]
        augmented[i] = [element / lead for element in augmented[i]]
        for j in range(n):
            if i != j:
                ratio = augmented[j][i]
                augmented[j] = [augmented[j][k] - ratio * augmented[i][k] for k in range(2 * n)]
    inverse = [row[n:] for row in augmented]
    return inverse


def matrix_vector_multiply(matrix, vector):
    return [sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(matrix))]


if __name__ == "__main__":
    print('Enter the vector of coefficients of the objective function (C)')
    coefficients = list(map(int, input().split()))
    print('Enter the vector of right-hand sides (b)')
    rightHandNumbers = list(map(int, input().split()))
    print('Enter the matrix of constraint coefficients (A)')
    matrix = []
    for i in range(len(rightHandNumbers)):
        coefficientsOfConstraints = list(map(int, input().split()))
        matrix.append(coefficientsOfConstraints)

    subMatrix = []
    for i in range(len(rightHandNumbers)):
        subArr = [0] * len(rightHandNumbers)
        subArr[i] = 1
        subMatrix.append(subArr)

    arr = []
    for i in range(len(rightHandNumbers)):
        subArr = []
        subArr += matrix[i]
        subArr += subMatrix[i]
        subArr += [rightHandNumbers[i]]
        arr.append(subArr)


    horSize = len(arr[0])
    verSize = len(arr)

    print("Enter the approximation accuracy (e.g. 1e-6)")
    accuracy = float(input())
    print("Enter the x0")
    x0 = list(map(float, input().split(" ")))

    interior_point_method(coefficients, matrix, rightHandNumbers, x0, accuracy, 0.5, 10)