from galoisfield import GaloisField

class GaussJordan:

    @staticmethod
    def calculate(leftmatrix, rightmatrix):

        n = len(leftmatrix)
        gf = GaloisField()

        for i in range(n):
            if leftmatrix[i][i] == float('-inf'):
                c = 1
                while (i + c) < n and leftmatrix[i + c][i] == float('-inf'):
                    c += 1
                # If no non-zero element is found, end the algorithm
                if (i + c) == n:
                    raise ValueError("Linear system is unsolvable")

                # Swap rows in the matrix
                leftmatrix[i], leftmatrix[i+c] = leftmatrix[i+c], leftmatrix[i]
                rightmatrix[i], rightmatrix[i+c] = rightmatrix[i+c], rightmatrix[i]

            # Normalize pivot row
            pivot = leftmatrix[i][i]
            if pivot != float('-inf'):
                for k in range(n):
                    leftmatrix[i][k] = gf.div(leftmatrix[i][k], pivot)
                rightmatrix[i] = gf.div(rightmatrix[i], pivot)

            for j in range(n):
                if i != j:
                    # Calculate scaling factor
                    p = gf.div(leftmatrix[j][i], leftmatrix[i][i])

                    # Eliminate column entries
                    for k in range(n):
                        leftmatrix[j][k] = gf.add(leftmatrix[j][k], gf.mul(leftmatrix[i][k], p))

                    # Update right matrix
                    rightmatrix[j] = gf.add(rightmatrix[j], gf.mul(rightmatrix[i], p))
        print("SOLVED LEFT MATRIX", leftmatrix)
        print("SOLVED RIGHT MATRIX", rightmatrix)

        return rightmatrix