from ChessImports import *

class Board:
    def __init__(self):
        self.board = chess.Board()

    def make_move(self, move):
        self.board.Move.from_uci(move)

    def is_checkmate(self):
        return self.board.is_checkmate()

    def is_draw(self):
        if self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_fivefold_repetition() or self.board.is_seventyfive_moves():
            return True
        return False

    def generate_moves(self):
        return self.board.legal_moves

    def generete_move_str(self):
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
