import sys


if __name__ == "__main__":
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])

    Discriminant = b * b - 4 * a * c
    x1 = (-b - Discriminant**0.5) / (2 * a)
    x2 = (-b + Discriminant**0.5) / (2 * a)
    print(int(x1))
    print(int(x2))
