# Snekoban Game

import json
from turtle import pos
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    # My implementation will be a dictionary where each key is an object in the game (i.e. walls, player, flags) and the values are a frozenset of their coordinates.
    # This representation is one that will reduce look up time and optimize the speed for other methods
    
    #Representaion is a dictrionary of sets
    #Go through each coordinate in the game representation and add the corresponding objects coordinate to the dictionary
    game = {'walls': set(), 'computers': set(), 'targets': set(), 'width': len(level_description[0]), 'height': len(level_description)}
    for row in range(len(level_description)):
        for column in range(len(level_description[0])):
            #Position variable
            position = level_description[row][column]
            #
            if 'player' in position:
                game['player'] = (row, column)
            if 'wall' in position:
                game['walls'].add((row, column))
            if 'computer' in position:
                game['computers'].add((row, column))
            if 'target' in position:
                game['targets'].add((row, column))
    return game

def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """
    #Check if there are no targets or computers
    if len(game['targets']) == 0:
        return False
    #If the computers are all on the target's coordinates then game has been won
    return game['computers'] == game['targets']
    # for computer in game['computers']:
    #     if computer not in game['targets']:
    #         return False
    # return True

def valid_move(result, direction):
    next_move = (result['player'][0] + direction_vector[direction][0], result['player'][1] + direction_vector[direction][1])
    one_next_move = (next_move[0] + direction_vector[direction][0], next_move[1] + direction_vector[direction][1])
    #If next_move is a wall
    if next_move in result['walls']:
        return False
    #If next move is a computer against a wall
    if next_move in result['computers'] and one_next_move in result['walls']:
        return False
    #If next move is a computer against another computer
    if next_move in result['computers'] and one_next_move in result['computers']:
        return False
    return True

def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    result = {'player': game['player'], 'walls': game['walls'], 'computers': game['computers'].copy(), 'targets': game['targets'], 'width': game['width'], 'height': game['height']}

    next_move = (game['player'][0] + direction_vector[direction][0], game['player'][1] + direction_vector[direction][1])
    one_next_move = (next_move[0] + direction_vector[direction][0], next_move[1] + direction_vector[direction][1])

    if valid_move(game, direction):
        if next_move in result['computers']:
            result['computers'].remove(next_move)
            result['computers'].add(one_next_move)
        result['player'] = next_move
    return result
        


def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    #Go through every possible coordinate given the dimensions of the game and see if that coordinate is in wall, computer, player, or targets and rebuild accordingly
    l = []
    for row in range(game['height']):
        s = []
        for column in range(game['width']):
            w = []
            position = (row, column)
            if position in game['walls']:
                w.append('wall')
            if position in game['targets']:
                w.append('target')
            if position == game['player']:
                w.append('player')
            if position in game['computers']:
                w.append('computer')
            s.append(w)
        l.append(s)
    return l

def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    #States of game that have already been visited
    visited = set()
    #Queue that contains state and path to get to that state
    queue = []
    #Add starting state to visited
    #Had to cast to frozenset because set() does not allow unhashable types
    visited.add((frozenset((game['computers'])), game['player']))
    #Add starting state to queue
    queue.append([game, []])

    while queue:
        #print("Visited set:", visited)
        #print("Queue: ", queue)
        #Tuple that contains current position and path to that position
        current_state = queue.pop(0)
        #print("Current State: ", current_state)
        #Check if current state of game is winning state if it is, then return the path
        if victory_check(current_state[0]):
            return current_state[1]
        
        #Have states of each move in each direction
        for direction in direction_vector.keys():
            next_state = step_game(current_state[0], direction)
            #print(direction)
            #print("Next_state: ", next_state)
            s = (frozenset((next_state['computers'])), next_state['player'])
            if s not in visited:
                queue.append([next_state, current_state[1] + [direction]])
                # print([current_state[1] + [direction]])
                visited.add(s)
    return None


if __name__ == "__main__":
    pass