import pygame as pg
from Matrix_Class import V, Matrix
from math import sin, cos,pi
movementSpeed=.1


def cast(X): #Turn the 3 vector into a 2 vector ... -ish
    return V((X[1],-X[2]))
def transform(P,X,zoom=1,shift=V((0,0))): #Transform the 3 vector into what goes on the screen
    return cast(P.apply(X)*zoom)+shift
def ftt(vec):
    if rotating:
        ht=hyper_theta*pi/180
        htt=(1-cos(ht))*pi/2
        sht=(vec[3]*2-1)*sin(ht)/5
        vec=(vec[0],vec[1],vec[2]+sht,((vec[3]*2-1)*cos(htt)+1)/2)
    elif rotating:
        ht=hyper_theta*pi/180
        vec=(vec[0],vec[1],vec[2]+(vec[3]*2-1)*sin(ht)/3,((vec[3]*2-1)*cos(ht)+1)/2)
    elif hyper_theta:
        vec=(vec[0],vec[1],vec[2],1-vec[3])

    # ht=hyper_theta*pi/180
    # vec=(vec[0],vec[1],vec[2]+(vec[3]*2-1)*sin(ht)/3,((vec[3]*2-1)*cos(ht)+1)/2)
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
        self.destination=self.pos4
        self.destinationDim="green"
        self.travelling=False
    def goto(self,board,pos4):
        self.destination=V(pos4)
        self.travelling=True
        board.setpos(self.pos4,-1)
        board.setpos(self.destination,self.rank)
    def update(self,P,zoom,shift,hpt,rtt):
        if self.travelling:
            if abs(self.destination-self.pos4)>movementSpeed:
                self.pos4+=(self.destination-self.pos4).normalize()*movementSpeed
            else:
                self.pos4=self.destination
                self.travelling=False
        global hyper_theta,rotating
        hyper_theta,rotating=(hpt,rtt)
        self.pos3=ftt(self.pos4)
        self.pos2=transform(P,self.pos3,zoom,shift)
    def telp(self,board,vec):
        board.setpos(self.pos4,-1)
        board.setpos(vec, self.rank)
        self.pos4=vec
        self.destination=vec
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
    def order(self):
        return self.ORDER+.02
    pass;
