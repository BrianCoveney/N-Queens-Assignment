import random


# ------------------------------------------
# Returns the heuristic value of our initial board state
# - outer loop is the rows in the range of our random
# ------------------------------------------
def getHeuristic(random_list):
    heuristic = 0

    for row in range(len(random_list)):
        for col in range(row + 1, len(random_list)):
            # Increment our heuristic if there are Queens are in the same row
            if random_list[row] == random_list[col]:
                heuristic += 1
            # Get the difference between the current column
            # and the check column
            offset = col - row
            # To be a diagonal, the check column value has to be
            # equal to the current column value +/- the offset
            if random_list[row] == random_list[col] - offset  or random_list[row] == random_list[col] + offset:
                heuristic += 1

    return heuristic


def make_move_first_choice(board):
    h_to_beat = getHeuristic(board)
    for col in range(len(board)):
        for row in range(len(board)):
            if board[col] == row:
                # We don't need to evaluate the current
                # position, we already know the h-value
                continue

            board_copy = list(board)
            # Move the queen to the new row
            board_copy[col] = row
            new_h_cost = getHeuristic(board_copy)

            # Return the first better (not best!) match you find
            if new_h_cost < h_to_beat:
                board[col] = row
                return board

    return board


# ------------------------------------------
# Return as list of random numbers
# ------------------------------------------
def getRandomNumbers():
    numbers = [3, 4, 7, 5, 0, 2, 1, 6]
    return numbers


# ------------------------------------------
# Prints the chess board with:
#  - positions of 'Q's retrieved from the index of our random number list
#  - otherwise positions are left blank
# ------------------------------------------
def displayBoard(num_queens):

    for row in range(num_queens):
        print("", end="|")

        queen = getRandomNumbers().index(row)

        for col in range(num_queens):
            if col == queen:
                print("Q", end="|")
            else:
                print("_", end="|")
        print("")


# ------------------------------------------
# Returns the selected number of queens
# Allows for changing the size of the board
# ------------------------------------------
def getNumQueens(count):
    return count


def main():
    num_queens = getNumQueens(8)

    random_list = getRandomNumbers()
    print("Random Initial State:", random_list)

    heuristic = getHeuristic(random_list)
    print("Heuristic Value:", heuristic)

    # first_choice_hc = make_move_first_choice(random_list)
    # print(first_choice_hc)
    displayBoard(num_queens)

if __name__ == '__main__':
    main()
