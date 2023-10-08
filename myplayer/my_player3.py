import random
import sys
import copy
from random import shuffle
from heapq import heappush, heappop

komi = 2.5
deadOpponent  = 0
deadSelf = 0
branch_factor = 15

'''
Below methods are taken from host.py
readInput
writeOutput
get_input
compare_board
detect_neighbor
detect_neighbor_ally
ally_dfs
find_liberty
find_died_pieces
remove_died_pieces
remove_certain_pieces
valid_place_check
'''

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
        return False

    new_board = []
    new_board = place_move(cur_board, i,j, piece_type)

    all_liberties = find_liberty(i, j, new_board)
    if len(all_liberties) != 0 :
        return True

    # If not, remove the died pieces of opponent and check again
    new_board, died_pieces=remove_died_pieces(3 - piece_type, new_board)
    all_liberties = find_liberty(i, j, new_board)

    if len(all_liberties) == 0:
        return False

    # Check special case: repeat placement causing the repeat board state (KO rule)
    else:
        if len(died_pieces) != 0 and compare_board(previous_board, new_board):
            return False
    return True

def get_all_valid_positions(cur_board, previous_board, piece_type):
    valid_placements = []
    favourable_moves = []
    i = 15
    h = -1
    for i in range(5):
        for j in range(5):
            if cur_board[i][j] == 0:
                is_valid = valid_place_check(i, j, cur_board, previous_board, piece_type)
                if is_valid:
                    deadStones = h * (deadOpponent - deadSelf)
                    heappush( valid_placements, ( deadStones, calculate_score(cur_board, main_player) , (i,j) ) )

    i = min(15, len(valid_placements))
    for j in range(0,i):
        favourable_moves.append(heappop(valid_placements)[2])
    return favourable_moves

def isCornerPositions(i, j, new_board, total_black, total_white, player):

    if ((i,j) == (0,0)) or ((i,j) == (0,4)) or ((i,j) == (4,0))or((i,j) == (4,4)):
        if player == 2:
            if new_board[i][j] ==2:
                total_white =  total_white -(5/100)
        elif player == 1:
            if new_board[i][j] == 1:
                total_black =  total_black - (5/100)

    return total_black, total_white


def isBoundaryPosition(i, j, new_board, total_black, total_white, player):

    if((i == 0) or (j == 0) or (i == 4)or(j == 4)):
        if player == 1:
            if new_board[i][j] == 1:
                total_black = total_black- (1/40)
        elif player == 2:
            if new_board[i][j] == 2:
                total_white = total_white- (1/40)
    return total_black, total_white

def black_surrounding_score(i,j,new_board, Nblacks, player):
    neighbors = detect_neighbor(i,j, new_board)
    # Nblacks = Nblacks+ 1
    count = 0
    i = 0
    while(i < len(neighbors)):
        (a,b) = neighbors[i]
        if new_board[a][b] == 2 and player ==1:
            Nblacks = Nblacks+ (1/2)
            count = count+ 1
        i = i+1

    if count == len(neighbors)-1:
        Nblacks = Nblacks- (1/4)

    return Nblacks


def white_surrounding_score(i,j,new_board, Nwhite, player):
    # Nwhite = Nwhite+ 1
    count= 0
    neighbors = detect_neighbor(i, j, new_board)
    i = 0

    while(i<len(neighbors)):
        (a,b) = neighbors[i]
        if new_board[a][b] == 1 and player == 2:
            Nwhite = Nwhite+ (1/2)
            count += 1
        i=i+1

    if count == len(neighbors)-1:
        Nwhite = Nwhite- (1/4)

    return Nwhite


def calculate_connected_score(new_board, player):

    self_eyes=0
    connectedStones=[]

    for i in range(5):
        for j in range(5):
            if new_board[i][j] == main_player:
                neighbhors = detect_neighbor(i,j, new_board)
                for (a,b) in neighbhors:
                    if new_board[a][b] == player:
                        connectedStones.append((a,b))
            if new_board[i][j]==0:
                sum=0
                neighbor=detect_neighbor(i,j,new_board)
                for (a,b) in neighbor:
                    if new_board[a][b] == player:
                        sum+=1

                if sum==len(neighbor):
                    self_eyes += 1

    return len(connectedStones)-self_eyes, self_eyes

