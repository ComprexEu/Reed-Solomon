class GaloisField:
    PRIMITIVE_POLY = 0b100101  # Wielomian pierwotny x^5 + x^2 + 1
    FIELD_SIZE = 32  # GF(2^5) - 32 elementy

    def __init__(self):
        # Inicjalizacja słownika mapującego elementy wektorowe i potęgi generatora
        self.field_dict = {}  # Nie przechowujemy elementu zerowego
        self._generate_field_dict()

    def _generate_field_dict(self):
        x = 1
        for i in range(self.FIELD_SIZE - 1):
            self.field_dict[i] = x  # Mapowanie potęgi do elementu wektorowego
            self.field_dict[x] = i  # Mapowanie elementu wektorowego do potęgi
            x <<= 1  # Mnożenie przez 2
            if x & self.FIELD_SIZE:  # Redukcja, jeśli x przekracza 5 bitów
                x ^= self.PRIMITIVE_POLY


gf = GaloisField()
gf.field_dict
