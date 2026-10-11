A = [
    [48, -1, -11, -7, 16],
    [13, 81, -20, 5, -7],
    [5, 6, 52, -3, -11],
    [-1, -19, -13, 45, -4],
    [-8, 4, -3, 4, -50],
]

B = [
    [84],
    [-42],
    [-189],
    [-84],
    [315],
]


class Matrix:
    def __init__(self, num_rows: int, num_columns: int, matrix=None):
        self.rows = num_rows
        self.columns = num_columns
        if matrix is None:
            self.matrix = self.create_zero_matrix()
        else:
            self.matrix = matrix

    def __getitem__(self, key):
        if isinstance(key, int):
            if self.columns == 1:
                return self.matrix[key][0]
            elif self.rows == 1:
                return self.matrix[0][key]
            else:
                return self.matrix[key]

        row, col = key
        return self.matrix[row][col]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if self.columns == 1:
                self.matrix[key][0] = value
            elif self.rows == 1:
                self.matrix[0][key] = value
            else:
                self.matrix[key] = value
        else:
            row, col = key
            self.matrix[row][col] = value

    def __str__(self):
        return "\n".join(" ".join(map(str, row)) for row in self.matrix)

    def create_identity_matrix(self) -> None:
        if self.rows == self.columns:
            for i in range(self.rows):
                self.matrix[i][i] = 1
        else:
            print("Matrix is not square that it is not can be identity matrix")

    def create_zero_matrix(self) -> list[list]:
        return [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    def swap_rows(self, row_1: int, row_2: int) -> None:
        self.matrix[row_1], self.matrix[row_2] = self.matrix[row_2], self.matrix[row_1]

    def __mul__(self, other: Matrix) -> Matrix:
        if self.columns == other.rows:
            new_matrix = Matrix(self.rows, other.columns)
            for i in range(self.rows):
                for j in range(other.columns):
                    for k in range(self.columns):
                        new_matrix[i, j] += self[i, k] * other[k, j]
            return new_matrix
        else:
            raise ValueError("The matrixs cannot be multiplied")


def LUP(U: Matrix, L: Matrix, P: Matrix) -> None:
    # Process each maximum absolute element position step by step
    for i in range(U.rows - 1):
        # Find index of the pivot (maximum absolute element) in column i
        max_element_index = max(range(i, U.rows), key=lambda row: abs(U[row, i]))

        # Swap rows in matrixs U, P and L if pivot is not on the diagonal
        if max_element_index != i:
            U.swap_rows(i, max_element_index)
            P.swap_rows(i, max_element_index)

            # In matrix L swap only parts of rows that playsed below diagonal
            for col in range(i):
                L[i, col], L[max_element_index, col] = (
                    L[max_element_index, col],
                    L[i, col],
                )

        # Compute multipliers for matrix L and zero out elements below the diagonal in U
        for j in range(i + 1, L.rows):
            L[j, i] = U[j, i] / U[i, i]

            for k in range(i, U.columns):
                U[j, k] -= L[j, i] * U[i, k]


def solve_matrix(U: Matrix, L: Matrix, P: Matrix, b: Matrix) -> Matrix:
    n = b.rows
    x = Matrix(n, 1)
    y = Matrix(n, 1)
    b = P * b

    for i in range(n):
        y[i] = b[i] - sum(L[i, j] * y[j] for j in range(i))

    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i, j] * x[j] for j in range(i + 1, n))) / U[i, i]

    return x


def crteate_and_solve_matrix() -> None:
    n_rows = len(A)
    n_columns = len(A[0])
    U = Matrix(n_rows, n_columns, A)

    n_rows = len(B)
    b = Matrix(n_rows, 1, B)
    L = Matrix(n_rows, n_rows)
    P = Matrix(n_rows, n_rows)
    L.create_identity_matrix()
    P.create_identity_matrix()
    print(f"Matrix: U\n{U}\n")
    print(f"Matrix: b\n{b}\n")
    print(f"Matrix: L\n{L}\n")
    print(f"Matrix: P\n{P}\n")
    LUP(U, L, P)
    X = solve_matrix(U, L, P, b)
    for i in range(X.rows):
        print(f"Results x{i + 1}: {X[i]}")


if __name__ == "__main__":
    crteate_and_solve_matrix()
