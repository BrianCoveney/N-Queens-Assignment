import random
import math
import time
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


# Parametrised number of Queens
global N
N = 8


# ------------------------------------------
# Heuristic
# Return the heuristic value of our initial board state
# :param board: board configuration
# :return: heuristic cost
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
# :param board: random board configuration
# :return: solution configuration found
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
# :param board: random board configuration
# :return: solution configuration found
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
# :param old_steepest_hill: List returned from the steepestHill() algorithm
# :param old_steepest_hill_heu: Heuristic for the old_steepest_hill
# :return: solution configuration found and a running count
# ------------------------------------------
def randomRestartHillClimb(old_steepest_hill, old_steepest_hill_heu):
    restarts = 500
    restart_count = 0
    count_new_solution = 0
    count_old_solution = 0
    best_solution = []

    # Initially set the maximum number of restarts to 500
    while restart_count < restarts:
        # Generate a new random configuration for the initial state of the board, and get it's heuristic
        new_random = getRandomNumbers(N)
        new_random_steepest_hill = steepestHill(new_random)
        new_steepest_hill_heu = getHeuristic(new_random_steepest_hill)

        # A solution was found for our new random state. Print details and exit.
        if new_steepest_hill_heu == 0:
            best_solution = new_random_steepest_hill
            return best_solution, count_new_solution

        # A solution was found for our steepest ascent algorithm. Print details and exit.
        elif old_steepest_hill_heu == 0:
            best_solution = old_steepest_hill
            return best_solution, count_old_solution

        # Otherwise, display which is the better algorithm
        else:
            if new_steepest_hill_heu < old_steepest_hill_heu:
                count_new_solution = count_new_solution + 1
            else:
                count_old_solution = count_old_solution + 1

        restart_count = restart_count + 1

    return best_solution, restart_count


# ------------------------------------------
# Simulated Annealing Algorithm
# :param board: random board configuration
# :return: solution configuration found and a running count
# ------------------------------------------
def annealing(board):
    temp = len(board) ** 2
    anneal_rate = 0.95
    heu_cost = getHeuristic(board)
    count = 0

    while heu_cost > 0:
        count = count + 1
        board = makeMove(board, heu_cost, temp)
        heu_cost = getHeuristic(board)
        # Make sure temp doesn't get impossibly low
        new_temp = max(temp * anneal_rate, 0.01)
        temp = new_temp
        if temp >= 50000:
            break

    return board, count


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

# end Simulated Annealing Algorithm


# ------------------------------------------
# Evaluation
# :param heu_rrhc: heuristics for RR-HC
# :param heu_annealing: heuristics for RR-SA
# :param steepest_hill: List returned from the steepestHill() algorithm
# :param steepest_hill_heu: Heuristic for the old_steepest_hill
# :return: Lists of the number moves taken to reach a solution for RR-HC and RR-SA
# ------------------------------------------
def evaluation(heu_rrhc, heu_annealing, steepest_hill, steepest_hill_heu):
    # Run our RR-HC and the RR-SA algorithms through boards ranging n=8 to n=25
    # Find the best performing algorithm, i.e. the number of moves to reach optimal solution
    i = 0
    rrhc_moves = []
    rrsa_moves = []
    random_initial_board = getRandomNumbers(N)

    while i < 17:

        if heu_rrhc == 0:
            solution_rrhc, rrhc_count = randomRestartHillClimb(steepest_hill, steepest_hill_heu)
            rrhc_moves.append(rrhc_count)

        if heu_annealing == 0:
            solution_annealing, sa_count = annealing(random_initial_board)
            rrsa_moves.append(sa_count)

        i += 1

    return rrhc_moves, rrsa_moves


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
    print("\nCorrect Answer found in RR-HC")
    solution_rrhc, rrhc_count = randomRestartHillClimb(steepest_hill, steepest_hill_heu)
    heu_rrhc = getHeuristic(solution_rrhc)
    print(solution_rrhc)
    print("Total moves:", rrhc_count)
    displayBoard(solution_rrhc)

    print("\n------------------------------------------")

    # Simulated Annealing
    print("\nCorrect Answer found in Simulated Annealing")
    solution_annealing, sa_count = annealing(random_initial_board)
    heu_annealing = getHeuristic(solution_annealing)
    print(solution_annealing)
    print("Total moves:", sa_count)
    displayBoard(solution_annealing)

    print("\n------------------------------------------")

    # Evaluation
    print("\nEvaluation:")
    rrhc_moves, rrsa_moves = evaluation(heu_rrhc, heu_annealing, steepest_hill, steepest_hill_heu)
    print(rrhc_moves)
    print(rrsa_moves)



if __name__ == '__main__':
    main()









































