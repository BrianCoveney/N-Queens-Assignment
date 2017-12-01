import random

# ------------------------------------------
# Global Variables
# ------------------------------------------
board_size = 8
num_queens = 8


def get_h_cost(board):
    h = 0
    for i in range(len(board)):
        # Check every column we haven't already checked
        for j in range(i + 1, len(board)):
            # Queens are in the same row
            if board[i] == board[j]:
                h += 1
            # Get the difference between the current column
            # and the check column
            offset = j - i
            # To be a diagonal, the check column value has to be
            # equal to the current column value +/- the offset
            if board[i] == board[j] - offset or board[i] == board[j] + offset:
                h += 1

    return h


def generateRandomNumbers():
    numbers = []
    for n in range(num_queens):
        numbers.append(n)
    random.shuffle(numbers)
    return numbers


def displayBoard():
    for row in range(board_size):
        print("", end="|")

        queen = generateRandomNumbers().index(row)

        for col in range(board_size):
            if col == queen:
                print("Q", end="|")
            else:
                print("_", end="|")
        print("")


def main():

    # a predetermined layout
    # queens = list(range(board_size))

    board = generateRandomNumbers()

    heu = get_h_cost(board)
    print(heu)

    displayBoard()
    print(board)


if __name__ == '__main__':
    main()
