import numpy as np
import time
import matplotlib.pyplot as plt

class ConnectFour:
    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.current_player = 1
        self.moves = []

    def print_board(self):
        print(self.board)

    def make_move(self, column):
        for row in range(5, -1, -1):
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
                self.moves.append((self.current_player, column))
                return True
        return False

    def check_winner(self):
        # Check rows
        for row in range(6):
            for col in range(4):
                if self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] == self.board[row][
                    col + 3] != 0:
                    return self.board[row][col]

        # Check columns
        for col in range(7):
            for row in range(3):
                if self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] == self.board[row + 3][
                    col] != 0:
                    return self.board[row][col]

        # Check diagonals
        for row in range(3):
            for col in range(4):
                if self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == \
                        self.board[row + 3][col + 3] != 0:
                    return self.board[row][col]

        for row in range(3, 6):
            for col in range(4):
                if self.board[row][col] == self.board[row - 1][col + 1] == self.board[row - 2][col + 2] == \
                        self.board[row - 3][col + 3] != 0:
                    return self.board[row][col]

        return 0

    def switch_player(self):
        self.current_player = 1 if self.current_player == 2 else 2

    def get_possible_moves(self):
        return [col for col in range(7) if self.board[0][col] == 0]

    def is_board_full(self):
        return np.all(self.board != 0)

def basic_negamax(board, depth, maximizing_player):
    if depth == 0 or board.check_winner() != 0:
        return 0

    max_eval = float('-inf')
    for move in board.get_possible_moves():
        new_board = ConnectFour()
        new_board.board = np.copy(board.board)
        new_board.make_move(move)
        eval = -basic_negamax(new_board, depth - 1, not maximizing_player)
        max_eval = max(max_eval, eval)
    return max_eval

def negamax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.check_winner() != 0:
        return 0

    max_eval = float('-inf')
    for move in board.get_possible_moves():
        new_board = ConnectFour()
        new_board.board = np.copy(board.board)
        new_board.make_move(move)
        eval = -negamax_alpha_beta(new_board, depth - 1, -beta, -alpha, not maximizing_player)
        max_eval = max(max_eval, eval)
        alpha = max(alpha, eval)
        if alpha >= beta:
            break
    return max_eval

def negamax_alpha_beta_symmetry(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.check_winner() != 0:
        return 0

    max_eval = float('-inf')
    for move in board.get_possible_moves():
        new_board = ConnectFour()
        new_board.board = np.copy(board.board)
        new_board.make_move(move)
        eval = -negamax_alpha_beta_symmetry(new_board, depth - 1, -beta, -alpha, not maximizing_player)
        max_eval = max(max_eval, eval)
        alpha = max(alpha, eval)
        if alpha >= beta:
            break
    return max_eval

def run_experiment(board, depth):
    basic_times = []
    alpha_beta_times = []
    alpha_beta_symmetry_times = []

    while not board.is_board_full() and board.check_winner() == 0:
        # Basic Negamax
        start_time = time.time()
        basic_negamax(board, depth, True)
        basic_times.append(time.time() - start_time)

        # Alpha-Beta Pruning
        start_time = time.time()
        negamax_alpha_beta(board, depth, float('-inf'), float('inf'), True)
        alpha_beta_times.append(time.time() - start_time)

        # Alpha-Beta Pruning with Symmetry Reduction
        start_time = time.time()
        negamax_alpha_beta_symmetry(board, depth, float('-inf'), float('inf'), True)
        alpha_beta_symmetry_times.append(time.time() - start_time)

        # User's move (assuming predefined moves)
        if predefined_moves:
            row, column = predefined_moves.pop(0)
            board.make_move(column)  # Pass only the column as an argument
            board.print_board()
        else:
            print("No more predefined moves.")
            break

    return basic_times, alpha_beta_times, alpha_beta_symmetry_times

# Predefined moves
predefined_moves = [(5, 3), (5, 0), (5, 1), (4, 0), (4, 1), (4, 3)]

# start of experiment
board = ConnectFour()
depth = 4
basic_times, alpha_beta_times, alpha_beta_symmetry_times = run_experiment(board, depth)

# Print the execution times
print("Basic Negamax Times:", basic_times)
print("Alpha-Beta Pruning Times:", alpha_beta_times)
print("Alpha-Beta Pruning with Symmetry Reduction Times:", alpha_beta_symmetry_times)

# Plotting the graph for execution times
plt.plot(basic_times, label='Basic Negamax')
plt.plot(alpha_beta_times, label='Alpha-Beta Pruning')
plt.plot(alpha_beta_symmetry_times, label='Alpha-Beta Pruning with Symmetry Reduction')
plt.xlabel('Move Number')
plt.ylabel('Execution Time (s)')
plt.title('Execution Times of Negamax Techniques')
plt.legend()
plt.show()
