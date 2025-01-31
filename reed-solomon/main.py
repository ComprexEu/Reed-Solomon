from galoisfield import GaloisField
from reedsolomon import ReedSolomon

class Main:

    def __init__(self):
        self.gf = GaloisField()
        self.rs = ReedSolomon(31, 11)

    def main(self):

        # print("Encoded message: ", self.rs.encode_as_lagrange_interpolation([1,2,3,4,5,6,7,8,9,10,11,12]))

        print(self.rs.encode([1,2,3,4,5,6,7,8,9,10,11]))

        #print(self.rs.encode_as_evaluations([1,2,3,4,5,6,7,8,9,10,11]))
        #print(self.rs.berlekamp_welch_decode([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 2, 15, 23, 28, 15, 19, 12, 6, 29, 16, 24, 17, 23, 3, 20, 30, 18, 6, 28]))

        print(self.rs.berlekamp_welch_decode([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 26, 4, 16, 0, 8, 6, 1, 5, 24, 28, 9, 8, 25, 14, 28, 30, 21, 1, 6, 30]))
if __name__ == "__main__":
    main = Main()
    main.main()
