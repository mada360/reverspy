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
        if change and len(change) != 0:
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
    if x_pos < 0 or x_pos > 7 or y_pos < 1 or y_pos > 8:

        return True
    return False


# Reduces lists into one dimensional lists.
def flatten_moves(all_moves, item):

    if False not in item and len(item) > 1:
        all_moves += item

    return all_moves


# Move is assigned the players colour and ensures a valid move is made
def move(colour):
    position = ''
    moved = False

    while not moved:
        position = get_input()

        # Exit game
        if position == 0:
            return 0

        position = (letters.index(position['x_pos']), position['y_pos'])

        vector_moves = list(map(lambda vec: check_direction(
            vec, colour, position, [], get_opponent(colour)), directions))

        reduced = reduce(flatten_moves, vector_moves)

        if len(reduced) > 1:
            return reduced
        print('Not a valid move, please try again')


# Checks all directions and returns a list of all possible moves and disks that could be changed.
def check_direction(vector, player, pos, lst, opponent):

    lst.append(({'x_pos': letters[pos[0]], 'y_pos': pos[1]}, player))

    pos = (pos[0] + vector[0], pos[1] + vector[1])

    if not off_board_check(pos[0], pos[1]):

        # If end of vector search is blank, not a valid move so return no changes
        if board_state[letters[pos[0]], pos[1]] == '.':
            return [False]

        # If the current player colour has been found return the list of disks.
        elif board_state[letters[pos[0]], pos[1]] == player:
            return lst

        # If opponent disk found, add position to list
        elif board_state[letters[pos[0]], pos[1]] == opponent:
            return [lst[0]] + check_direction(vector, player, pos, lst[1:], opponent)

    return [False]


# Simply returns the opponent colour based on the current player
def get_opponent(player):
    if player == 'W':
        return 'B'

    return 'W'


# Get a list of possible moves to be made
def get_moves(player, opponent):
    vector_moves = []

    # Check every blank space if there is a possible move
    for space in board_state:
        if board_state[space] == '.':
            position = (letters.index(space[0]), space[1])
            vector_moves += list(map(lambda vec: check_direction(vec, player, position, [], opponent), directions))

    if len(vector_moves) < 1:
        print('No more moves')
        return False

    reduced = reduce(flatten_moves, vector_moves)

    moves = []

    for position in reduced:

        if position and board_state[position[0]['x_pos'], position[0]['y_pos']] == '.':
            if position not in moves:
                moves.append(position)

    return moves


# Prints the available moves into a more readable format for the player.
def display_moves(moves_lst):
    for position in moves_lst:
        print(position[0]['x_pos'], position[0]['y_pos'], end=", ", sep="")
    print('')


# Returns the player's score
def score(player):
    player_score = 0

    for space in board_state:
        if board_state[space] is player:
            player_score += 1

    return player_score


# Prints the current score for both players
def display_score(player, opponent):
    print(player, score(player))
    print(opponent, score(opponent))
