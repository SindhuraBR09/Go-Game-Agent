import random
import sys
import copy
from random import shuffle

komi = 2.5

def readInput(n, path="input.txt"):

    with open(path, 'r') as f:
        lines = f.readlines()

        piece_type = int(lines[0])

        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n+1]]
        board = [[int(x) for x in line.rstrip('\n')] for line in lines[n+1: 2*n+1]]

        return piece_type, previous_board, board

def writeOutput(result, path="output.txt"):
    res = ""
    if result == "PASS":
    	res = "PASS"
    else:
	    res += str(result[0]) + ',' + str(result[1])

    with open(path, 'w') as f:
        f.write(res)


def get_input( go, piece_type):
    '''
    Get one input.

    :param go: Go instance.
    :param piece_type: 1('X') or 2('O').
    :return: (row, column) coordinate of input.
    '''
    possible_placements = []
    for i in range(go.size):
        for j in range(go.size):
            if go.valid_place_check(i, j, piece_type, test_check = True):
                possible_placements.append((i,j))

    if not possible_placements:
        return "PASS"
    else:
        return random.choice(possible_placements)


def compare_board( board1, board2):
    for i in range(5):
        for j in range(5):
            if board1[i][j] != board2[i][j]:
                return False
    return True

def copy_board():
    '''
    Copy the current board for potential testing.

    :param: None.
    :return: the copied board instance.
    '''
    return deepcopy()

#new method
def place_move(cur_board, row, col, player):

    new_board = copy.deepcopy(cur_board)
    new_board[row][col] = player

    return new_board

def detect_neighbor(i, j, board):
    '''
    Detect all the 4 neighbors of a given stone.

    :param i: row number of the board.
    :param j: column number of the board.
    :return: a list containing the neighbors row and column (row, column) of position (i, j).
    '''

    neighbors = []
    # Detect borders and add neighbor coordinates
    if i > 0: neighbors.append((i-1, j))
    if i < len(board) - 1: neighbors.append((i+1, j))
    if j > 0: neighbors.append((i, j-1))
    if j < len(board) - 1: neighbors.append((i, j+1))
    return neighbors

def detect_neighbor_ally(i, j, new_board):
    '''
    Detect the neighbors that are having same color as given stone.

    :param i: row number of the board.
    :param j: column number of the board.
    :return: a list containing the neighbored allies row and column (row, column) of position (i, j).
    '''

    '''
    first get all the 4 neighbors then filter only those having same color as new move
    '''
    neighbors = detect_neighbor(i, j, new_board)  # Detect neighbors
    group_allies = []
    # Iterate through neighbors
    for piece in neighbors:
        # Add to allies list if having the same color
        #Sindhura added not in check
        if new_board[piece[0]][piece[1]] == new_board[i][j] and piece not in group_allies:
            group_allies.append(piece)
    return group_allies

def ally_dfs(i, j, new_board):
    '''
    Get all the connected stones of same color (not just the neighboring once but all the positions that are connected)

    :param i: row number of the board.
    :param j: column number of the board.
    :return: a list containing the all allies row and column (row, column) of position (i, j).
    '''
    stack = [(i, j)]  # stack for DFS serach
    ally_members = []  # record allies positions during the search
    while stack:
        piece = stack.pop()
        ally_members.append(piece)
        neighbor_allies = detect_neighbor_ally(piece[0], piece[1], new_board)
        for ally in neighbor_allies:
            if ally not in stack and ally not in ally_members:
                stack.append(ally)
    return ally_members

def find_liberty(i, j, new_board):
    '''
    Find the list of liberties that new move has. Count the liberties of its connected stones also (same color stones)

    :param i: row number of the board.
    :param j: column number of the board.
    :return: boolean indicating whether the given stone still has liberty.
    '''

    #added code (instead of returning boolean)
    all_liberties = []
    #TODO send cur_board

    '''
    all_dfs() will return all the nodes that are connected(even the farthest) to new move.
    Iterate through all these node and find if they have any empty position orthogonally adjacent
    '''
    ally_members = ally_dfs(i, j, new_board)
    for member in ally_members:
        neighbors = detect_neighbor(member[0], member[1], new_board)
        for piece in neighbors:
            # If there is empty space around a piece, it has liberty
            #Sindhura added not in check
            if new_board[piece[0]][piece[1]] == 0 and piece not in all_liberties:
                all_liberties.append((piece[0], piece[1]))

    return all_liberties

