from ChessImports import *
from ChessVars import *
from Board import Board
from logger import log

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
INI_ID_W = 0
INI_ID_B = 0 



class Node:
    def __init__(self, parent, state, nodeLevel, nodeIndex, color):
        global INI_ID_W
        global INI_ID_B
        self.nId=None
        self.score=0
        self.visits=0
        self.isLeaf=True
        self.parent=parent
        self.nodeLevel=nodeLevel
        self.nodeIndex=nodeIndex
        self.rootColor=color
        self.state=state
        self.children=[]
        self.nIdOfMove=None
        self.isTerminal, self.winColor=Board().check_state_outcome(self.state) 
        if color==WHITE:
            self.nId=INI_ID_W
            INI_ID_W+= 1
        else:
            self.nId=INI_ID_B
            INI_ID_B+=1
        self.logger=log.Logger("CHESS_LOG.log")
    
    def show_node(self):
        print("""
    Node ID:    %s
    Score:      %s
    Visits:     %s
    IsLeaf:     %s
    Parent ID:  %s
    Node Level: %s
    Node Index: %s
    Root Color: %s
    State:      %s
    IsTerminal: %s
    Win Color:  %s
    """%(str(self.nId), str(self.score), str(self.visits), str(self.isLeaf),
     str(self.parent.nId), str(self.nodeLevel), str(self.nodeIndex), str(self.rootColor),
      str(self.state), str(self.isTerminal), str(self.winColor)))
   
    def get_parent_details(self):
        if self.parent==None:
            return None, None
        return self.parent, self.parent.nId
    
    def backpropagate(self, reward, nodes_dict):
        self.score+=reward
        self.visits+=1
        self.isLeaf=False
        par=nodes_dict[self.parent]
        while par!=-1:
            par.score+=reward
            par.visits+=1
            if par.parent==-1:
                break
            par=nodes_dict[par.parent]

    def calculate_ucb(self, N):
        if self.visits==0:
            return INF
        return (self.score/self.visits) + (2*np.log(N)/self.visits)**0.5

    def max_ucb_node(self, N, nodes_dict):
        max_ind=[]
        max_val=-100000000000000000000000
        l=len(self.children)

        if l==0:
            return None

        for i in range(l):
            node=nodes_dict[self.children[i]]
            val=node.calculate_ucb(N)
            if val>max_val:
                max_ind=[]
                max_ind.append(i)
                max_val=val
            elif val==max_val:
                max_ind.append(i)

        l1=len(max_ind)

        if l1==0:
            print("Woops")

        maxInd=rd.randint(0,l1-1)
        global logger
        self.logger.log("LOG", "Returning Max UCB Node ID: %s"%(str(nodes_dict[self.children[maxInd]].nId)))
        return maxInd, nodes_dict[self.children[maxInd]]

    def populate_node(self, nodes_dict):
        if self.isTerminal:
            return False
        self.isLeaf=False
        curr_state=self.state
        b=Board()
        vb=b.get_virtual_board(curr_state)
        lm=b.get_virtual_move_str(vb)
        l=len(lm)
        for i in range(l):
            move=lm[i]
            afterMoveState=b.make_virtual_move(move, vb)
            node=Node(self.nId, str(afterMoveState), self.nodeLevel+1, i, self.rootColor)
            nodes_dict[node.nId]=node
            self.children.append(node.nId)
