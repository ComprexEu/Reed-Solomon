class GaloisField:
    PRIMITIVE_POLY = 0b100101  # Wielomian pierwotny x^5 + x^2 + 1
    FIELD_SIZE = 32  # GF(2^5) - 32 elementy

    def __init__(self):
        # Inicjalizacja słowników mapujących elementy wektorowe i potęgi generatora
        self.exp_to_elem = {}
        self.elem_to_exp = {}
        self._generate_field_dict()

    def _generate_field_dict(self):
        x = 1
        for i in range(self.FIELD_SIZE - 1):
            self.exp_to_elem[i] = x  # Mapowanie potęgi do elementu wektorowego
            self.elem_to_exp[x] = i  # Mapowanie elementu wektorowego do potęgi
            x <<= 1  # Mnożenie przez 2
            if x >= self.FIELD_SIZE:  # Redukcja, jeśli x przekracza 5 bitów
                x ^= self.PRIMITIVE_POLY
        self.exp_to_elem[float('-inf')] = 0
        self.elem_to_exp[0] = float('-inf')

    def add(self, a, b):
        return self.elem_to_exp[self.exp_to_elem[a] ^ self.exp_to_elem[b]]

    def mul(self, a, b):
        if a == float('-inf') or b == float('-inf'):
            return float('-inf')
        return (a + b) % (self.FIELD_SIZE - 1)

    def div(self, a, b):
        if a == float('-inf'):
            return float('-inf')
        if b == float('-inf'):
            raise ZeroDivisionError
        return (a - b) % (self.FIELD_SIZE - 1)

    def pow(self, a, n):
        if n == 0:
            return 0
        b = a
        for i in range(n - 1):
            a = self.mul(a, b)
        return a

    def poly_multiply(self, p, q):
        result = [0] * (len(p) + len(q) - 1)

        for i in range(len(p)):
            for j in range(len(q)):
                result[i + j] ^= self.exp_to_elem[self.mul(p[i], q[j])]

        for i in range(len(result)):
            result[i] = self.elem_to_exp[result[i]]
        return result

    def poly_mod(self, p, q):
        q_deg = len(q)
        r = p[:]
        while len(r) >= q_deg:
            factor = self.div(r[0], q[0])

            for i in range(q_deg):
                term = self.mul(factor, q[i])
                r[i] = self.add(r[i], term)

            r.pop(0)
        return r

    def poly_div(self, p, q):
        q_deg = len(q)
        r = p[:]
        result = []
        while len(r) >= q_deg:
            factor = self.div(r[0], q[0])

            for i in range(q_deg):
                term = self.mul(factor, q[i])
                r[i] = self.add(r[i], term)

            r.pop(0)
            result.append(factor)
        return result

    def calculate_poly(self, p, x):
        p_deg = len(p) - 1
        result = float('-inf')
        for i in range(p_deg + 1):  # pi * x^i
            result = self.add(result, self.mul(p[i], self.pow(x, p_deg - i)))
        return result

    def lagrange_interpolation(self, points):
        """
        Perform Lagrange interpolation in GF(2^5).
        points: List of tuples (x, y), where x and y are powers of alpha.
        Returns the coefficients of the interpolated polynomial.
        """
        n = len(points)
        coefficients = [float('-inf')] * n  # Initialize coefficients to 0 (in exponent domain)

        for i in range(n):
            xi, yi = points[i]
            term = [0]  # Start with 1 (x^0), represented as 0 in exponent domain

            for j in range(n):
                if j != i:
                    xj, _ = points[j]
                    # Compute (x - xj) / (xi - xj)
                    # (x - xj) is represented as [xj, 1] in polynomial form
                    # (xi - xj) is the denominator
                    denominator = self.add(xi, xj)  # xi - xj
                    if denominator == float('-inf'):
                        raise ValueError("Duplicate points or invalid interpolation.")
                    inv_denominator = self.exp_to_elem[self.div(0, self.elem_to_exp[denominator])]
                    term = self.poly_multiply(term, [xj, 0])  # Multiply by (x - xj)
                    term = [self.mul(coeff, inv_denominator) for coeff in term]

            # Multiply term by yi and add to coefficients
            term = [self.mul(coeff, yi) for coeff in term]
            coefficients = [self.add(c, t) for c, t in zip(coefficients, term)]

        return coefficients

    def encode_message(self, message, codeword_length):
        """
        Encode a message using polynomial interpolation.
        message: List of powers of alpha.
        codeword_length: Desired length of the codeword.
        """
        # Convert message to points (x, y), where x is the index and y is the message value
        points = [(i, message[i]) for i in range(len(message))]

        # Perform Lagrange interpolation to find the polynomial
        coefficients = self.lagrange_interpolation(points)

        # Evaluate the polynomial at higher powers of alpha
        codeword = message.copy()
        for i in range(len(message), codeword_length):
            x = i
            y = self.calculate_poly(coefficients, x)
            codeword.append(y)

        return codeword
