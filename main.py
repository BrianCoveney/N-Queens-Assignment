import random
import math
import time
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.plotly as py
from sklearn.metrics import classification_report

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

    # h = getHeuristic(board)
    # if h == 0:
    #     print(board)

    return board


# ------------------------------------------
# Random Restart Algorithm
# :param old_steepest_hill: List returned from the steepestHill() algorithm
# :param old_steepest_hill_heu: Heuristic for the old_steepest_hill
# :return: solution configuration found and a running count
# ------------------------------------------
def randomRestartHillClimb(new_random, old_steepest_hill, old_steepest_hill_heu):
    restarts = 500
    restart_count = 0
    count_new_solution = 0
    count_old_solution = 0
    best_solution = []

    # Initially set the maximum number of restarts to 500
    while restart_count < restarts:
        # Generate a new random configuration for the initial state of the board, and get it's heuristic
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
                count_new_solution += 1
            else:
                count_old_solution += 1

        restart_count += 1

    return best_solution, restart_count


# A solution was found for our steepest ascent algorithm. Print details and exit.
# :param board: random board configuration
# :return: solution configuration found and a running count
# ------------------------------------------
def simulatedAnnealing(board):
    temp = 250000.0
    anneal_rate = 0.95
    heu_cost = getHeuristic(board)
    count = 0

    while heu_cost > 0:
        board = makeMove(board, heu_cost, temp)
        heu_cost = getHeuristic(board)
        # Make sure temp doesn't get impossibly low
        new_temp = max(temp * anneal_rate, 0.01)
        temp = new_temp
        count += 1

        # It is possible that the algorithm will get stuck.
        # To prevent this I have limited the iterations to 50000
        if count >= 50000:
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
# Evaluation:
# Run our RR-HC and the RR-SA algorithms through boards ranging n=8 to n=25
# Find the best performing algorithm, i.e. the number of moves to reach optimal solution
# :param heu_rrhc: heuristics for RR-HC
# :param heu_annealing: heuristics for RR-SA
# :param steepest_hill: List returned from the steepestHill() algorithm
# :param steepest_hill_heu: Heuristic for the old_steepest_hill
# :return: Lists of the number moves taken to reach a solution for RR-HC and RR-SA
# ------------------------------------------
def evaluation(heu_rrhc, heu_annealing, steepest_hill, steepest_hill_heu):
    board_eight_queens = N
    board_twenty_five_queens = 25
    rrhc_moves = []
    rrsa_moves = []
    while board_eight_queens <= board_twenty_five_queens:


        random_board_rrsa = getRandomNumbers(board_eight_queens)
        random_board_rrhc = getRandomNumbers(board_eight_queens)

        if heu_annealing == 0:
            solution_annealing, sa_count = simulatedAnnealing(random_board_rrsa)
            rrsa_moves.append(sa_count)
            # print(board, "Queens Solution for RR-SA algorithm %s in %d moves" % (solution_annealing, sa_count))

        if heu_rrhc == 0:
            solution_rrhc, rrhc_count = randomRestartHillClimb(random_board_rrhc, steepest_hill, steepest_hill_heu)
            rrhc_moves.append(rrhc_count)
            # print(board, "Queens Solution for RR-HC algorithm %s in %d moves" % (solution_rrhc, rrhc_count))
        board_eight_queens += 1

    return rrhc_moves, rrsa_moves


# ------------------------------------------
# Display Graphs for evaluation purposes
# ------------------------------------------
def displayGraphs(rrhc_moves, rrsa_moves):
    if rrhc_moves != 0 and rrsa_moves != 0:
        # Bar Chart showing of the average moves each algorithm takes to reach a solution.
        # Taken from running our algorithms through boards ranging n=8 to n=25
        rrhc_np = np.array(rrhc_moves)
        rrhc_mean = np.mean(rrhc_np)
        rrsa_np = np.array(rrsa_moves)
        rrsa_mean = np.mean(rrsa_np)
        displayBarChart("8-Queens to 25-Queens\nMean Moves till Solution", "moves", rrhc_mean, rrsa_mean)


        # BarChart for 8 Queens moves till solution for both algorithms
        rrhc_eight_board_moves = rrhc_moves[0]
        rrsa_eight_board_moves = rrsa_moves[0]
        displayBarChart("8-Queens\nMoves till Solution", "moves", rrhc_eight_board_moves, rrsa_eight_board_moves)

        # BarChart for 25 Queens moves till solution for both algorithms
        rrhc_twentyfive_board_moves = rrhc_moves[-1]
        rrsa_twentyfour_board_moves = rrsa_moves[-1]
        displayBarChart("25-Queens\nMoves  till Solution", "moves", rrhc_twentyfive_board_moves, rrsa_twentyfour_board_moves)


