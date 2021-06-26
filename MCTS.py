from ChessImports import *
from ChessVars import *
from Node import Node
from Board import Board

"""
Selection-->Expansion-->Rollout/Simulation-->Backpropagation
"""

class MCTSAgent:
    def __init__(self, color):
        init_state='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.root=Node(None, init_state, 0, 0)
        self.root.populate_node()
        self.color=color

    def terminal_reward(self, winColor):
        if winColor==DRAW:
            return 0
        if winColor!=self.color:
            return -10000
        else:
            return 10000

    def rollout(self, state):
        b=Board()
        vb=b.get_virtual_board(state)
        while True:
            vlm=b.get_virtual_move_str(vb)
            move=rd.randint(0,len(vlm)-1)
            vb_fen=b.make_virtual_move(vlm[move], vb) #get FEN rep of board
            vb=b.get_virtual_board(vb_fen)  #create virtual board through FEN 
            _, result=b.check_state_outcome(vb_fen) #check result of the move made
            if result==self.color:
                return 1
            if result==DRAW:
                return 0
            if result==(3-self.color):
                return -1


    def get_best(self, n_iterations, board, moves):
        cnode=self.root
        if moves!=[]:
            for mtuple in moves:
                if len(cnode.children)==0:
                    cnode.populate_node()
                cnode=cnode.children[mtuple[0]]
        inode=cnode
        count=0
        flag=True #represents if reset of cnode is reqd
        while count<n_iterations:
            if flag:
                cnode=inode
            if cnode==self.root:
                _, cnode=cnode.max_ucb_node(self.root.visits)
                flag=False
                continue
            if cnode.isLeaf:
                if cnode.isTerminal:
                    reward=self.terminal_reward(cnode.winColor)
                    cnode.backpropagate(reward)
                    count+=1
                    flag=True
                    continue
                reward=self.rollout(cnode.state)
                cnode.backpropagate(reward)
                count+=1
                flag=True
                continue
            else:
                if cnode.isTerminal:
                    if cnode.isTerminal:
                        reward=self.terminal_reward(cnode.winColor)
                        cnode.backpropagate(reward)
                        count+=1
                        flag=True
                        continue
                if len(cnode.children)==0:
                    cnode.populate_node()
                _, cnode=cnode.max_ucb_node(self.root.visits)
                flag=False
        moveIndex, node=inode.max_ucb_node(self.root.visits)
        return moveIndex

