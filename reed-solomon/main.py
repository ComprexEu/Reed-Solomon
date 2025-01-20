from galoisfield import GaloisField
from reedsolomon import ReedSolomon

class Main:

    def __init__(self):
        self.gf = GaloisField()
        self.rs = ReedSolomon(31, 11)

    def main(self):

        print("Encoded message: ", self.rs.encode_as_evaluations([2,1,3,7, 4, 5, 6, 7, 8, 9, 10]))
        print(self.rs.berlekamp_welch_decode([26, 7, 4, 6, 11, 25, 17, 24, float('-inf'), 2, 2, 2, 2, 2, 2, 24, 22, 7, 24, 24, 10, 29, 16, 21, 26, 3, 25, 19, 2, 9, 13]))


if __name__ == "__main__":
    main = Main()
    main.main()
