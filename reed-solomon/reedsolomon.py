from galoisfield import GaloisField


class ReedSolomon:
    def __init__(self, t):
        self.t = t  # liczba błędów do korekcji
        self.gf = GaloisField()  # instancja klasy GaloisField

    def generate_generator_poly(self):
        g = [0]
        for i in range(1, 2 * self.t + 1):
            g = self.gf.poly_multiply(g, [0, i])
        return g
