import othello
import random
import math


# A class object used to represent a node
class Node(object):
    """ A Node in the tree

    Attributes:
        total: The total value of the node based on the children.
        hit_count: The number of times the node has been visited.
        children: A list of the children nodes of the node.
    """

    def __init__(self):
        self.total = 0
        self.hit_count = 0
        self.children = []

    def update_total(self, value):
        self.total += value

    def update_hit_count(self):
        self.hit_count += 1

    def add_children(self, child):
        self.children.append(child)


def copy_board(current_state):
    return current_state


# Selects a random move from available moves and returns the disks to be flipped.
def random_move(colour, moves):

    if not moves:
        return 0
    position = random.choice(moves)

    position = (othello.letters.index(position[0]['x_pos']), position[0]['y_pos'])

    vector_moves = list(map(lambda vec: othello.check_direction(
        vec, colour, position, [], othello.get_opponent(colour)), othello.directions))

    reduced = othello.reduce(othello.flatten_moves, vector_moves)
    return reduced


def get_node_score(avg, parent_node, node):
    # Exploration constant: Larger value == more exploration
    c = 2

    # othello.score(player)

    # Handle divide by 0, unvisited nodes are equal to an infinite value.
    if node == 0:
        return math.inf
    node_score = avg + math.sqrt((c * math.log(parent_node)) / node)
    return node_score


def monte_carlo():
    d6 = Node()
    print(d6.total)
    # Selection

    # Expansion

    # Simulation

    # Back propagation

    pass

print('s1')
print(get_node_score(24, 5, 1))
print('s2')
print(get_node_score(33, 5, 1))
print('s3')
print(get_node_score(28, 5, 1))
print('s4')
print(get_node_score(71, 5, 1))
print('s5')
print(get_node_score(31, 2, 1))
print('s6')
print(get_node_score(0, 2, 0))