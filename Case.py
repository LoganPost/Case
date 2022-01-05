import pygame as pg
from sys import exit
from Matrix_Class import Matrix,V
from math import sin, cos
from Case_Board import Board,newBoard
from Sprite_Classes import Piece
import time
B=newBoard()
memory=[]
B.sps()
def getAdjacent(vec):
    for i,xi in enumerate(vec):
        if xi==1:
            yield tuple(vec[0:i]+[0]+vec[i+1:])
        else:
            yield tuple(vec[0:i] + [0] + vec[i + 1:])
def r(Orientation,dX):
    dx,dy=dX
    cdx,sdx,cdy,sdy=cos(dx),sin(dx),cos(dy),sin(dy)
    roth = Matrix([[cdx, sdx, 0], [-sdx, cdx, 0], [0, 0, 1]])
    rotv = Matrix([[cdy, 0, sdy], [0, 1, 0], [-sdy, 0, cdy]])
    rot = roth*rotv
    return rot*Orientation
def cast(X):
    return V((X[1],-X[2]))
def transform(P,X,zoom=1,shift=V((0,0))):
    return cast(P.apply(X)*zoom)+shift
class Line():
    def __init__(self,start, end,color=(75,75,75)):
        self.start=start
        self.end=end
        self.color=color
        self.shift=V((0,0))
    def move(self,shft):
        if not isinstance(shft,V):
            self.shft=V(shft)
        self.shift=shft
    def paint(self,color):
        self.color=color
    def order(self,P):
        return ((P.apply(self.start))[0]+(P.apply(self.end))[0])/2
    def draw(self,color="null"):
        if color=="null":
            color=self.color
        #255 * (self.end() + (1, 1, 1)) / 2
        pg.draw.line(screen, color, transform(P, self.start, zoom, shift+self.shift), transform(P, self.end, zoom, shift+self.shift),width=2)
    def midpoint(self):
        return (self.start+self.end)/2
pg.init()

P=Matrix([[1,0,0],[0,1,0],[0,0,1]])
P=r(P,(.05,.05))
zoom=130
sensitivity=0.01
clock=pg.time.Clock()
windowSize=V((1000,600))
clickProximity=10
shift=windowSize/2
screen=pg.display.set_mode(windowSize)
leftClicking=pg.mouse.get_pressed()[0]
min=-.5
max=.5
lines1 = [Line(V((min, j, k)),V((max, j, k))) for j in (min, max) for k in (min, max)]
lines1 += [Line(V((i, j, min)), V((i, j, max))) for j in (min, max) for i in (min, max)]
lines1 += [Line(V((i, min, k)), V((i, max, k))) for i in (min, max) for k in (min, max)]

lines2 = [Line(V((-1, j, k)), V((1, j, k))) for j in (-1, 1) for k in (-1, 1) if j**2+k**2!=0]
lines2 += [Line(V((i, j, -1)), V((i, j, 1))) for j in (-1, 1) for i in (-1, 1)if j**2+i**2!=0]
lines2 += [Line(V((i, -1, k)), V((i, 1, k))) for i in (-1, 1) for k in (-1, 1)if i**2+k**2!=0]

lines=lines1+lines2

#corners = [V((i, j, k)) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1) if
#          not (i == 0 and j == 0 and k == 0)]
corners = [V((i, j, k)) for i in (-1, 1) for j in (-1, 1) for k in (-1, 1)]
outsideCorners=corners
insideCorners = [corner/2 for corner in corners]
corners=insideCorners+outsideCorners
#print(pg.font.get_fonts())
myFont=pg.font.SysFont("timesnewroman",50)
# xImOr = pg.image.load("X.png").convert_alpha()
# xIm=pg.transform.rotozoom(xImOr,0,0.5)
# xRect=xIm.get_rect(center=(0,0))
# oImOr=pg.image.load("O.png").convert_alpha()
# oIm = pg.transform.rotozoom(oImOr,0,0.5)
# oRect=oIm.get_rect(center=(0,0))
oSquare=pg.Surface((40,40))
oSquare.fill('orange')
bSquare=pg.Surface((40,40))
bSquare.fill('blue')

turn=1
turnIm=myFont.render("Turn:",True,(64,64,64))
turnImRect=turnIm.get_rect(topright=(200,30))

