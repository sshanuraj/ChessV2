from Board import Board
from MCTS import MCTSAgent
from ChessVars import *
from ChessImports import *

class Chess:
    def __init__(self):
        self.board=Board()

    def check_result(self):
        return self.board.check_outcome()

    def play(self, w, b, n):
        for i in range(n):
            moves=[]
            n_iterations=1000
            self.board.reset()
            while True:
                #white generates move
                moveIndex=w.get_best(n_iterations, self.board, moves)
                move=self.board.generate_move_str()[moveIndex]
                self.board.make_move(move)
                moves.append([moveIndex, move])
                result=self.check_result()
                self.board.print_board()
                if result==DRAW:
                    print("Draw")
                    break
                if result==WHITE:
                    print("White wins")
                    break

                #black generates move
                moveIndex=b.get_best(n_iterations, self.board, moves)
                move=self.board.generate_move_str()[moveIndex]
                self.board.make_move(move)
                moves.append([moveIndex, move])
                result=self.check_result()
                self.board.print_board()
                if result==DRAW:
                    print("Draw")
                    break
                if result==BLACK:
                    print("Black wins")
                    break

chess=Chess()
chess.play(MCTSAgent(WHITE), MCTSAgent(BLACK), 2)


