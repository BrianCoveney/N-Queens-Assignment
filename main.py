import random

global N
N = 8


# ------------------------------------------
# Returns the heuristic value of our initial board state
# ------------------------------------------
def getHeuristic(board):
    heuristic = 0
    for row in range(len(board)):

        for col in range(row + 1, len(board)):

            if board[row] == board[col]:
                heuristic += 1

            offset = col - row

            if board[row] == board[col] - offset or board[row] == board[col] + offset:
                heuristic += 1

    return heuristic


# ------------------------------------------
# Return as list of random numbers
# ------------------------------------------
def getRandomNumbers(num_queens):
    numbers = []
    for n in range(num_queens):
        numbers.append(n)
    random.shuffle(numbers)

    return numbers


def moveOneQueen(board):
    initial_heuristic = getHeuristic(board)
    for col in range(len(board)):
        for row in range(len(board)):
            board_copy = list(board)
            # Move queen
            board_copy[row], board_copy[col] = board_copy[col], board_copy[row]
            new_heuristic = getHeuristic(board_copy)

            # Return the first better (not best!) match you find
            if new_heuristic < initial_heuristic:
                board[col] = board[row]
                return board

    return board


# ------------------------------------------
# Prints the chess board with:
#  - positions of 'Q's retrieved from the index of our random number list
#  - otherwise positions are left blank
# ------------------------------------------
def displayBoard(board):
    for row in range(len(board)):
        print("", end="|")

        queen = board.index(row)

        for col in range(len(board)):
            if col == queen:
                print("Q", end="|")
            else:
                print("_", end="|")
        print("")


def main():

    # Generate a random initial state, display board and get heuristic
    random_initial_board = getRandomNumbers(N)
    displayBoard(random_initial_board)
    heuristic = getHeuristic(random_initial_board)
    print("Heuristic Value:", heuristic)
    print("Random Initial State:", random_initial_board)

    # Move one queen and get heuristic
    move_one = moveOneQueen(random_initial_board)
    print("\nMoving one position: ", move_one)
    move_one_heuristic = getHeuristic(move_one)
    print("Heuristic Value:", move_one_heuristic)




if __name__ == '__main__':
    main()
