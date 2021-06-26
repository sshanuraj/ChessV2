from Board import Board
from MCTS import MCTS
from ChessVars include *
from ChessImports include *

class Chess:
    def __init__(self):
        self.board=Board()

    def check_result(self):
        return self.board.check_outcome()

    def play(self, w, b, n):
        for i in range(n):
            moves=[]
            n_iterations=10
            while True:
                #white generates move
                move=w.get_best(n_iterations, self.board, moves)
                self.board.make_move(move)
                actions.append(move)
                result=self.check_result()
                if result==DRAW:
                    print("Draw")
                    break
                if result==WHITE:
                    print("White wins")
                    break

                #black generates move
                move=b.get_best(n_iterations, self.board, moves)
                self.board.make_move(move)
                actions.append(move)
                result=self.check_result()
                if result==DRAW:
                    print("Draw")
                    break
                if result==BLACK:
                    print("Black wins")
                    break

