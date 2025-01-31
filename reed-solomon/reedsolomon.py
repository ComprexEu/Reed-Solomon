from eyed3.utils import formatTime

from galoisfield import GaloisField
from gaussjordan import GaussJordan
#import gaussjordan


class ReedSolomon:
    def __init__(self, n, k):
        self.gf = GaloisField()  # instancja klasy GaloisField
        self.n = n  # długość wiadomości
        self.k = k  # liczba bitów informacyjnych
        self.t = (self.n - self.k) // 2  # maksymalna liczba błędów do korekcji
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

    def simple_decode(self, encoded_message):
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
        return None

    def lagrange_interpolation(self, x_values, y_values, x):

        total = 0 # wielomian końcowy interpolacji
        k = len(x_values)
        for i in range(k):
            # Obliczanie L_i(x)
            term = y_values[i]
            for j in range(k):
                if i != j:
                    #Równanie zapisane poniżej ma taką postać - term *= (x - x_values[j]) / (x_values[i] - x_values[j])
                    term = self.gf.poly_multiply(term, self.gf.poly_div((self.gf.add(x,x_values[j])),self.gf.add(x_values[i],x_values[j])))
            total = self.gf.add(total, term)

        return total


    def encode_as_lagrange_interpolation(self, message):
        k = len(message)  # Liczba symboli w wiadomości
        x_values = list() # Przypisujemy x = [1, 2, 3, ..., k]
        for i in range(k):
            x_values.append(i)
        y_values = message  # Odpowiednie wartości y
        # Wyznaczanie funkcji opisującej zbiór punktów wiadomości
        # Generowanie n punktów kodowych
        encoded_points = [(i, self.lagrange_interpolation(x_values, y_values, i)) for i in range(0, self.n)]

        return encoded_points

    def encode_as_evaluations(self, message):
        encoded = []
        for x in range(self.n):
            encoded.append(self.gf.calculate_poly(message, x))
        return encoded

    def construct_matrices(self, received_message):

        #print("RECEIVED MESSAGE ", received_message)
        left = []
        right = []

        for i in range(self.n):
            ai = i
            wi = received_message[i]

            q = [float('-inf')] * (self.k + self.t)
            e = [float('-inf')] * (self.t + 1)

            for j in range(len(q)):  # współczynniki q
                q[j] = self.gf.pow(ai, len(q) - j - 1)
            for j in range(len(e)):  # współczynniki e
                e[j] = self.gf.pow(ai, len(e) - j - 1)
                e[j] = self.gf.mul(e[j], wi)
            r = e[0]
            e.pop(0)

            left.append(q + e)
            right.append(r)

        return left, right

    def solve_linear_system(self, left, right):
        rightmatrix = GaussJordan.calculate(left, right)
        Q = rightmatrix[:self.k + self.t]
        E = rightmatrix[self.k + self.t:]
        return Q, E

    def berlekamp_welch_decode(self, received_message):

        try:
            left, right = self.construct_matrices(received_message)
            Q, E = self.solve_linear_system(left, right)
        except ValueError:
            print("Decoding failed: Too many errors to correct")
            return None  # or raise an exception if needed

        E.insert(0, 0)

        message_polynomial = self.gf.poly_div(Q, E)

        decoded_message = []
        error_count = 0

        for i in range(self.n):
            decoded_message.append(self.gf.calculate_poly(message_polynomial, i))
            if decoded_message[i] != received_message[i]:
                error_count += 1

        return decoded_message if error_count <= 10 else None