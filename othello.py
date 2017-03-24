import re
from functools import reduce

letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
game_board = [(x, y) for x in [chr(i) for i in range(ord('a'), ord('h') + 1)] for y in range(1, 9)]
directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

# Set dictionary to have coordinates as key and state stored in them
board_state = {}


# Set the board by populating the board_state
def set_board():
    for space in game_board:
        board_state[space] = '.'

    change_board([({'x_pos': 'd', 'y_pos': 4}, 'B'), ({'x_pos': 'e', 'y_pos': 5}, 'B'),
                  ({'x_pos': 'd', 'y_pos': 5}, 'W'), ({'x_pos': 'e', 'y_pos': 4}, 'W')])


# Takes a list of changes and updates the board state
def change_board(changes):

    # Exit condition
    if changes == 0:
        return 0

    for change in changes:
        if len(change) != 0:
            board_state[change[0]['x_pos'], change[0]['y_pos']] = change[1]


# Display the current game state
def display():
    print_letters()
    y = 1
    while y <= 8:
        x = 0
        print(y, end='|')
        while x < 8:
            print(board_state[letters[x], y], end='|')
            x += 1
        print(y)

        y += 1
    print_letters()


# Adds the letters along the top of the displayed board
def print_letters():
    print(end=' |')
    for letter in letters:
        print(letter, end='|')
    print()


# Takes the user input and ensures it is of the correct notation
def get_input():
    regex = r"([a-h][1-8])"
    pos = input('Where would you like to move?: ').strip()
    while not re.search(regex, pos):
        if pos == "exit" or pos == 'quit':
            return 0
        print("Notation incorrect should be a1")
        pos = input('Where would you like to move?: ')

    return {'x_pos': pos[0], 'y_pos': int(pos[1])}


# Ensures board checks avoid going off the board
def off_board_check(x_pos, y_pos):
    if x_pos < 0 or x_pos > 7 or y_pos <= 1 or y_pos > 7:
        return True
    return False


def flatten_moves(all_moves, item):

    print('flatten')
    print(item)
    if False not in item:
        all_moves += item

    print(all_moves)
    return all_moves


# Move is assigned the players colour and ensures a valid move is made
def move(colour):
    position = ''
    moved = False

    opponent = 'W'

    if colour == 'W':
        opponent = 'B'

    while not moved:
        position = get_input()

        # Exit game
        if position == 0:
            return 0

        position = (letters.index(position['x_pos']), position['y_pos'])

        # moved = valid_move(position['x_pos'], position['y_pos'], colour)
        vector_moves = list(map(lambda vec: check_direction(vec, colour, position, [], opponent), directions))
        reduced = reduce(flatten_moves, vector_moves)
        print(len(reduced))
        print('move')
        print(reduced)
        if len(reduced) > 1:
            return reduced
        print('Not a valid move, please try again')


# May be able to use check_direction to ensure flanking
def flanking_move(x_pos, y_pos, colour):
    local_disks = []
    index = letters.index(x_pos)

    x = -1
    while x <= 1:
        y = -1
        while y <= 1:
            if not off_board_check(index + x, y_pos + y):
                local_disks.append(board_state[letters[(index + x)], y_pos + y])
            y += 1
        x += 1

    if colour == 'W':
        if 'B' in local_disks:
            return True
        else:
            print("You must flank Black")
            return False
    elif colour == 'B':
        if 'W' in local_disks:
            return True
        else:
            print("You must flank White")
            return False


def check_direction(vector, player, pos, lst, find):

    lst.append(({'x_pos': letters[pos[0]], 'y_pos': pos[1]}, player))

    pos = (pos[0] + vector[0], pos[1] + vector[1])

    if not off_board_check(pos[0], pos[1]):

        # If end of vector search is blank, not a valid move so return no changes
        if board_state[letters[pos[0]], pos[1]] == '.':
            return [False]

        # If the current player colour has been found return the list of disks.
        elif board_state[letters[pos[0]], pos[1]] == player:
            return lst

        elif board_state[letters[pos[0]], pos[1]] == find:
            return [lst[0]] + check_direction(vector, player, pos, lst[1:], find)

    return []


def get_moves(colour):
    vector_moves = []
    for space in board_state:
        if board_state[space] == '.':
            position = (letters.index(space[0]), space[1])
            vector_moves += list(map(lambda vec: check_direction(vec, colour, position, [], 'W'), directions))

    reduced = reduce(flatten_moves, vector_moves)

    print(reduced)


# The game loop
def game():
    # Set's the board for starting state
    set_board()

    # The game is now set to playing
    playing = True

    # Initial player is set, in reversi/othello this is black
    player = 'B'

    # Provide basic instructions to enter moves and exit the game
    print("Type exit to quit. To make a move please use the following notation a1")

    # A playing loop, currently the only means to end the game is to manually exit
    while playing:
        print(player + "'s go")
        # colour -> player makes move -> move validated -> make change
        display()
        #get_moves(player)
        # End game if user enters exit or quit
        if change_board(move(player)) == 0:
            print('exit code 0')
            break

        # Swap player turn
        if player == 'B':
            player = 'W'
        else:
            player = 'B'


game()
