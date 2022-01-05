from Matrix_Class import Matrix,V

def nothing(vec):
    for i,xi in enumerate(vec):
        if xi==1:
            yield V((*vec[0:i],0,*vec[i+1:]))
        else:
            yield V((*vec[0:i],1,*vec[i+1:]))
def getAdjacent(vec):
    a,b,c,d=vec
    return (a,b,c,(d+1)%2),(a,b,(c+1)%2,d),(a,(b+1)%2,c,d),((a+1)%2,b,c,d)
class Board(list):
    def place(self,pos,rank):
        newBoard=self.copy()
        newBoard[pos[0]][pos[1]][pos[2]][pos[3]]=rank
        return newBoard
    def copy(self):
        return Board([[[[lay for lay in dim] for dim in col]for col in row] for row in self])
    def get(self,pos):
        return self[pos[0]][pos[1]][pos[2]][pos[3]]
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
    def legalMoves(self,order,pos):
        print("there are legal moves for {} and here they are".format(pos))
        for i in getAdjacent(pos):
            if self.isLegal(order,i):
                yield i
    def isLegal(self,order,pos):
        val=self.get(pos)
        return val in (-1,order-1,order+5)
    def setpos(self,pos,value):
        self[pos[0]][pos[1]][pos[2]][pos[3]]=value
    def all_spots(self):
        return [(i,j,k,l) for i,a in enumerate(self) for j,b in enumerate(a) for k,c in enumerate(b) for l,d in enumerate(c)]




def newBoard():
    return Board([[[[-1,-1],[-1,-1]],[[-1,-1],[-1,-1]]],[[[-1,-1],[-1,-1]],[[-1,-1],[-1,-1]]]])