def find_died_pieces(piece_type, new_board):
    '''
    Find the died stones that has no liberty in the board for a given piece type.

    :param piece_type: 1('X') or 2('O').
    :return: a list containing the dead pieces row and column(row, column).
    '''
    died_pieces = []

    for i in range(len(new_board)):
        for j in range(len(new_board)):
            # Check if there is a piece at this position:
            if new_board[i][j] == piece_type:
                # The piece die if it has no liberty
                #TODO check length of liberties instead of not liberty
                liberties = find_liberty(i, j, new_board)
                if not liberties and (i,j) not in died_pieces:
                    died_pieces.append((i,j))
    return died_pieces

def remove_died_pieces(piece_type, new_board):
    '''
    Remove the dead stones in the board.
    :param piece_type: 1('X') or 2('O').
    :return: locations of dead pieces.
    '''
    died_pieces = find_died_pieces(piece_type, new_board)
    #TODO check length of died piece
    if len(died_pieces) == 0:
        return new_board, died_pieces
    new_board = remove_certain_pieces(died_pieces, new_board)
    return new_board, died_pieces

def remove_certain_pieces(positions, new_board):
    '''
    Remove the stones of certain locations.

    :param positions: a list containing the pieces to be removed row and column(row, column)
    :return: None.
    '''
    for piece in positions:
        new_board[piece[0]][piece[1]] = 0
    return new_board

def find_all_liberties(new_board, piece_type):

    '''
    Calls find_liberty()
    '''
    total_liberties = []
    positions = []
    for i in range(5):
        for j in range(5):
            if new_board[i][j] == piece_type:
                positions.append((i,j))

    for position in positions:
        liberty = find_liberty(position[0],position[1], new_board)
        difference = set(liberty) - set(total_liberties)
        total_liberties = total_liberties + list(difference)

    return total_liberties


def valid_place_check(i, j, cur_board, previous_board, piece_type):
    '''
    Check whether a placement is valid.

    :param i: row number of the board.
    :param j: column number of the board.
    :param piece_type: 1(white piece) or 2(black piece).
    :param test_check: boolean if it's a test check.
    :return: boolean indicating whether the placement is valid.
    '''

    # Check if the place already has a piece
    if cur_board[i][j] != 0:
        return False, [], []

    new_board = []
    new_board = place_move(cur_board, i,j, piece_type)

    all_liberties = find_liberty(i, j, new_board)
    if len(all_liberties) != 0 :
        died_pieces = find_died_pieces(3-piece_type, new_board)
        my_dead_stones = find_died_pieces(piece_type, new_board)
        return True, died_pieces, my_dead_stones

    # If not, remove the died pieces of opponent and check again
    new_board, died_pieces=remove_died_pieces(3 - piece_type, new_board)
    all_liberties = find_liberty(i, j, new_board)
    my_dead_stones = find_died_pieces(piece_type, new_board)
    if len(all_liberties) == 0:
        return False, died_pieces, my_dead_stones

    # Check special case: repeat placement causing the repeat board state (KO rule)
    else:
        if len(died_pieces) != 0 and compare_board(previous_board, new_board):
            return False, died_pieces, my_dead_stones
    return True, died_pieces, my_dead_stones

def get_all_valid_positions(cur_board, previous_board, piece_type):
    '''
    Get one input.

    :param go: Go instance.
    :param piece_type: 1('X') or 2('O').
    :return: (row, column) coordinate of input.
    '''
    possible_placements = []
    for i in range(5):
        for j in range(5):
            is_valid, dead_pieces, my_dead_pieces = valid_place_check(i, j, cur_board, previous_board, piece_type)
            if is_valid:
                possible_placements.append((i,j, (len(dead_pieces) - len(my_dead_pieces))))

    if len(possible_placements) > 0:
        return sorted(possible_placements, key=lambda x:-x[2])
    return possible_placements

def is_Q1(i,j, new_board,player):

    if i-1 >= 0:
        if j-1 >= 0:
            if new_board[i-1][j] == 0 and new_board[i][j-1] == 0 and new_board[i-1][j-1] == 0:
                return True
        if j+1 < 5:
            if new_board[i-1][j] == 0 and new_board[i][j+1] == 0 and new_board[i-1][j+1] == 0:
                return True
    if i+1 < 5:
        if j-1 >= 0:
            if new_board[i+1][j] == 0 and new_board[i][j-1] == 0 and new_board[i+1][j-1] == 0:
                return True
        if j+1 < 5:
            if new_board[i+1][j] == 0 and new_board[i][j+1] == 0 and new_board[i+1][j+1] == 0:
                return True

    return False


