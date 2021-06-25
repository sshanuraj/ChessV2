import chess
import Board
from logger import log


"""
node:
    score
    count
    isLeaf bool
    isVisited bool
    parent = node above
    #Chess
        state = board
        children = []
        isWin bool acts as terminal node
        winColor = w/b/draw/NA -- > 1/2/0/-1
"""

INI_ID = 0 

class Node:
    def __init__(self, parent, state):
        global INI_ID
        self.nId=INI_ID
        self.score=0
        self.count=0
        self.isLeaf=True
        self.isVisited=False
        self.parent=parent
        #chess details
        self.state=state
        self.children=[]
        self.isWin=False
        self.winColor=-1

        INI_ID += 1

    def show_node(self):
        print("""
        Node ID:    %s
        Score:      %s
        Count:      %s
        IsLeaf:     %s
        IsVisited:  %s
        Parent ID:  %s
        State:      %s
        IsWin:      %s
        Win Color:  %s
        """%(str(self.nId), str(self.score), str(self.count), str(self.isLeaf), str(self.isVisited), str(self.parent.nId), str(self.state), str(self.isWin), str(self.winColor)))

