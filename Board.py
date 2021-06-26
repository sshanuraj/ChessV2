from ChessImports import *
from ChessVars import *

class Board:
    def __init__(self):
        self.board = chess.Board()

    def make_move(self, move):
        self.board.push(chess.Move.from_uci(move))

    def is_checkmate(self):
        return self.board.is_checkmate()

    def is_draw(self):
        if self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_fivefold_repetition() or self.board.is_seventyfive_moves():
            return True
        return False
    
    def check_outcome(self):
        oc=self.board.outcome()
        if oc is None:
            return NA
        if oc.result()=="1-0":
            return WHITE
        elif oc.result()=="0-1":
            return BLACK
        else:
            return DRAW
        return DRAW

    def generate_moves(self):
        return self.board.legal_moves

    def generate_move_str(self):
        moves=[]
        lm=self.generate_moves()
        for move in lm:
            moves.append(str(move))
        return moves

    def print_board(self):
        print(self.board)

    def un_move(self):
        self.board.pop()

    def reset(self):
        self.board.reset()

    def board_fen(self):
        return self.board.fen()

    def get_virtual_board(self, state):
        return chess.Board(state)

    def turn_virtual(self, vboard):
        return vboard.turn

    def get_virtual_move_str(self, vboard):
        moves=[]
        vlm=vboard.legal_moves
        for move in vlm:
            moves.append(str(move))
        return moves

    def make_virtual_move(self, move, vboard):
        vboard.push(chess.Move.from_uci(move))
        vb_fen=vboard.fen()
        vboard.pop()
        return vb_fen

    def turn(self):
        return self.board.turn

    def check_state_outcome(self, random_state):
        boardNew=chess.Board(str(random_state))
        outcome=boardNew.outcome()
        if outcome is None:
            return False, NA
        oc_str=outcome.result()
        if oc_str=='1-0':
            return True, WHITE
        elif oc_str=='0-1':
            return True, BLACK
        else:
            return True, DRAW
