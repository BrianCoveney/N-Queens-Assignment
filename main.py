import random
import math

global N
N = 8


# ------------------------------------------
# Return the heuristic value of our initial board state
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
# Move One Queen Algorithm
# ------------------------------------------
def moveOneQueen(board):
    initial_heuristic = getHeuristic(board)
    for col in range(len(board)):
        for row in range(len(board)):
            board_copy = list(board)
            # Move queen
            board_copy[row], board_copy[col] = board_copy[col], board_copy[row]
            new_heuristic = getHeuristic(board_copy)

            # Return the first better match
            if new_heuristic < initial_heuristic:
                board[col] = board[row]
                return board

    return board


# ------------------------------------------
# Steepest Hill Algorithm
# ------------------------------------------
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
# Random Restart Algorithm
# ------------------------------------------
def randomRestartHillClimb(old_steepest_hill, old_steepest_hill_heu):
    restarts = 500
    restart_count = 0
    count_new_solution = 0
    count_old_solution = 0
    best_solution = []

    # Initially set the maximum number of restarts to 500
    while restart_count < restarts:
        # Generate a new random configuration for the initial state of the board
        new_random = getRandomNumbers(N)
        new_steepest_hill = steepestHill(new_random)
        new_steepest_hill_heu = getHeuristic(new_steepest_hill)
        print("")

        # A solution was found for our new random state. Print details and exit.
        if new_steepest_hill_heu == 0:
            print("Correct Answer found in New Steepest Hill count: ",count_new_solution,"\n", new_steepest_hill,sep="")
            best_solution = new_steepest_hill
            return best_solution

        # A solution was found for out steepest ascent algorithm. Print details and exit.
        elif old_steepest_hill_heu == 0:
            print("Correct Answer found in Old Steepest Hill count: ",count_old_solution,"\n",old_steepest_hill,sep="")
            best_solution = old_steepest_hill
            return best_solution

        # Otherwise, display which is the better algorithm
        else:
            if new_steepest_hill_heu < old_steepest_hill_heu:
                print("Count New:",count_new_solution)
                print("New solution better  ", old_steepest_hill)
                print("Heuristic Value:", new_steepest_hill_heu)
                count_new_solution = count_new_solution + 1
            else:
                print("Count Old:", count_old_solution)
                print("Old solution better  ", new_steepest_hill)
                print("Heuristic Value:", old_steepest_hill_heu)
                count_old_solution = count_old_solution + 1

        restart_count = restart_count + 1

        # Display total number of moves
        total_number_of_moves = count_old_solution + count_new_solution
        print("\nTotal number of moves:", total_number_of_moves)



    return best_solution


def annealing(board):
    temp = len(board) ** 2
    anneal_rate = 0.95
    heu_cost = getHeuristic(board)

    while heu_cost > 0:
        board = makeMove(board, heu_cost, temp)
        heu_cost = getHeuristic(board)
        # Make sure temp doesn't get impossibly low
        new_temp = max(temp * anneal_rate, 0.01)
        temp = new_temp
        if temp >= 50000:
            break

    return board


def makeMove(board, heu_cost, temp):
    board_copy = list(board)
    found_move = False

    while not found_move:
        board_copy = list(board)
        new_row = random.randint(0, len(board) - 1)
        new_col = random.randint(0, len(board) - 1)
        board_copy[new_col] = new_row
        new_h_cost = getHeuristic(board_copy)
        if new_h_cost < heu_cost:
            found_move = True
        else:
            # How bad was the choice?
            delta_e = heu_cost - new_h_cost
            # Probability can never exceed 1
            accept_probability = min(1, math.exp(delta_e / temp))
            found_move = random.random() <= accept_probability

    return board_copy


# ------------------------------------------
# Return a list of random numbers
# ------------------------------------------
def getRandomNumbers(num_queens):
    numbers = []
    for n in range(num_queens):
        numbers.append(n)
    random.shuffle(numbers)

    return numbers


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
    # Random Initial State
    random_initial_board = getRandomNumbers(N)
    displayBoard(random_initial_board)
    print("Random Initial State:", random_initial_board)
    print("Heuristic Value:", getHeuristic(random_initial_board))

    print("------------------------------------------")

    # Move One Queen
    move_one = moveOneQueen(random_initial_board)
    print("\nMoving one position: ", move_one)
    move_one_heu = getHeuristic(move_one)
    print("Heuristic Value:", move_one_heu)

    print("------------------------------------------")

    # Steepest Hill Climbing
    steepest_hill = steepestHill(random_initial_board)
    print("\nSteepest hill:       ", steepest_hill)
    steepest_hill_heu = getHeuristic(steepest_hill)
    print("Heuristic Value:", steepest_hill_heu)

    print("------------------------------------------")

    # Random Restart Hill Climbing
    solution = randomRestartHillClimb(steepest_hill, steepest_hill_heu)
    displayBoard(solution)

    # Simulated Annealing
    print("\nCorrect Answer found in Simulated Annealing")
    simulated_annealing = annealing(random_initial_board)
    print(simulated_annealing)
    displayBoard(simulated_annealing)

if __name__ == '__main__':
    main()
