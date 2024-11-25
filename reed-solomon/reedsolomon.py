from galoisfield import GaloisField


class ReedSolomon:
    def __init__(self, n, k):
        self.gf = GaloisField()  # instancja klasy GaloisField
        self.n = n  # długość wiadomości
        self.k = k  # liczba bitów informacyjnych
        self.t = (self.n - self.k) // 2  # liczba błędów do korekcji
        self.generator_poly = self.generate_generator_poly()  # wielomian generujący

    def generate_generator_poly(self):
        g = [0]
        for i in range(1, self.n - self.k + 1):
            g = self.gf.poly_multiply(g, [0, i])
        return g

    def encode(self, message):
        info_poly = message + [float('-inf')] * (self.n - self.k)
        control_poly = self.gf.poly_mod(info_poly, self.generator_poly)
        encoded_message = info_poly[:self.k] + control_poly
        return encoded_message

    def decode(self, encoded_message):
        # co robić w przypadku, gdy jest większa liczba błedów w pakiecie, jak złapać taki wyjątek
        iterator = 0
        decoded_message = encoded_message
        while iterator < self.n:

            # tworzenie syndromu
            syndrome = self.gf.poly_mod(decoded_message, self.generator_poly)

            syndrome = [float('-inf')] * (len(encoded_message) - len(syndrome)) + syndrome

            syndrome_weight = 0  # waga syndromu, to ilosc wszystkich nie zerowych elementów w syndromie
            for i in range(0, len(syndrome)):
                if self.gf.exp_to_elem[syndrome[i]] > 0:
                    syndrome_weight += 1

            if self.t >= syndrome_weight > 0:
                for i in range(0, self.n):
                    decoded_message[i] = self.gf.add(syndrome[i], encoded_message[i])

                # przesunięcie cykliczne w lewo do pierwotenj postaci
                for i in range(0, iterator):
                    decoded_message.append(decoded_message[0])
                    decoded_message.pop(0)

                return decoded_message
            elif syndrome_weight == 0:
                return decoded_message

            # przesunięcie cykliczne w prawo - dodanie zer z lewej strony
            decoded_message.insert(0, decoded_message[self.n - 1])
            decoded_message.pop(len(decoded_message) - 1)

            iterator += 1
