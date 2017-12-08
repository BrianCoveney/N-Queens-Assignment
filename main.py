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


def steepestHill(board):
    moves = {}
    for col in range(len(board)):
        for row in range(len(board)):
            board_copy = list(board)
            board_copy[col] = row
            moves[(col, row)] = getHeuristic(board_copy)

    best_moves = []
    initial_heuristic = getHeuristic(board)



    for k, v in moves.items():
        if v < initial_heuristic:
            initial_heuristic = v

    for k, v in moves.items():
        if v == initial_heuristic:
            best_moves.append(k)



    # Pick a random best move
    if len(best_moves) > 0:
        pick = random.randint(0, len(best_moves) -1)
        col = best_moves[pick][0]
        row = best_moves[pick][1]
        board[col] = row


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
    print("Random Initial State:", random_initial_board)
    print("Heuristic Value:", getHeuristic(random_initial_board))


    # Move one queen and get heuristic
    move_one = moveOneQueen(random_initial_board)
    print("\nMoving one position: ", move_one)
    move_one_heu = getHeuristic(move_one)
    print("Heuristic Value:", move_one_heu)

    # Steepest hill climbing
    steepest_hill = steepestHill(random_initial_board)
    print("\nSteepest hill:       ", steepest_hill)
    steepest_hill_heu = getHeuristic(steepest_hill)
    print("Heuristic Value:", steepest_hill_heu)

    # Random restart hill climbing
    best_conf = None
    new_random = getRandomNumbers(N)
    new_steepest_hill = steepestHill(new_random)
    print("\nNew Steepest hill:   ", new_steepest_hill)
    new_steepest_hill_heu = getHeuristic(new_steepest_hill)
    print("Heuristic Value:", new_steepest_hill_heu)

    print("")
    if new_steepest_hill_heu < steepest_hill_heu:
        print("New solution better  ", steepest_hill)
    else:
        print("Old solution better  ", new_steepest_hill)


if __name__ == '__main__':
    main()
