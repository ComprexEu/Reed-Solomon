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
                # Jeśli znaleziono jakiś niezerowy element, zakończ algorytm
                if (i + c) == n:
                    if rightmatrix[i] != float('-inf'):
                        raise ValueError("Linear system is unsolvable")
                    continue

                # Zamiana wierszy w macierzy
                leftmatrix[i], leftmatrix[i+c] = leftmatrix[i+c], leftmatrix[i]
                rightmatrix[i], rightmatrix[i+c] = rightmatrix[i+c], rightmatrix[i]

            # Normalizacja wiersza obrotu
            pivot = leftmatrix[i][i]
            if pivot != float('-inf'):
                for k in range(n):
                    leftmatrix[i][k] = gf.div(leftmatrix[i][k], pivot)
                rightmatrix[i] = gf.div(rightmatrix[i], pivot)

            for j in range(n):
                if i != j:
                    # Wyliczenie wartości wektora skalującego
                    p = gf.div(leftmatrix[j][i], leftmatrix[i][i])

                    # Eliminacja columny
                    for k in range(n):
                        leftmatrix[j][k] = gf.add(leftmatrix[j][k], gf.mul(leftmatrix[i][k], p))

                    rightmatrix[j] = gf.add(rightmatrix[j], gf.mul(rightmatrix[i], p))

        return rightmatrix