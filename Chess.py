from Board import Board
from MCTS import MCTSAgent
from ChessVars import *
from ChessImports import *
from logger import log

class Chess:
    def __init__(self):
        self.board=Board()
        self.logger=log.Logger("CHESS_LOG.log")

    def check_result(self):
        return self.board.check_outcome()

    def play(self, w, b, n):
        self.logger.log("LOG", "-----------------NEW MCTS ITERATION-----------------")
        for i in range(n):
            moves=[]
            n_iterations=10
            self.board.reset()
            count=1
            while True:
                #white generates move
                self.logger.log("LOG", "------------White deciding move--------------")
                moveIndex=w.get_best(n_iterations, self.board, moves)
                move=self.board.generate_move_str()[moveIndex]
                self.logger.log("LOG", "------------White selected move: %s, moveIndex: %s------------"%(move, str(moveIndex)))
                self.board.make_move(move)
                moves.append([moveIndex, move])
                result=self.check_result()
                self.board.print_board()
                self.logger.log("LOG", "Board FEN after move %s: %s"%(str(count), self.board.board_fen()))
                if result==DRAW:
                    print("Draw")
                    break
                if result==WHITE:
                    print("White wins")
                    break

                #black generates move
                self.logger.log("LOG", "-------------Black deciding move--------------")
                moveIndex=b.get_best(n_iterations, self.board, moves)
                move=self.board.generate_move_str()[moveIndex]
                self.logger.log("LOG", "-------------Black selected move: %s, moveIndex: %s-------------"%(move, str(moveIndex)))
                self.board.make_move(move)
                moves.append([moveIndex, move])
                result=self.check_result()
                self.board.print_board()
                self.logger.log("LOG", "Board FEN after move %s: %s"%(str(count), self.board.board_fen()))
                if result==DRAW:
                    print("Draw")
                    break
                if result==BLACK:
                    print("Black wins")
                    break
                count+=1

chess=Chess()
chess.play(MCTSAgent(WHITE), MCTSAgent(BLACK), 1)


