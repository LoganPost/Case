from Matrix_Class import Matrix,V

def getAdjacent(vec):
    for i,xi in enumerate(vec):
        if xi==1:
            yield V((*vec[0:i],0,*vec[i+1:]))
        else:
            yield V((*vec[0:i],1,*vec[i+1:]))
class Board(list):
    def place(self,pos,dimIndex,turn):
        newBoard=Board([[[[i for i in dim] for dim in col]for col in row] for row in self])
        newBoard[pos[0]][pos[1]][pos[2]][dimIndex]=turn
        return newBoard
    def spot(self,pos,dimIndex):
        return self[pos[0]][pos[1]][pos[2]][dimIndex]
    def inverted(self):
        return Board([[[[-i for i in dim] for dim in col]for col in row] for row in self])
    def sps(self):
        for dim in self:
            for r,row in enumerate(dim):
                out=""
                for c,col in enumerate(row):
                    out+="["
                    first=True
                    for e,el in enumerate(col):
                        if not first:
                            out+=" "
                        else:
                            first=False
                        out+=str(el)
                        for i in range(max([len(str(dim[i][c][e])) for i in range(len(dim))])-len(str(el))):
                            out+=" "
                    out+="]   "
                print(out)
            print()
        return
    def legalMoves(self,order,pos, dimIndex):
        for i in getAdjacent(pos):
            if self.isLegal(order,i,dimIndex):
                yield i, dimIndex
        print("made it here")
        if self.isLegal(order, pos, (dimIndex+1)%2):
            print("also made it here")
            yield pos, (dimIndex+1)%2
    def isLegal(self,order,pos,dimIndex):
        return isinstance(self.spot(pos,dimIndex),int) or self.spot(pos,dimIndex).rank==order-1 or self.spot(pos,dimIndex).rank==order+5



def newBoard():
    return Board([[[[0,0],[0,0]],[[0,0],[0,0]]],[[[0,0],[0,0]],[[0,0],[0,0]]]])