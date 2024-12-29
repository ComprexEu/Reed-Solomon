from galoisfield import GaloisField
from reedsolomon import ReedSolomon
from gaussjordan import GaussJordan


class Main:
    def __init__(self):
        self.gf = GaloisField()
        self.rs = ReedSolomon(7, 3)

    def main(self):
        print(self.gf.add(1, 0))
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

        #print(self.rs.encode([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]))
        #print(self.rs.simple_decode(
            #[1, 2, 4, 4, 5, 6, 7, 8, 9, 10, 11, 26, 4, 16, 0, 8, 6, float('-inf'), 5, 25, 28, 9, 8, 25, 14, 28, 30, 21,
             #float('-inf'), 6, 30]))
        #print(self.rs.encode_as_evaluations([0, 0, 0, 4, 5, 6, 7, 5, 9, 10, 11]))
        #print(self.rs.berlekamp_welch_decode(
            #[18, 10, 15, 19, 21, 3, 2, 1, 9, 23, 13, 8, 3, 0, 4, 7, 6, 7, 8, 9, 10, 25, 2, 20, 26, 14, 30, 7, 28, 1, 12]))

        print("ENCODED MESSAGE ", self.rs.encode_as_evaluations([1, 2, 3]))
        print(self.rs.berlekamp_welch_decode([6, 5, 5, 6, 1, 2, 2]))


if __name__ == "__main__":
    main = Main()
    main.main()