def is_Q2(i,j, new_board,player):

    if i-1 >= 0:
        if j-1 >= 0:
            if new_board[i-1][j] == player and new_board[i][j-1] == player and new_board[i-1][j-1] == 0:
                return True
        if j+1 < 5:
            if new_board[i-1][j] == player and new_board[i][j+1] == player and new_board[i-1][j+1] == 0:
                return True
    if i+1 < 5:
        if j-1 >= 0:
            if new_board[i+1][j] == player and new_board[i][j-1] == player and new_board[i+1][j-1] == 0:
                return True
        if j+1 < 5:
            if new_board[i+1][j] == player and new_board[i][j+1] == player and new_board[i+1][j+1] == 0:
                return True
    return False

def is_Q3(i,j, new_board,player):
    count = 0
    if i+1 < 5:
        if j-1 >= 0:
            if new_board[i+1][j] == 0 and new_board[i][j-1] == 0 and new_board[i+1][j-1] == player:
                count = count +1
        if j+1 < 5:
            if new_board[i+1][j] == 0 and new_board[i][j+1] == 0 and new_board[i+1][j+1] == player:
                count = count +1
    return count


def calculate_Euler_score(new_board, player):
    q1 = 0
    q2 = 0
    q3 = 0

    for i in range(5):
        for j in range(5):
            if is_Q1(i,j, new_board,player):
                q1 = q1+1
            elif is_Q2(i,j,new_board,player):
                q2 = q2+1
            else:
                q3 = q3 + is_Q3(i,j, new_board, player)

    euler_score = (q1 - q2 +  2*q3)/4
    return euler_score

#TODO
def calculate_score(new_board, player):
    #border values need to be prioritized?
    #place the move and find the score + number of liberties of both black and white + number of black dead stones aft placing the move
    black_score = 0
    white_score = 0
    number_of_blacks = 0
    number_of_whites = 0
    score = 0

    for i in range(5):
        for j in range(5):
            if new_board[i][j] == 1:
                number_of_blacks += 1
                if isCornerPositions(i,j) and main_player == 1:
                    number_of_blacks = number_of_blacks - 0.05
                if isBoundaryPosition(i,j) and main_player == 1:
                    number_of_blacks = number_of_blacks - 0.25

                neighbors = detect_neighbor(i,j, new_board)
                count = 0
                for (a,b) in neighbors:
                    if new_board[a][b] == 1 and player == 1:
                        count = count + 1
                    if new_board[a][b] == 2:
                        if main_player == 1:
                            number_of_blacks= number_of_blacks + 0.50
                if count == len(neighbors):
                    number_of_blacks = number_of_blacks - 0.25

            if new_board[i][j] == 2:
                number_of_whites += 1
                if isCornerPositions(i,j) and main_player == 2:
                    number_of_whites = number_of_whites - 0.05
                if isBoundaryPosition(i,j) and main_player == 2:
                    number_of_whites = number_of_whites - 0.25

                neighbors = detect_neighbor(i,j, new_board)
                count = 0
                for (a,b) in neighbors:
                    if new_board[a][b] == 2 and player == 2:
                        count = count + 1
                    if new_board[a][b] == 1:
                        if main_player == 2:
                            number_of_whites= number_of_whites + 0.50
                if count == len(neighbors):
                    number_of_whites = number_of_whites - 0.25

    black_score = number_of_blacks
    white_score = number_of_whites + komi

    if main_player == 1:
        score = black_score - white_score
    if main_player == 2:
        score = white_score - black_score - komi

    #find the number of opposite stones that the new move removes from board
    died_pieces = find_died_pieces(3-player, new_board)
    died_pieces = len(died_pieces)
    if player != main_player:
        died_pieces = -1 * died_pieces
    #find the number of liberties new move leaves
    player_liberties = find_all_liberties(new_board, main_player)
    opposite_player_liberties = find_all_liberties(new_board, 3-main_player)
    #TODO not happening correctly
    reduced_liberty = len(player_liberties) - len(opposite_player_liberties)
    # reduced_liberty = min(max(reduced_liberty,-4), 4)
    euler_score = calculate_Euler_score(new_board, main_player)
    return 0.725 * score + 0.1 * reduced_liberty + 0.1* euler_score + 0.025 *died_pieces
    # return score + reduced_liberty + euler_score + died_pieces

