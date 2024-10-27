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

    def add(self, a, b):
        return a ^ b

    def mul(self, a, b):
        if a == 0 or b == 0:
            return 0
        # α^x * α^y = α^((x + y) mod (2^5 - 1))
        exp_sum = (self.elem_to_exp[a] + self.elem_to_exp[b]) % (self.FIELD_SIZE - 1)
        return self.exp_to_elem[exp_sum]

    def poly_multiply(self, p, q):
        result = [0] * (len(p) + len(q) - 1)

        for i in range(len(p)):
            for j in range(len(q)):
                result[i + j] ^= self.mul(self.exp_to_elem[p[i]], self.exp_to_elem[q[j]])

        for i in range(len(result)):
            result[i] = self.elem_to_exp[result[i]]

        return result

    def poly_mod(self, p, q):
        q_deg = len(q)
        r = p[:]
        while (len(r) >= q_deg) != 0:
            added_value = self.add(self.exp_to_elem[r[0]], self.exp_to_elem[q[0]])

            if added_value != 0:
                factor = self.elem_to_exp[added_value]
            else:
                factor = 1

            for i in range(q_deg):
                term = self.mul(factor, q[i])
                added_value = self.add(self.exp_to_elem[r[i]], self.exp_to_elem[term])

                if added_value != 0:
                    r[i] = self.elem_to_exp[added_value]
                else:
                    r[i] = 0
                #r = self.elem_to_exp[self.add(self.exp_to_elem[r[i]], self.exp_to_elem[term])]

            r.pop(0)
        return r
