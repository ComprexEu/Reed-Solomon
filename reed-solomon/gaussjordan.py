from galoisfield import GaloisField


class GaussJordan:

    def __init__(self, leftmatrix, rightmatrix):
        self.leftmatrix = leftmatrix  # Matrix of equations
        self.n = len(self.leftmatrix)
        self.rightmatrix = rightmatrix  # Solution matrix (1 x n)
        self.gf = GaloisField()

    def calculate(self):

        for i in range(self.n):
            if self.leftmatrix[i][i] == float('-inf'):
                c = 1
                while (i + c) < self.n and self.leftmatrix[i + c][i] == float('-inf'):
                    c += 1
                # If no non-zero element is found, end the algorithm
                if (i + c) == self.n:
                    break

                # Swap rows in the matrix
                self.leftmatrix[i], self.leftmatrix[i+c] = self.leftmatrix[i+c], self.leftmatrix[i]
                self.rightmatrix[i], self.rightmatrix[i+c] = self.rightmatrix[i+c], self.rightmatrix[i]

            # Normalize pivot row
            pivot = self.leftmatrix[i][i]
            if pivot != float('-inf'):
                for k in range(self.n):
                    self.leftmatrix[i][k] = self.gf.div(self.leftmatrix[i][k], pivot)
                self.rightmatrix[i] = self.gf.div(self.rightmatrix[i], pivot)

            for j in range(self.n):
                if i != j:
                    # Calculate scaling factor
                    p = self.gf.div(self.leftmatrix[j][i], self.leftmatrix[i][i])

                    # Eliminate column entries
                    for k in range(self.n):
                        self.leftmatrix[j][k] = self.gf.add(self.leftmatrix[j][k], self.gf.mul(self.leftmatrix[i][k], p))

                    # Update right matrix
                    self.rightmatrix[j] = self.gf.add(self.rightmatrix[j], self.gf.mul(self.rightmatrix[i], p))

