from galoisfield import GaloisField


class GaussJordan:

    def __init__(self, leftmatrix, rightmatrix):
        self.leftmatrix = leftmatrix  # macierz równań
        self.n = len(self.leftmatrix)
        self.rightmatrix = rightmatrix  # macierz o wymiarze 1xn, czyli tablica z rozwiązaniami
        self.gf = GaloisField()

    def calculate(self):
        for i in range(self.n):
            # Ensure diagonal element is non-zero by row swapping if needed
            if self.leftmatrix[i][i] == float('inf'):
                swapped = False
                for c in range(i + 1, self.n):
                    if self.leftmatrix[c][i] != float('inf'):
                        # Swap rows in leftmatrix
                        self.leftmatrix[i], self.leftmatrix[c] = self.leftmatrix[c], self.leftmatrix[i]
                        # Swap corresponding values in rightmatrix
                        self.rightmatrix[i], self.rightmatrix[c] = self.rightmatrix[c], self.rightmatrix[i]
                        swapped = True
                        break
                if not swapped:  # No non-zero pivot found
                    raise ValueError(f"Matrix is singular or unsolvable at row {i}")

            # Normalize the pivot row and eliminate the i-th variable from other rows
            for j in range(self.n):
                if i != j:
                    # Scaling factor for elimination
                    p = self.gf.div(self.leftmatrix[j][i], self.leftmatrix[i][i])

                    # Update the left matrix row
                    for k in range(self.n):
                        self.leftmatrix[j][k] = self.gf.add(
                            self.leftmatrix[j][k],
                            self.gf.mul(self.leftmatrix[i][k], p)
                        )

                    # Update the right matrix element
                    self.rightmatrix[j] = self.gf.add(
                        self.rightmatrix[j],
                        self.gf.mul(self.rightmatrix[i], p)
                    )
