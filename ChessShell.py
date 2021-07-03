from Node import Node
from ChessVars import *
import chess
import dill

f=open("ChessNodesW.obj", "rb")
g=open("ChessNodesB.obj", "rb")

chessNodesWhite=dill.load(f)
chessNodesBlack=dill.load(g)

f.close()
g.close()

def show_node(color, nId):
    node=None
    if color==WHITE:
        if nId not in chessNodesWhite.keys():
            print("No such ID exists in White MCTS Tree")
            return None
        else:
            node=chessNodesWhite[nId]
            print("White Player Node")
    if color==BLACK:
        if nId not in chessNodesBlack.keys():
            print("No such ID exists in Black MCTS Tree")
            return None
        else:
            node=chessNodesBlack[nId]
            print("Black Player Node")
    nIdOfMove = "None" if node.nIdOfMove==None else str(node.nIdOfMove)
    print("""
Node ID:         %s
Score:           %s
Visits:          %s
IsLeaf:          %s
Parent ID:       %s
Node Level:      %s
Node Index:      %s
Root Color:      %s
State:           %s
Node Id of Move: %s
IsTerminal:      %s
Win Color:       %s
"""%(str(node.nId), str(node.score), str(node.visits), str(node.isLeaf),
str(node.parent), str(node.nodeLevel), str(node.nodeIndex), str(node.rootColor), str(node.state),
nIdOfMove, str(node.isTerminal), str(node.winColor)))

    if len(node.children)!=0:
        print("Children Node IDs:")
        l=len(node.children)
        for i in range(l):
            print(node.children[i], end=' ')
        print()
        print()
    else:
        print("No children for this node")
        print()
    
    board=chess.Board(str(node.state))
    print("Board Representation:")
    print(board)

def traverse_up(up, last_nId, last_color):
    if last_color==NA:
        print("No previous ID was encountered.")
        return None
    count=0
    nId=last_nId
    while up>count:
        if last_color==WHITE:
            nId=chessNodesWhite[nId].parent
            print("Going up to Node Id: %d"%(nId))
        else:
            nId=chessNodesBlack[nId].parent
            print("Going up to Node Id: %d"%(nId))
        if nId==-1:
            print("Found root..Ending traversal.")
            break
        count+=1
    if nId==-1:
        show_node(last_color, 0)
    else:
        show_node(last_color, nId)
    return nId

def traverse_down(down, last_nId, last_color):
    if last_color==NA:
        print("No previous ID encountered.")
        return last_nId
    count=0
    nId=last_nId
    while down>count:
        if last_color==WHITE:
            if chessNodesW[nId].isTerminal:
                print("Encountered node is terminal..ending traversal")
                show_node(last_color, nId)
                return nId
            else:
                count+=1
                if chessNodesW[nId].nIdOfMove!=None:
                    print("Going down")
                    nId=chessNodesW[nId].nIdOfMove
                else:
                    print("No next move found, returning current node")
                    show_node(last_color, nId)
                    return nId
        else:
            if chessNodesB[nId].isTerminal:
                print("Encountered node is terminal..ending traversal")
                show_node(last_color, nId)
                return nId
            else:
                count+=1
                if chessNodesB[nId].nIdOfMove!=None:
                    print("Going down")
                    nId=chessNodesB[nId].nIdOfMove
                else:
                    print("No next move found, returning current node")
                    show_node(last_color, nId)
                    return nId
    show_node(last_color, nId)
    return nId
            
#----------------------------------------------------------------------------------------

query=""
print("""
---Welcome to ChessShell, 2021 sshanuraj---
Explore nodes of the most recently played game..
Commands to start of with:
    wnode [Node ID] - Explore a white node with some Node ID
    bnode [Node ID] - Explore a black node with some Node ID
    up [int]        - Go up moves from last searched node
    down [int]      - Go down moves from last searched node
    exit - Exit from command line
""".strip())

commands={"help":1, "wnode":2, "bnode":3, "up":4, "down":5, "exit":6}
last_nId=-1
last_color=NA

while True:
    query=input(">>> ")
    query=query.strip()
    qsplit=query.split(' ')
    main_query=qsplit[0]
    
    if main_query in commands.keys() and main_query!="exit":
        try:
            if main_query=="wnode" or main_query=="Wnode":
                nId=int(qsplit[1])
                show_node(WHITE, nId)
                last_nId=nId
                last_color=WHITE
            elif main_query=="bnode":
                nId=int(qsplit[1])
                show_node(BLACK, nId)
                last_nId=nId
                last_color=BLACK
            elif main_query=="up":
                if last_nId==-1:
                    print("No previous ID encountered")
                else:
                    up=int(qsplit[1])
                    last_nId=traverse_up(up, last_nId, last_color)
            elif main_query=="down":
                down=int(qsplit[1])
                last_nId=traverse_down(down, last_nId, last_color)
                    
        except:
            print("ID should be numeric. In Except")
    elif main_query=="exit":
        break
    else:
        print("Wrong command")