def isCornerPositions(i, j):
    if (i == 0 and j == 0) or (i == 4 and j == 0) or (i == 0 and j == 4) or (i==4 and j==4):
        return True
    else:
        return False

def isBoundaryPosition(i,j):
    if i ==0 or j == 0 or i == 4 or j == 4:
        return True
    else:
        return False

def find_score(new_board, player):
    black_score = 0
    white_score = 0
    number_of_blacks = 0
    number_of_whites = 6
    black_in_danger = 0
    white_in_danger = 0

    for i in range(5):
        for j in range(5):
            if new_board[i][j] == 1:
                number_of_blacks += 1
                temp_liberty = find_liberty(i,j, new_board)
                if len(temp_liberty) <= 1:
                    black_in_danger += 1
            elif new_board[i][j] == 2:
                number_of_whites += 2
                temp_liberty = find_liberty(i,j, new_board)
                if len(temp_liberty) <= 1:
                    white_in_danger += 1

    if player == 1:
        score = 10*number_of_blacks - 10*number_of_whites + 2*white_in_danger - 1.5*black_in_danger
    else:
        score =  10*number_of_whites - 10*number_of_blacks + 2*black_in_danger - 1.5*white_in_danger
    return score



def max_alpha_beta(cur_board, previous_board, n, player, alpha, beta):
    infinity = float('inf')
    best_score = -infinity
    best_move = []
    if n == 0:
        final_score = find_score(cur_board, player)
        return final_score, []

    possible_moves = get_all_valid_positions(cur_board, previous_board, player)
    # shuffle(possible_moves)
    for move in possible_moves:
        new_board = place_move(cur_board, move[0], move[1], player)
        new_board,died_pieces = remove_died_pieces(3-player, new_board)
        score, action = min_alpha_beta( new_board, cur_board,n-1, 3-player, alpha, beta ) #TODO define alpha beta
        my_died_pieces = find_died_pieces(player, new_board)
        score = score + (5*len(died_pieces)) - (8.5*len(my_died_pieces))
        if score > best_score:
            best_score = score
            best_move = move
        if best_score >= beta:
            best_move = move
            return best_score, best_move
        alpha = max(alpha, best_score)
        best_move = move

    return best_score, best_move


def min_alpha_beta( cur_board, previous_board, n , player,alpha, beta):
    infinity = float('inf')
    best_score = infinity
    best_move = []

    if n == 0:
        final_score = find_score(cur_board, player)
        return final_score, []

    possible_moves = get_all_valid_positions(cur_board, previous_board, player)
    for move in possible_moves:
        new_board = place_move( cur_board, move[0], move[1], player)
        new_board, died_pieces = remove_died_pieces(3-player, new_board)
        score, action = max_alpha_beta( new_board, cur_board, n-1, 3-player, alpha, beta ) #TODO change the 3- logic
        my_died_pieces = find_died_pieces(player, new_board)
        score = score + (5*len(died_pieces)) - (8.5*len(my_died_pieces))
        if score < best_score:
            best_score = score
            best_move = move
        if best_score <= alpha:
            best_move = move
            return score, best_move
        if best_score < beta:
            beta = min(beta, score)
        # best_move = move

    return best_score, best_move


def alpha_beta_pruning(cur_board, previous_board, depth, maximizing, player):
    best_state = []
    #handle the first move manually
    if isFirstMove(cur_board):
        if cur_board[2][2] != 0:
            return [(2,1)]
        else:
            return [(2,2)]

    infinity = float('inf')
    alpha = -infinity
    beta = infinity

    score, best_state = max_alpha_beta(cur_board, previous_board, depth, player, alpha, beta)
    if len(best_state) == 0:
        return ['PASS']
    return [best_state]

def findOccupiedPositions(cur_board):
    pos = 0
    for i in range(5):
        for j in range(5):
            if cur_board[i][j] == 1 or cur_board[i][j] == 2:
                pos += 1

    print("Sindhura : number of occupied pos ", pos)
    return pos

def isFirstMove(cur_board):
    if findOccupiedPositions(cur_board) <= 1:
        return True
    else:
        return False

if __name__ == "__main__":
    N = 5
    global main_player
    piece_type, previous_board, current_board = readInput(N)
    main_player = piece_type
    action = alpha_beta_pruning(current_board, previous_board, 2, True, piece_type)
    print("Next move and stone type ", action, piece_type)
    writeOutput(action[0])