bRock=Piece("Blue","Rock",0); bRock.telp(V((0,0,0)),0,0.5,B)
bPaper=Piece("Blue","Paper",4); bPaper.telp(V((0,1,0)),0,0.5,B)
bScissors=Piece("Blue","Scissors",2); bScissors.telp(V((1,0,0)),0,0.5,B)

oRock=Piece("Orange","Rock",3); oRock.telp(V((1,1,1)),1,1,B)
oPaper=Piece("Orange","Paper",1); oPaper.telp(V((0,1,1)),1,1,B)
oScissors=Piece("Orange","Scissors",5); oScissors.telp(V((1,0,1)),1,1,B)

B.sps()
pieces=pg.sprite.Group(bRock,bPaper,bScissors,oPaper,oScissors,oRock)
selected=False
gameOver=False
initializeGameOver=False
while True:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            exit()
        if event.type==pg.MOUSEBUTTONDOWN:
            if event.button==1:
                leftClicking=True
                mPos=V(pg.mouse.get_pos())
                if selected:
                    print(list(B.legalMoves(selectedPiece.rank,selectedPiece.pos3, selectedPiece.dimIndex)))
                    for pos, dimIndex in B.legalMoves(selectedPiece.rank,selectedPiece.pos3, selectedPiece.dimIndex):
                        pPos=V(transform(P,2*pos-V((1,1,1)),zoom*(1+dimIndex)/2,shift))
                        print("Checking for proximity")
                        if abs(pPos-mPos)<clickProximity:
                            selected=False
                            memory.append(B)
                            print("FINALLY MOVING")
                            if not isinstance(B.spot(pos,dimIndex),int):
                                initializeGameOver=True
                                B.spot(pos,dimIndex).kill()
                            selectedPiece.goto(pos,dimIndex,(1+dimIndex)/2,B)
                            if initializeGameOver:
                                gameOver=True
                            if turn==0:
                                turn=1
                            else:
                                turn=0
                else:
                    for piece in pieces:
                        if piece.rank%2!=turn:
                            if not piece.travelling:
                                pPos=V(transform(P,2*piece.pos3-(1,1,1),zoom*piece.dim,shift))
                                #print(pPos,piece.color)
                                if abs(pPos-mPos)<clickProximity:
                                    selected=True
                                    selectedPiece=piece
                                    print(selectedPiece)
                print()
                for corn in corners:
                    cPos = V(transform(P, corn, zoom, shift))
        elif event.type==pg.MOUSEBUTTONUP:
            if event.button==1:
                leftClicking=False
        elif event.type==pg.KEYDOWN:
            if event.key==pg.K_b:
                if memory:
                    B,turn=memory.pop()
            elif event.key==pg.K_r:
                B = newBoard()
                turn = 1
                memory = []
    if gameOver:
        print("GAME OVER")
    else:
        if leftClicking:
            newPos=V(pg.mouse.get_pos())
            dX=sensitivity*(newPos-mPos).pmul((-1,1))
            mPos=newPos
            P=r(P,dX)
        pg.draw.rect(screen, (200, 200, 200), (0, 0, *windowSize))
        for piece in pieces:
            piece.update()

        screen.blit(turnIm,turnImRect)
        if turn==1:
            screen.blit(myFont.render( "Blue",True, (0,0,140)),(200,30))
            #screen.blit(bSquare,((320,45)))
        elif turn==0:
            screen.blit(myFont.render("Orange", True, (170, 95, 40)), (200, 30))
            #screen.blit(oSquare,((320,45)))
        for corn in outsideCorners:
             Line(0.5*corn,1*corn,(180,180,180)).draw()
        for corn in corners:
            sx,sy,ds=*transform(P, corn, zoom, shift),20
            pg.draw.ellipse(screen, (100, 100, 100), pg.Rect(sx - ds / 2-0*zoom, sy - ds / 2, ds, ds))
        lines.sort(key = lambda x: x.order(P))
        for line in lines:
            line.draw()
        for i in pieces:
            i.rect.center = transform(P, 2*i.pos3-(1,1,1), zoom*i.dim, shift)
            i.order=(P.apply(i.pos3))[0]*i.dim
        pieceList=[i for i in pieces]
        pieceList.sort(key = lambda x: x.order)
        for i in pieceList:
            screen.blit(i.image,i.rect)



    pg.display.update()
    clock.tick(60)