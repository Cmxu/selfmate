import chess
import time
import pickle

board = chess.Board('R5B1/3p2P1/8/4P3/rp6/bp6/br3N2/RNk1K1BQ w - - 0 1')
#board = chess.Board('k7/1p1R4/8/7Q/4N3/8/2p5/K1N4R w - - 0 1')
#board = chess.Board('2B5/p2Q4/1P6/2P5/3P2n1/4P1Pk/5Pp1/6K1 w - - 0 1')
#board = chess.Board('8/2p5/6pp/2R3pk/2R5/2P3PK/6PP/8 w - - 0 1')
board = chess.Board('8/8/1Q6/8/1p6/k1N5/p1B5/K7 w - - 0 1')
num_moves = 4
stor = {}
#with open('sm_stor.pickle', 'rb') as f:
#    stor = pickle.load(f)

def find_forcing_moves(fen, move_list, thres = 3):
    forcing_moves = []
    for move in move_list:
        board = chess.Board(fen)
        board.push(move)
        if len(list(board.legal_moves)) < thres:
            forcing_moves.append(move)
    return forcing_moves

def find_selfmate(board, moves_left, my_move = True, current_moves = []):
    if moves_left == 0:
        return board.is_checkmate(), [['over']]
    copied_board = board.fen()
    if copied_board in stor:
        return stor[copied_board]
    move_lists = []
    best_result = not my_move
    poss_moves = list(board.legal_moves)
    if my_move:
        if moves_left > 10:
            poss_moves = find_forcing_moves(copied_board, poss_moves, thres = 4) # 4
        else:
            poss_moves = find_forcing_moves(copied_board, poss_moves, thres = 5) #5
    for move in poss_moves:
        if moves_left == num_moves:
            print(move)
        board = chess.Board(copied_board)
        board.push(move)
        if board.is_checkmate():
            result, moves = not my_move, [[my_move]]
        else:
            current_moves.append(move)
            result, moves = find_selfmate(chess.Board(board.fen()), moves_left -1, not my_move, current_moves)
            current_moves = current_moves[:-1]
        if my_move:
            if result:
                return True, [move, moves]
                best_result = my_move
                move_lists.append([move, moves])
        else:
            if result:
                move_lists.append([move, moves])
            else:
                stor[copied_board] = (False, [['dead_end']])
                if len(stor) % 100000 == 0:
                    print('Explored {} Positions'.format(len(stor)))
                return False, [['dead_end']]
    if not move_lists:
        stor[copied_board] = (False, [])
        if len(stor) % 100000 == 0:
            print('Explored {} Positions'.format(len(stor)))
        return False, []
    else:
        if best_result:
            print(current_moves)
        stor[copied_board] = (best_result, move_lists)
        if len(stor) % 100000 == 0:
            print('Explored {} Positions'.format(len(stor)))
        return best_result, move_lists

start = time.time()
a, b = find_selfmate(board, moves_left = num_moves)
print(time.time() - start)
