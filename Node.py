from ChessImports import *
from Board import Board

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
    def __init__(self, parent, state, nodeLevel, nodeIndex):
        global INI_ID
        self.nId=INI_ID
        self.score=0
        self.count=0
        self.isLeaf=True
        self.isVisited=False
        self.parent=parent
        self.nodeLevel=nodeLevel
        self.nodeIndex=nodeIndex
        #chess details
        self.state=state
        self.children=[]
        self.isWin=False
        self.winColor=-1

        INI_ID += 1

    def show_node(self):
        if self.parent is None:
             print("""
        Node ID:    %s
        Score:      %s
        Count:      %s
        IsLeaf:     %s
        IsVisited:  %s
        Parent ID:  %s
        Node Level: %s
        Node Index: %s
        State:      %s
        IsWin:      %s
        Win Color:  %s
        """%(str(self.nId), str(self.score), str(self.count), str(self.isLeaf), str(self.isVisited), str("None"), str(self.nodeLevel), str(self.nodeIndex), str(self.state), str(self.isWin), str(self.winColor)))
        else: 
            print("""
        Node ID:    %s
        Score:      %s
        Count:      %s
        IsLeaf:     %s
        IsVisited:  %s
        Parent ID:  %s
        Node Level: %s
        Node Index: %s
        State:      %s
        IsWin:      %s
        Win Color:  %s
        """%(str(self.nId), str(self.score), str(self.count), str(self.isLeaf), str(self.isVisited), str(self.parent.nId), str(self.nodeLevel), str(self.nodeIndex), str(self.state), str(self.isWin), str(self.winColor)))

b=Board()
root=Node(None, b.board_fen(), 0, 0)
b.make_move("e2e4")

n=Node(root, b.board_fen(), 1, 0)
root.children.append(n)

root.show_node()
root.children[0].show_node()

