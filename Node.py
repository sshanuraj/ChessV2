from ChessImports import *
from ChessVars import *
from Board import Board

"""
node:
    score
    count
    isLeaf bool
    isVisited bool
    parent = node above
    nodeLevel = level of mcts tree
    nodeIndex = index in the current level
    #Chess
        state = board
        children = []
        isWin bool acts as terminal node
        winColor = w/b/draw/NA -- > 1/2/0/-1
"""
INF=100000000
INI_ID = 0 

class Node:
    def __init__(self, parent, state, nodeLevel, nodeIndex):
        global INI_ID
        self.nId=INI_ID
        self.score=0
        self.visits=0
        self.isLeaf=True
        self.parent=parent
        self.nodeLevel=nodeLevel
        self.nodeIndex=nodeIndex
        #chess details
        self.state=state
        self.children=[]
        self.isTerminal, self.winColor= Board().check_state_outcome(self.state) 

        INI_ID += 1
    
    def show_node(self):
        if self.parent is None:
             print("""
        Node ID:    %s
        Score:      %s
        Visits:     %s
        IsLeaf:     %s
        Parent ID:  %s
        Node Level: %s
        Node Index: %s
        State:      %s
        IsTerminal: %s
        Win Color:  %s
        """%(str(self.nId), str(self.score), str(self.visits), str(self.isLeaf), str("None"), str(self.nodeLevel), str(self.nodeIndex), str(self.state), str(self.isTerminal), str(self.winColor)))
        else: 
            print("""
        Node ID:    %s
        Score:      %s
        Visits:     %s
        IsLeaf:     %s
        Parent ID:  %s
        Node Level: %s
        Node Index: %s
        State:      %s
        IsTerminal: %s
        Win Color:  %s
        """%(str(self.nId), str(self.score), str(self.visits), str(self.isLeaf), str(self.parent.nId), str(self.nodeLevel), str(self.nodeIndex), str(self.state), str(self.isTerminal), str(self.winColor)))
    
    def calculate_ucb(self, N):
        if self.visits==0:
            return INF
        return (self.score/self.visits) + (2*np.log(N)/self.visits)**0.5

    def max_ucb_node(self, N):
        max_ind=[]
        max_val=-100
        l=len(self.children)

        if l==0:
            return None

        for i in range(l):
            val=self.calculate_ucb(N)
            if val>max_val:
                max_ind=[]
                max_ind.append(i)
                max_val=val
            elif val==max_val:
                max_ind.append(i)

        l1=len(max_ind)
        if l1==1:
            return self.children[max_ind[0]]
        maxInd=rd.randint(0,l1-1)
        return self.children[maxInd]

    def populate_node(self):
        if self.isTerminal:
            return False
        curr_state=self.state
        b=Board()
        vb=b.get_virtual_board(curr_state)
        lm=b.get_virtual_move_str(vb)
        l=len(lm)
        for i in range(l):
            move=lm[i]
            afterMoveState=b.make_virtual_move(move, vb)
            self.children.append(Node(self, afterMoveState, self.nodeLevel+1, i))

b=Board()
root=Node(None, b.board_fen(), 0, 0)
root.populate_node()
root.children[0].populate_node()
for i in root.children[0].children:
    i.show_node()
