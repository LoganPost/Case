import pygame as pg
from Matrix_Class import V, Matrix
movementSpeed=.1
class Piece(pg.sprite.Sprite):
    def __init__(self,color,shape,rank):
        super().__init__()
        self.image=pg.image.load("Pieces/"+color+" "+shape+".png")
        self.image=pg.transform.rotozoom(self.image,0,80/(self.image.get_width()+self.image.get_height()))
        self.rect=self.image.get_rect(center=(300,300))
        self.pos3=V((0,0,0))
        self.dim=1
        self.color=color
        self.shape=shape
        self.rank=rank
        self.dimIndex=0
        self.selected=False
        self.destination=V((0,0,0))
        self.destinationDim="green"
        self.travelling=False
    def goto(self,vec,dimIndex,dim,board):
        print("Our vector looks like THIS!: ",self.pos3)
        print(self.dimIndex)
        board[self.pos3[0]][self.pos3[1]][self.pos3[2]][self.dimIndex] = 0
        print("We're currently at: ",str(self.pos3),"in dimension ",str(self.dimIndex)," at ",str(self.dim))
        print("Let's go to: ",str(vec)," in dimension ",str(dim))
        if vec!=self.pos3 or self.dim!=dim:
            self.travelling=True
            self.destination=V(vec)
            self.dimIndex=dimIndex
            self.destinationDim=dim
            print("This worked")
        board[vec[0]][vec[1]][vec[2]][dimIndex] = self
        print("We're currently at: ",str(self.pos3),"in dimension ",str(self.dimIndex)," at ",str(self.dim))
        print("Let's go to: ",str(self.destination)," in dimension ",str(dimIndex)," at ",str(self.destinationDim))
    def update(self):
        if self.travelling:
            if abs(self.destination-self.pos3)>.01 or abs(self.dim-self.destinationDim)>.01:
                self.pos3+=(self.destination-self.pos3).normalize()*movementSpeed
                if self.destinationDim>self.dim:
                    self.dim+=0.5*movementSpeed
                elif self.destinationDim<self.dim:
                    self.dim-=0.5*movementSpeed
            else:
                self.pos3=self.destination
                self.dim=self.destinationDim
                self.travelling=False
    def telp(self,vec,dimIndex,dim,board):
        board[self.pos3[0]][self.pos3[1]][self.pos3[2]][self.dimIndex] = 0
        self.pos3=vec
        self.dim=dim
        self.dimIndex=dimIndex
        board[vec[0]][vec[1]][vec[2]][dimIndex] = self
    def __repr__(self):
        return str(self.rank)
    pass;
