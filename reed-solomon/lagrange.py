from galoisfield import GaloisField


class LagrangeInterpolation:
    def __init__(self, gf):
        self.gf = gf

    def interpolate(self, x_values, y_values):
        assert len(x_values) == len(y_values), "Liczba wartości x musi być równa liczbie wartości y"
        n = len(x_values)
        polynomial = [float('-inf')]  # Początkowy wielomian to 0

        for i in range(n):
            numerator = [float('-inf')]
            denominator = float('-inf')

            for j in range(n):
                if i != j:
                    numerator = self.gf.poly_multiply(numerator, [self.gf.add(x_values[j], float('-inf')), 0])
                    denominator = self.gf.add(denominator, self.gf.mul(x_values[i], x_values[j]))

            denominator_inv = self.gf.div(0, denominator)  # Odwrotność elementu
            term = [self.gf.mul(y_values[i], denominator_inv)]
            term.extend(numerator)

            while len(polynomial) < len(term):
                polynomial.insert(0, float('-inf'))

            for k in range(len(term)):
                polynomial[-(k + 1)] = self.gf.add(polynomial[-(k + 1)], term[-(k + 1)])

        return polynomial


gf = GaloisField()
lagrange = LagrangeInterpolation(gf)
x_vals = [0, 1, 2]  # Elementy w postaci alfa
y_vals = [4, 5, 6]  # Wartości funkcji w tych punktach
polynomial = lagrange.interpolate(x_vals, y_vals)
print(gf.calculate_poly(polynomial,0))
print("Interpolowany wielomian:", polynomial)

