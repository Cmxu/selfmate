import chess
import time
import pickle

board = chess.Board('R5B1/3p2P1/8/4P3/rp6/bp6/br3N2/RNk1K1BQ w - - 0 1') # 18
#board = chess.Board('k7/1p1R4/8/7Q/4N3/8/2p5/K1N4R w - - 0 1') # 20
#board = chess.Board('2B5/p2Q4/1P6/2P5/3P2n1/4P1Pk/5Pp1/6K1 w - - 0 1') # 10
#board = chess.Board('8/2p5/6pp/2R3pk/2R5/2P3PK/6PP/8 w - - 0 1') # 6
#board = chess.Board('8/8/1Q6/8/1p6/k1N5/p1B5/K7 w - - 0 1') # 4
num_moves = 18
stor = {}

def find_forcing_moves(fen, move_list, thres = 2):
    forcing_moves = []
    for move in move_list:
        board = chess.Board(fen)
        board.push(move)
        if len(list(board.legal_moves)) <= thres:
            forcing_moves.append(move)
    return forcing_moves

def find_selfmate(board, moves_left, my_move = True, current_moves = []):
    board_fen = board.fen()
    if board_fen in stor:
        return stor[board_fen]
    if moves_left == 0:
        if board.is_checkmate():
            stor[board_fen] = True, ['Forced Mate!']
            return True, ['Forced Mate!']
        else:
            stor[board_fen] = False, ['No More Moves']
            return False, ['No More Moves']
    if board.is_checkmate():
        stor[board_fen] = my_move, ['Mate!']
        return my_move, ['Mate!']
    possible_moves = list(board.legal_moves)
    if my_move:
        possible_moves = find_forcing_moves(board_fen, possible_moves, thres = 5)
    all_moves = []
    for move in possible_moves:
        board.push(move)
        #current_moves.append(move)
        result, move_list = find_selfmate(board, moves_left - 1, not my_move)#, current_moves)
        #current_moves = current_moves[:-1]
        assert move == board.pop()
        if my_move and result:
            stor[board_fen] = True, [move, move_list]
            return True, [move, move_list]#[current_moves, move_list]
        if not my_move and not result:
            stor[board_fen] = False, ['Dead End']
            return False, ['Dead End']
        all_moves.append([move, move_list])
    if not all_moves:
        stor[board_fen] = False, ['Dead End']
        return False, ['Dead End']
    if my_move:
        stor[board_fen] = False, ['Dead End']
        return False, ['Dead End']
    else:
        stor[board_fen] = True, all_moves
        return True, all_moves#[current_moves, all_moves]

start = time.time()
a,b = find_selfmate(board, moves_left = num_moves)
print('Time Taken: {}'.format(time.time() - start))
