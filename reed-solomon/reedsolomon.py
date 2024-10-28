from galoisfield import GaloisField


class ReedSolomon:
    def __init__(self, t, n, k):
        self.t = t  # liczba błędów do korekcji
        self.gf = GaloisField()  # instancja klasy GaloisField
        self.n = n  # długość wiadomości
        self.k = k  # liczba bitów informacyjnych
        self.generator_poly = self.generate_generator_poly()  # wielomian generujący

    def generate_generator_poly(self):
        g = [0]
        for i in range(1, self.n - self.k + 1):
            g = self.gf.poly_multiply(g, [0, i])
        return g

    def encode(self, message):
        info_poly = message + [float('-inf')] * (self.n - self.k)
        control_poly = self.gf.poly_mod(info_poly, self.generator_poly)

        encoded_message = info_poly
        for i in range(0, len(control_poly)):
            encoded_message[len(info_poly) - len(control_poly) + i] = control_poly[i]
        return encoded_message

    def decode(self, encoded_message):
        syndrom = self.gf.poly_mod(encoded_message, self.generator_poly)
        syndrom = [float('-inf')] * (len(encoded_message) - len(syndrom)) + syndrom
        decoded_message = encoded_message
        # co robić w przypadku, gdy jest większa liczba błedów w pakiecie, jak złapać taki wyjątek
        syndrom_weight = 0

        for i in range(0, len(syndrom)):
            if self.gf.exp_to_elem[syndrom[i]] > 0:
                syndrom_weight += 1

        if self.t >= syndrom_weight > 0:
            for i in range(0, self.n):
                decoded_message[i] = self.gf.elem_to_exp[self.gf.add(self.gf.exp_to_elem[syndrom[i]],
                                                                     self.gf.exp_to_elem[encoded_message[i]])]
            return decoded_message
        elif syndrom_weight == 0:
            return decoded_message
