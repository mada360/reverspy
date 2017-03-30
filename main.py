from othello import *
from ai import *


# The game loop
def game():

    test()

    # Set's the board for starting state
    set_board()

    # The game is now set to playing
    playing = True

    # Initial player is set, in Reversi/othello this is black
    player = 'B'
    opponent = get_opponent(player)

    # Assign computer to player(s)
    computer = 'W'

    print('Computer is ', computer)

    move_number = 0

    # Provide basic instructions to enter moves and exit the game
    print("Type exit to quit. To make a move please use the following notation a1")

    # A playing loop, currently the only means to end the game is to manually exit
    while playing:
        display_score(player, opponent)
        print(player + "'s go." + ' moves made: ' + str(move_number))
        # colour -> player makes move -> move validated -> make change
        display()
        if True:  # player is computer:
            if 0 == change_board(random_move(player, get_moves(player, opponent))):
                playing = False
        else:
            display_moves(get_moves(player, opponent))
            # End game if user enters exit or quit
            if change_board(move(player)) == 0:
                print('exit code 0')
                break

        move_number += 1

        # Swap players
        player = opponent
        opponent = get_opponent(player)

game()
