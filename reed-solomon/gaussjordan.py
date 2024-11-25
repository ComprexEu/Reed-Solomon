from galoisfield import GaloisField


class GaussJordan:

    def __init__(self, leftmatrix, rightmatrix):
        self.leftmatrix = leftmatrix  # macierz równań
        self.n = len(self.leftmatrix)
        self.rightmatrix = rightmatrix  # macierz o wymiarze 1xn, czyli tablica z rozwiązaniami
        self.gf = GaloisField()

    def calculate(self):

        for i in range(self.n):
            if self.leftmatrix[i][i] == 0:

                c = 1
                while (i + c) < self.n and self.leftmatrix[i + c][i] == 0:
                    c += 1
                # warunek w przypadku, gdy wszystkie wartości w jednym wierszu są już zerami - koniec algorytmu
                if (i + c) == self.n:
                    break

                # zamiana dwóch wierszy ze sobą w macierzy rozwiązań
                for k in range(1 + self.n):
                    tmp = self.leftmatrix[i][k]
                    self.leftmatrix[i][k] = self.leftmatrix[i+c][k]
                    self.leftmatrix[i+c][k] = tmp
                # zamiana wierszy w macierzy z rozwiązaniami
                tmp = self.rightmatrix[i]
                self.rightmatrix[i] = self.rightmatrix[i+c]
                self.rightmatrix[i+c] = tmp
            for j in range(self.n):

                if i != j:
                    # znalezienie wartości skalującej
                    p = self.gf.div(self.leftmatrix[i][j], self.leftmatrix[i][i])

                    for k in range(1 + self.n):  # operacja odejmowania w ciele GF(2^m)# jest tożsama z operacją dodawania
                        self.leftmatrix[j][k] = self.gf.add(self.leftmatrix[j][k], (self.gf.mul(self.leftmatrix[i][k], p)))

                    self.rightmatrix[j] = self.gf.add(self.rightmatrix[j], (self.gf.mul(self.rightmatrix[i], p)))