def calculate_remaining_stones2(new_board, player):
    Nblacks = 0
    Nwhite = 0
    new_board2 = copy.deepcopy(new_board)

    for i in range(5):
        for j in range(5):
            Nblacks, Nwhite = isCornerPositions(i,j,new_board, Nblacks, Nwhite, player)
            Nblacks, Nwhite = isBoundaryPosition(i,j,new_board, Nblacks, Nwhite, player)

            if(new_board2[i][j]==1):
                Nblacks = Nblacks+ 1
                Nblacks = black_surrounding_score(i,j, new_board, Nblacks, player)

            elif(new_board2[i][j]==2):
                Nwhite = Nwhite+ 1
                Nwhite = white_surrounding_score(i,j,new_board, Nwhite, player)

    if (main_player==2):
        score= Nwhite - Nblacks
    elif (main_player==1):
        score= Nblacks - Nwhite - komi
    return score

def getReducedLiberty(new_board):
    player_liberty = 0
    opponent_liberty = 0

    for i in range(5):
        for j in range(5):
            if (new_board[i][j] == 0):
                neighbours = detect_neighbor(i,j,new_board)
                for (a,b) in neighbours:
                    if (new_board[a][b] == main_player):
                        player_liberty += 1
                    elif (new_board[a][b] == 3-main_player):
                        opponent_liberty += 1

    return (player_liberty) - (opponent_liberty)

#TODO
def calculate_score(new_board, player):
    score = calculate_remaining_stones2(new_board, player)
    eulerValue, eyes = calculate_connected_score(new_board, player)
    reduced_liberty = getReducedLiberty(new_board)
    uVal =  (0.725 * score) + (0.1 * reduced_liberty) + (0.1* eulerValue) + (0.075*eyes)
    return uVal

def get_updated_board(cur_board, row, col, player):
    global deadSelf, deadOpponent

    new_board = place_move(cur_board, row, col, player)
    died_pieces = find_died_pieces(3-player, new_board)
    if player == main_player:
        deadSelf += len(died_pieces)
    else:
        deadOpponent += len(died_pieces)

    if len(died_pieces) > 0:
        for position in died_pieces:
            new_board[position[0]][position[1]] = 0

    return new_board


def max_alpha_beta(cur_board, previous_board, n, player, alpha, beta):
    infinity = float('inf')
    best_score = -infinity
    best_move = ()
    if n == 0:
        final_score = calculate_score(cur_board, main_player)
        deadOpponent = 0
        deadSelf = 0
        return final_score, ()

    possible_moves = get_all_valid_positions(cur_board, previous_board, player)
    for move in possible_moves:
        new_board = get_updated_board(cur_board, move[0], move[1], player)
        # new_board,died_pieces = remove_died_pieces(3-player, new_board)
        score, action = min_alpha_beta( new_board, cur_board,n-1, 3-player, alpha, beta ) #TODO define alpha beta
        if score > best_score:
            best_score = score
            best_move = move
        # if best_score >= beta:
        #     best_move = move
        #     return best_score, best_move
        # alpha = max(alpha, best_score)
        best_score = max(best_score,score)
        alpha = max(alpha,best_score)
        if beta <= alpha:
            break

    return best_score, best_move


def min_alpha_beta( cur_board, previous_board, n , player,alpha, beta):
    infinity = float('inf')
    best_score = infinity
    best_move = ()

    if n == 0:
        final_score = calculate_score(cur_board, main_player)
        deadOpponent = 0
        deadSelf = 0

        return final_score, ()

    possible_moves = get_all_valid_positions(cur_board, previous_board, player)
    for move in possible_moves:
        new_board = get_updated_board(cur_board, move[0], move[1], player)
        # new_board, died_pieces = remove_died_pieces(3-player, new_board)
        score, action = max_alpha_beta( new_board, cur_board, n-1, 3-player, alpha, beta ) #TODO change the 3- logic
        if score < best_score:
            best_score = score
            best_move = move
        # if best_score <= alpha:
        #     best_move = move
        #     return score, best_move
        # if best_score < beta:
        #     beta = best_score

        best_score = min(best_score, score)
        beta = min(beta, best_score)
        if beta <= alpha:
              break

    return best_score, best_move


def alpha_beta_pruning(cur_board, previous_board, depth, player):
    global deadOpponent, deadSelf

    best_state = []
    #handle the first move manually
    if isFirstMove(cur_board):
        if cur_board[2][2] == 0:
            return (2,2)
    else:
        if cur_board[2][2] == 0:
            if valid_place_check(2, 2, cur_board, previous_board, player):
                return (2,2)

    # infinity = float('inf')
    alpha = float('-inf')
    beta = float('inf')

    score, best_state = max_alpha_beta(cur_board, previous_board, depth, player, alpha, beta)
    print("Sindhura : returned values ",best_state )
    if len(best_state) == 0:
        return 'PASS'
    return best_state

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
    action = alpha_beta_pruning(current_board, previous_board, 2, piece_type)
    print("Next move and stone type ", action, piece_type)
    writeOutput(action)
