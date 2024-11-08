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
            if x & self.FIELD_SIZE:  # Redukcja, jeśli x przekracza 5 bitów
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