def displayBarChart(title, label, input1, input2):
    algos = ('RR-HC', 'RR-SA')
    y_pos = np.arange(len(algos))
    performance = [input1, input2]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, algos)
    plt.ylabel(label)
    plt.title(title)
    plt.show()


# ------------------------------------------
# Return a list of random numbers
# ------------------------------------------
def getRandomNumbers(num_queens):
    numbers = []
    for n in range(num_queens):
        numbers.append(n)
    random.shuffle(numbers)

    numbers = [6,5,1,2,7,0,4,3]
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
    print("Random Initial State\n", random_initial_board, sep="")
    print("Heuristic Value:", getHeuristic(random_initial_board))
    displayBoard(random_initial_board)


    print("------------------------------------------")

    # Move One Queen
    random_board_mo = getRandomNumbers(N)
    move_one = moveOneQueen(random_board_mo)
    print("\nMoving one position: ", move_one)
    move_one_heu = getHeuristic(move_one)
    print("Heuristic Value:", move_one_heu)

    print("------------------------------------------")

    # Steepest Hill Climbing
    random_board_sh = getRandomNumbers(N)
    steepest_hill = steepestHill(random_board_sh)
    print("\nSteepest hill:       ", steepest_hill)
    steepest_hill_heu = getHeuristic(steepest_hill)
    print("Heuristic Value:", steepest_hill_heu)

    print("------------------------------------------")

    # Random Restart Hill Climbing
    rrhc_start_time = time.time()
    random_board_rrhc = getRandomNumbers(N)
    solution_rrhc, rrhc_count = randomRestartHillClimb(random_board_rrhc, steepest_hill, steepest_hill_heu)
    heu_rrhc = getHeuristic(solution_rrhc)
    rrhc_processing_time = time.time() - rrhc_start_time

    print("\nCorrect Answer found in RR-HC")
    print(solution_rrhc)
    print("Heuristic Value:", heu_rrhc, "\nTotal moves:", rrhc_count)
    displayBoard(solution_rrhc)
    rrhc_execution_time = "Random Restart Hill processing time %s seconds" % rrhc_processing_time
    print(rrhc_execution_time)

    print("\n------------------------------------------")

    # Simulated Annealing
    sa_start_time = time.time()
    random_board_sa = getRandomNumbers(N)
    solution_annealing, sa_count = simulatedAnnealing(random_board_sa)
    heu_annealing = getHeuristic(solution_annealing)
    rrsa_processing_time = time.time() - sa_start_time

    print("\nCorrect Answer found in Simulated Annealing")
    print(solution_annealing)
    print("Heuristic Value:", heu_annealing, "\nTotal moves:", sa_count, )
    displayBoard(solution_annealing)
    rrsa_execution_time = "Simulated Annealing processing time %s seconds" % rrsa_processing_time
    print(rrsa_execution_time)

    print("\n------------------------------------------")

    # Evaluation
    print("\nEvaluation:")

    # Checks if 'steepest_hill' is a List. In some cases it's returned as an int
    rrhc_moves, rrsa_moves = evaluation(heu_rrhc, heu_annealing, steepest_hill, steepest_hill_heu)

    print("\n 17 runs of RR-HC", rrhc_moves)
    print("\n 17 runs of RR-SA", rrsa_moves)
    # Example:
    # 17 runs of RR-HC [22, 23, 160, 19, 41, 64, 44, 7, 48, 166, 49, 268, 62, 144, 178, 115, 80, 251]
    # 17 runs of RR-SA [171, 327, 192, 298, 264, 246, 322, 339, 404, 563, 698, 814, 208, 569, 432, 314, 881, 806]

    displayGraphs(rrhc_moves, rrsa_moves)

    displayBarChart("Processing Time", "seconds", rrhc_processing_time, rrsa_processing_time)


if __name__ == '__main__':
    main()


















