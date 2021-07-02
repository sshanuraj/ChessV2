from ChessImports import *
from ChessVars import *
from Node import Node
from Board import Board
from logger import log

"""
Selection-->Expansion-->Rollout/Simulation-->Backpropagation
"""

class MCTSAgent:
    def __init__(self, color):
        init_state='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.root=Node(-1, init_state, 0, 0, color)
        self.nodes={0:self.root}
        self.root.populate_node(self.nodes)
        self.color=color
        self.logger=log.Logger("CHESS_LOG.log")
        
    def terminal_reward(self, winColor):
        if winColor==DRAW:
            return 0
        if winColor!=self.color:
            return -10000
        else:
            return 10000

    def v_evaluate(self, vboard):
        w = 0
        b = 0
        dic = {1:1, 2:3, 3:3, 4:5, 5:9, 6:100}

        for i in range(64):
            if vboard.color_at(i) == True:
                w = w + dic[vboard.piece_type_at(i)]
            elif vboard.color_at(i) == False:
                b = b + dic[vboard.piece_type_at(i)]
        if self.color == WHITE:
            return w - b
        else:
            return b - w

    def get_numeric_pos(self, strpos):
        dict2 = {'a':1, 'b':2,'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8}
        n=int(strpos[1])
        return dict2[strpos[0]]*(n-1) + (n-1)

    def rollout(self, state):
        b=Board()
        vb=b.get_virtual_board(state)
        start=time.time()
        count=0
        dict1 = {None:0, 1:1, 2:3, 3:3, 4:5, 5:9, 6:100}
        opp_color = False if self.color==WHITE else True
        while True:
            vlm=b.get_virtual_move_str(vb)
            move=0
            l=len(vlm)
            flag=0
            max_move=-10000
            for i in range(l):
                loc1=self.get_numeric_pos(vlm[i][0:2])  #location where we wanna go
                loc2=self.get_numeric_pos(vlm[i][2:])  #location from where to move
                pt1=dict1[vb.piece_type_at(loc1)]  #piece to attack
                pt2=dict1[vb.piece_type_at(loc2)]  #my piece
                attack_=vb.is_attacked_by(opp_color, loc1)
                if pt1!=0 and pt2-pt1>0 and not attack_:
                    if max_move<pt2-pt1:
                        move=i
                        flag=1
                elif pt1!=0 and pt2-pt1<0:
                    if max_move<pt1-pt2:
                        move=i
                        flag=1
                elif pt1!=0 and pt2-pt1==0:
                    if max_move<0:
                        move=i; flag=1;
            if flag==0:
                move=rd.randint(0, l-1)
            vb_fen=b.make_virtual_move(vlm[move], vb) #get FEN rep of board
            vb=b.get_virtual_board(vb_fen)  #create virtual board through FEN 
            _, result=b.check_state_outcome(vb_fen) #check result of the move made
            if result==self.color:
                end=time.time()
                self.logger.log("LOG","Rollout took %s seconds, Result:[WIN] %s"%(str(end-start), str(self.color)))
                return 1
            if result==DRAW:
                end=time.time()
                self.logger.log("LOG","Rollout took %s seconds, Result:[DRAW]"%(str(end-start)))
                return 0
            if result==(3-self.color):
                end=time.time()
                self.logger.log("LOG","Rollout took %s seconds, Result:[LOSE] %s"%(str(end-start), str(self.color)))
                return -1
            count+=1
            if count==30:
                val=self.v_evaluate(vb)
                if val>0:
                    end=time.time()
                    self.logger.log("LOG","Rollout took %s seconds, Result:[WIN] %s"%(str(end-start), str(self.color)))
                    return 1
                elif val<0:
                    end=time.time()
                    self.logger.log("LOG","Rollout took %s seconds, Result:[LOSE] %s"%(str(end-start), str(self.color)))
                    return -1
                else:
                    end=time.time()
                    self.logger.log("LOG","Rollout took %s seconds, Result:[DRAW]"%(str(end-start)))
                    return 0

    def get_best(self, n_iterations, board, moves):
        cnode=self.root
        if moves!=[]:
            for mtuple in moves:
                if len(cnode.children)==0:
                    cnode.populate_node(self.nodes)
                cnode=self.nodes[cnode.children[mtuple[0]]]
        inode=cnode
        assert inode.state==board.board_fen() 
        count=0
        flag=True #represents if reset of cnode is reqd
        while count<n_iterations:
            if flag:
                cnode=inode
                self.logger.log("LOG", "Running iteration %s"%(count))
            if cnode==self.root:
                self.logger.log("LOG", "Finding Max UCB Node, initial search from root")
                _, cnode=cnode.max_ucb_node(self.root.visits, self.nodes)
                flag=False
                continue
            if cnode.visits==0:
                if cnode.isTerminal:
                    self.logger.log("LOG", "Found terminal node with Node ID: %s, Node Level: %s, Node Index: %s, Parent ID: %s"%
                        (str(cnode.nId),str(cnode.nodeLevel),str(cnode.nodeIndex), str(cnode.parent))) 
                    reward=self.terminal_reward(cnode.winColor)
                    cnode.backpropagate(reward, self.nodes)
                    count+=1
                    flag=True
                    continue

                self.logger.log("LOG", "Found unvisited node with Node ID: %s, Node Level: %s, Node Index: %s, Parent ID: %s"%
                    (str(cnode.nId), str(cnode.nodeLevel), str(cnode.nodeIndex), str(cnode.parent)))
                reward=self.rollout(cnode.state)
                cnode.backpropagate(reward, self.nodes)
                count+=1
                flag=True
                continue
            else:
                if cnode.isTerminal:
                    self.logger.log("LOG", "Found terminal node with Node ID: %s, Node Level: %s, Node Index: %s, Parent ID: %s"%
                        (str(cnode.nId),str(cnode.nodeLevel),str(cnode.nodeIndex), str(cnode.parent)))
                    reward=self.terminal_reward(cnode.winColor)
                    cnode.backpropagate(reward, self.nodes)
                    count+=1
                    flag=True
                    continue
                if len(cnode.children)==0:
                    cnode.populate_node(self.nodes)
                self.logger.log("LOG", "Finding Max UCB Node Final")
                _, cnode=cnode.max_ucb_node(self.root.visits, self.nodes)
                flag=False
        moveIndex, node=inode.max_ucb_node(self.root.visits, self.nodes)
        inode.nIdOfMove=node.nId
        return moveIndex

