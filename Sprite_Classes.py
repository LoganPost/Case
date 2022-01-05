import pygame as pg
from Matrix_Class import V, Matrix
movementSpeed=.1


def cast(X): #Turn the 3 vector into a 2 vector ... -ish
    return V((X[1],-X[2]))
def transform(P,X,zoom=1,shift=V((0,0))): #Transform the 3 vector into what goes on the screen
    return cast(P.apply(X)*zoom)+shift
def ftt(vec):
    return (V((vec[:3]))-(0.5,0.5,0.5))*(1+vec[3])


class Piece(pg.sprite.Sprite):
    def __init__(self,color,shape,rank):
        super().__init__()
        image=pg.image.load("Pieces/"+color+" "+shape+".png")
        self.image=pg.transform.rotozoom(image,0,80/(image.get_width()+image.get_height()))
        self.selected_image=pg.transform.rotozoom(image,0,100/(image.get_width()+image.get_height()))
        self.rect=self.image.get_rect(center=(300,300))
        self.selected_rect=self.selected_image.get_rect()
        self.pos2=V((0,0))
        self.pos3=V((0,0,0))
        self.pos4=V((0,0,0,0))
        self.color=color
        self.shape=shape
        self.rank=rank
        self.dimIndex=0
        self.selected=False
        self.destination=V((0,0,0))
        self.destinationDim="green"
        self.travelling=False
    def goto(self,board,pos4):
        # print("Our vector looks like THIS!: ",self.pos3)
        # print(self.dimIndex)
        self.destination=V(pos4)
        self.travelling=True
        board.setpos(self.pos4,-1)
        board.setpos(self.destination,self.rank)
        # board[self.pos3[0]][self.pos3[1]][self.pos3[2]][self.dimIndex] = 0
        # print("We're currently at: ",str(self.pos3),"in dimension ",str(self.dimIndex)," at ",str(self.dim))
        # print("Let's go to: ",str(vec)," in dimension ",str(dim))
         #board[vec[0]][vec[1]][vec[2]][dimIndex] = self
        # print("We're currently at: ",str(self.pos3),"in dimension ",str(self.dimIndex)," at ",str(self.dim))
        # print("Let's go to: ",str(self.destination)," in dimension ",str(dimIndex)," at ",str(self.destinationDim))
    def update(self,P,zoom,shift):
        if self.travelling:
            if abs(self.destination-self.pos4)>.01:
                self.pos4+=(self.destination-self.pos4).normalize()*movementSpeed
            else:
                self.pos4=self.destination
                self.travelling=False
        self.pos3=ftt(self.pos4)
        self.pos2=transform(P,self.pos3,zoom,shift)
    def telp(self,vec,board):
        board.setpos(self.pos4,-1)
        board.setpos(vec, self.rank)
        # board[self.pos3[0]][self.pos3[1]][self.pos3[2]][self.dimIndex] = 0
        self.pos4=vec
        self.pos3 = ftt(self.pos4)
    def __repr__(self):
        return str("{} {} with rank {}".format(self.color,self.shape,self.rank))
    def blit(self,screen):
        if self.selected:
            self.selected_rect.center=self.pos2
            screen.blit(self.selected_image, self.selected_rect)
        else:
            self.rect.center = self.pos2
            screen.blit(self.image, self.rect)
    def find_yourself(self,board):
        # print(len(board.all_spots()))
        for s in board.all_spots():
            # print(len())
            if board.get(s)==self.rank:
                # print(s)
                # print(self.pos4)
                self.destination = V(s)
                # print(self.destination!=self.pos4)
                self.travelling = True
    pass;
