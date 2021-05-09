def play_a_game(board, player1, player2):
    turn = 0
    players = [player1, player2]

    end = False
    while not end:
        players[turn].move()
        turn = 1 - turn

        end = board.check_if_ended()

    print(board.matrix)
    print(f"Winner is {board.winner}")
    board.plot_board()
