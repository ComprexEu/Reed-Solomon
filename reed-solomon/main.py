from galoisfield import GaloisField
from reedsolomon import ReedSolomon
from gaussjordan import GaussJordan


class Main:
    def __init__(self):
        self.gf = GaloisField()
        self.rs = ReedSolomon(7, 3)

    def main(self):
        E = self.gf.calculate_poly([0, 4, 3], 6)
        wiE = self.gf.mul(E, 2)
        Q = self.gf.calculate_poly([1, 3, float('-inf'), 4, 6], 6)
        print('E: ', E)
        print('wi * E: ', wiE)
        print('Q: ', Q)
        print(self.gf.add(4, float('-inf')))
        print(self.gf.mul(4, 6))
        print(self.gf.pow(6, 4))
        print(self.gf.mul(2, 5))
        print(self.gf.div(30, 3))
        print(self.gf.calculate_poly([1, 1], 1))

        left_matrix = [
            [0, 0],
            [1, 1]
        ]

        right_matrix = [1, 2]

        gauss_jordan = GaussJordan(left_matrix, right_matrix)
        gauss_jordan.calculate()
        print(right_matrix)

        print("ENCODED MESSAGE ", self.rs.encode_as_evaluations([1, 2, 3]))
        print(self.rs.berlekamp_welch_decode([6, 5, 5, 6, 1, 2, 2]))


if __name__ == "__main__":
    main = Main()
    main.main()
