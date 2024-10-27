from galoisfield import GaloisField

class ReedSolomon:
    def __init__(self, t, n, k):
        self.t = t  # liczba błędów do korekcji
        self.gf = GaloisField()  # instancja klasy GaloisField
        self.n = n # Długość wiadomości
        self.k = k # ilość bitów informacyjnych
        self.generator_poly = self.generate_generator_poly()

    def generate_generator_poly(self):
        g = [0]
        for i in range(1, 2 * self.t + 1):
            g = self.gf.poly_multiply(g, [0, i])
        return g

    def encode(self, message):
        info_poly = message + [0] * (self.n - self.k)
        r = info_poly % self.generator_poly

        return info_poly
