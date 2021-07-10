import sys


if __name__ == "__main__":
    number_of_stairs = int(sys.argv[1])
    number_of_grids = 1
    number_of_spaces = number_of_stairs - number_of_grids
    for _ in range(number_of_stairs):
        print(" " * number_of_spaces + "#" * number_of_grids)
        number_of_grids += 1
        number_of_spaces -= 1
