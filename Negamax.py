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

        # User's move
        user_input = input("Enter your move (column number 0-6): ")
        column = int(user_input)
        if column < 0 or column > 6 or board.board[0][column] != 0:
            print("Invalid move. Try again.")
            continue
        board.make_move(column)
        board.print_board()

    return basic_times, alpha_beta_times, alpha_beta_symmetry_times

# Start of the experiment
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
