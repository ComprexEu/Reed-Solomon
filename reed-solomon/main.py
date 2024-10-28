from pyexpat.errors import messages

from galoisfield import GaloisField
from reedsolomon import ReedSolomon


class Main:
    def __init__(self):
        self.gf = GaloisField()
        self.rs = ReedSolomon(1,7,4)

    def main(self):
        # Przykładowe elementy do dodawania i mnożenia
        a = 1
        b = 2
        p = [0, 1]
        q = [0, 2]
        r = [0, 3]
        message = [0,1,0,1]
        sum_result = self.gf.add(a, b)
        print(sum_result)
        mul_result = self.gf.mul(a, b)
        print(mul_result)
        result = self.gf.poly_multiply(p, q)
        print(result)
        result2 = self.gf.poly_multiply(result, r)
        print(result2)
        for i in range(len(result2)):
            print(self.gf.exp_to_elem[result2[i]])

        print(self.gf.poly_mod([0, 1, 0, 1, float('-inf'), float('-inf'), float('-inf')], [0, 6, 1, 6]))
        print(self.rs.generator_poly)
        print(self.rs.encode([0, 1, 0, 1]))
        print(self.rs.decode([0, 1, 0, 1, 0, 4, 5]))


if __name__ == "__main__":
    main = Main()
    main.main()
