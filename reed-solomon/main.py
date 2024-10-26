from galoisfield import GaloisField


class Main:
    def __init__(self):
        self.gf = GaloisField()

    def main(self):
        # Przykładowe elementy do dodawania i mnożenia
        a = 30
        b = 10

        sum_result = self.gf.add(a, b)
        print(sum_result)
        mul_result = self.gf.mul(a, b)
        print(mul_result)


if __name__ == "__main__":
    main = Main()
    main.main()
