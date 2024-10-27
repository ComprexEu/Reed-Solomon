from galoisfield import GaloisField


class Main:
    def __init__(self):
        self.gf = GaloisField()

    def main(self):
        # Przykładowe elementy do dodawania i mnożenia
        a = 1
        b = 2
        p = [0, 1]
        q = [0, 2]
        r = [0, 3]

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


if __name__ == "__main__":
    main = Main()
    main.main()
