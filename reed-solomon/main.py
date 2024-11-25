from galoisfield import GaloisField
from reedsolomon import ReedSolomon


class Main:
    def __init__(self):
        self.gf = GaloisField()
        self.rs = ReedSolomon(31, 11)

    def main(self):
        print(self.rs.encode([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]))
        print(self.rs.decode(
            [1, 2, 4, 4, 5, 5, 7, 8, 6, 6, 11, 16, 4, 16, 0, 8, 6, float('-inf'), 5, 25, 28, 9, 8, 25, 14, 28, 30, 21,
             float('-inf'), 6, 30]))
        print(len([1, 2, 4, 4, 5, 6, 7, 8, 9, 10, 11, 26, 4, 16, 0, 8, 6, float('-inf'), 5, 25, 28, 9, 8, 25, 14, 28,
                   30, 21, float('-inf'), 6, 30]))
        print(self.gf.pow(2, 2))


if __name__ == "__main__":
    main = Main()
    main.main()
