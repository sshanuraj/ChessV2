from Board import Board
from MCTS import MCTSAgent
from ChessVars import *
from ChessImports import *
from logger import log
from Node import Node, store_ids
import dill

f=open("ChessNodesW.obj", "rb")
g=open("ChessNodesB.obj", "rb")

class Chess:
    def __init__(self):
        self.board=Board()
        self.logger=log.Logger("CHESS_LOG.log")

    def check_result(self):
        return self.board.check_outcome()

    def play(self, w, b, n):
        self.logger.log("LOG", "-----------------NEW MCTS ITERATION-----------------")
        for i in range(n):
            self.logger.log("LOG", "----------------Game %s----------------"%(str(i)))
            moves=[]
            n_iterations=1000
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
                print()
                #self.logger.log("LOG", "Board FEN after move %s: %s"%(str(count), self.board.board_fen()))
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
                print()
                #self.logger.log("LOG", "Board FEN after move %s: %s"%(str(count), self.board.board_fen()))
                #self.logger.log("LOG", "Moves played till now: %s"%(str(moves)))
                if result==DRAW:
                    print("Draw")
                    break
                if result==BLACK:
                    print("Black wins")
                    break
                count+=1
            self.logger.log("LOG", "-----------------Game %s Ends----------------"%(str(i)))

chess=Chess()
w=dill.load(f)
b=dill.load(g)
f.close()
g.close()
"""
w=MCTSAgent(WHITE)
b=MCTSAgent(BLACK)

w.nodes=chessNodesW
b.nodes=chessNodesB
"""
chess.play(w, b, 1)
f=open("ChessNodesW.obj", "wb")
g=open("ChessNodesB.obj", "wb")
dill.dump(w, f)
dill.dump(b, g)
f.close()
g.close()
store_ids()

