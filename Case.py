import pygame as pg
from sys import exit
from Matrix_Class import Matrix,V
from math import sin, cos,pi
from Case_Board import Board,newBoard,getAdjacent
from Sprite_Classes import Piece,ftt
from Button_Class import Button
import time
debug=not True
def r(Orientation,dX): #Apply a mouse movement to the matrix
    dx,dy=dX
    cdx,sdx,cdy,sdy=cos(dx),sin(dx),cos(dy),sin(dy)
    roth = Matrix([[cdx, sdx, 0], [-sdx, cdx, 0], [0, 0, 1]])
    rotv = Matrix([[cdy, 0, sdy], [0, 1, 0], [-sdy, 0, cdy]])
    rot = roth*rotv
    # rot.strict_normalize()
    return rot*Orientation
def cast(X): #Turn the 3 vector into a 2 vector ... -ish
    return V((X[1],-X[2]))
def transform(P,X,zoom=1,shift=V((0,0))): #Transform the 3 vector into what goes on the screen
    return cast(P.apply(X)*zoom)+shift

def order(vec3):
    return P.apply(vec3)[0]
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
    def order(self):
        #return order(self.midpoint())
        return min(order(ftt(self.start)),order(ftt(self.end)))-0.01
    def blit(self,screen,color="null"):
        if color=="null":
            color=self.color
        #255 * (self.end() + (1, 1, 1)) / 2
        pg.draw.line(screen, color, transform(P, ftt(self.start), zoom, shift+self.shift), transform(P, ftt(self.end), zoom, shift+self.shift),width=line_width)
    def midpoint(self):
        return (self.start+self.end)/2
class Corner():
    def __init__(self,pos,color=(75,75,75)):
        self.pos=pos
        self.color=color
        self.shift=V((0,0))
    def move(self,shft):
        self.shift=V(shft)
    def paint(self,color):
        self.color=color
    def order(self):
        return order(ftt(self.pos))
    def blit(self,screen,color="null"):
        if color=="null":
            color=self.color
        pg.draw.ellipse(screen,color,(transform(P, ftt(self.pos), zoom, shift+self.shift)-(10,10),(20,20)))
        #255 * (self.end() + (1, 1, 1)) / 2
        # pg.draw.line(screen, color, transform(P, self.start, zoom, shift+self.shift), transform(P, self.end, zoom, shift+self.shift),width=2)
def undo():
    global turn,B
    if memory:
        B = memory.pop()
        turn = (turn + 1) % 2
        for p in pieces:
            p.find_yourself(B)
def check_game_over():
    blue_win = True
    orange_win = True
    for i in pieces:
        if i.rank % 2 == i.destination[3]:
            if i.rank % 2 == 0:
                blue_win = False
            if i.rank % 2 == 1:
                orange_win = False
    if orange_win:
        global orange_victory
        orange_victory=True
    if blue_win:
        global blue_victory
        blue_victory = True
    if blue_win or orange_win:
        return True
    return False
pg.init()
P=Matrix([[1,0,0],[0,1,0],[0,0,1]])
P=r(P,(.05,.05))
memory=[]
zoom=130
sensitivity=0.01
hyper_theta=-90
clock=pg.time.Clock()
window_size=V((1000,600))
clickProximity=28
shift=window_size/2
screen=pg.display.set_mode(window_size)
leftClicking=pg.mouse.get_pressed()[0]
lines=[]
for dim in range(2):
    lines += [Line(V((0, j, k,dim)), V((1, j, k,dim))) for j in (0, 1) for k in (0, 1)]
    lines += [Line(V((i, j, 0,dim)), V((i, j, 1,dim))) for j in (0, 1) for i in (0, 1)]
    lines += [Line(V((i,0, k,dim)), V((i, 1, k,dim))) for i in (0, 1) for k in (0, 1)]

outsideCorners=[Corner(V((i, j, k,1)),(120, 100, 80)) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
insideCorners =[Corner(V((i, j, k,0)),(100, 100, 130)) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
corners=insideCorners+outsideCorners

turn=1
myFont=pg.font.SysFont("calibri",50)
smaller_font=pg.font.SysFont("calibri",19)
turnIm=myFont.render("Turn: ",True,(64,64,64))
orange_turn_text=myFont.render("Orange", True, (170, 95, 40))
blue_turn_text=myFont.render( "Blue",True, (0,0,140))
instr_1=smaller_font.render("Click on a piece to select and move to an adjacent spot.",True,(50,50,50))
instr_1_rect=instr_1.get_rect(bottomright=(990,540))
instr_2=smaller_font.render("To win, take an enemy piece or get all pieces to the enemy color.",True,(50,50,50))
instr_2_rect=instr_2.get_rect(bottomright=(990,563))
instr_3=smaller_font.render("Right click or 'b' to undo, 'r' to restart, left click to rotate.",True,(50,50,50))
instr_3_rect=instr_3.get_rect(bottomright=(990,586))
turnImRect=turnIm.get_rect(bottomright=(200,80))
orange_turn_text_rect=orange_turn_text.get_rect(bottomleft=(200,80))
blue_turn_text_rect=blue_turn_text.get_rect(bottomleft=(200,80))
go_text=myFont.render("Game Over",True,(30,30,30))
go_text_rect=go_text.get_rect(midbottom=(850,80))
ov_text=myFont.render("Orange Wins",True,(30,30,30))
ov_text_rect=ov_text.get_rect(midtop=(850,80))
bv_text=myFont.render("Blue Wins",True,(30,30,30))
bv_text_rect=bv_text.get_rect(midtop=(850,80))

if debug:
    line_width_slider=Button((30,10),(60,60,60),thickness=1)
    line_width_slider.center((50,260))
    line_width=int(line_width_slider.rect.centery/10-24)
else:
    line_width=2

oRock=Piece("Orange","Rock",3);
oPaper=Piece("Orange","Paper",1);
oScissors=Piece("Orange","Scissors",5);
bPaper=Piece("Blue","Paper",4);
bScissors=Piece("Blue","Scissors",2);
bRock =Piece("Blue","Rock",0);
def set_up_board(B):
    oRock.telp(B,V((1, 1, 1, 1)))
    oPaper.telp(B,V((0,1,1,1)))
    oScissors.telp(B,V((1,0,1,1)))
    bPaper.telp(B,V((0,1,0,0)))
    bScissors.telp(B,V((1,0,0,0)))
    bRock.telp(B,V((0,0,0,0)))
def reset_board(B):
    oRock.goto(B,V((1, 1, 1, 1)))
    oPaper.goto(B,V((0,1,1,1)))
    oScissors.goto(B,V((1,0,1,1)))
    bPaper.goto(B,V((0,1,0,0)))
    bScissors.goto(B,V((1,0,0,0)))
    bRock.goto(B,V((0,0,0,0)))
B=newBoard()
set_up_board(B)

background=pg.Surface(window_size); background.fill((200,205,200))
ranked_pieces=[bRock,oPaper,bScissors,oRock,bPaper,oScissors]
pieces=ranked_pieces[:]
objects=[i for i in ranked_pieces]
for i in lines:
    objects.append(i)
for i in corners:
    objects.append(i)
for corn1, corn2 in zip(outsideCorners, insideCorners):
    objects.append(Line(corn1.pos, corn2.pos, (160, 160, 160)))
selected=False
rotating=1
folding_speed=3
game_over=False
orange_victory=False
blue_victory=False
while True:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            exit()
        if event.type==pg.MOUSEBUTTONDOWN:
            if event.button==1:
                mPos=V(pg.mouse.get_pos())
                if selected: # Move the piece
                    for pos in sorted(B.legalMoves(selectedPiece.rank,selectedPiece.pos4),key=lambda x:order(ftt(x)),reverse=True):
                        pPos=V(transform(P,ftt(pos),zoom,shift))
                        if abs(pPos-mPos)<clickProximity:
                            memory.append(B.copy())
                            if B.get(pos) >= 0:
                                game_over=True
                                if selectedPiece.rank%2==0:
                                    blue_victory=True
                                else:
                                    orange_victory=True
                            selectedPiece.goto(B, pos)
                            if check_game_over():
                                game_over=True
                            if turn==0:
                                turn=1
                            else:
                                turn=0
                            break
                    selected = False
                    selectedPiece.selected = False
                elif not game_over: # Select the piece
                    for piece in reversed(pieces):
                        if piece.rank%2!=turn:
                            if not piece.travelling:
                                pPos=piece.pos2
                                if abs(pPos-mPos)<clickProximity and selected==False:
                                    selected=True
                                    piece.selected=True
                                    selectedPiece=piece
                                    print(selectedPiece)
                if not selected:
                    if debug and line_width_slider.collidepoint(mPos):
                        line_width_slider.pressed=True
                    else:
                        leftClicking = True
            elif event.button==4:
                rotating=1
            elif event.button==5:
                rotating=-1
            elif event.button==3:
                undo()
                selected = False
                selectedPiece.selected=False
                game_over = check_game_over()
                blue_victory = False
                orange_victory = False
        elif event.type==pg.MOUSEBUTTONUP:
            if event.button==1:
                leftClicking=False
                if debug:
                    line_width_slider.pressed=False
        elif event.type==pg.KEYDOWN:
            if event.key==pg.K_b:
                undo()
                selected=False
                selectedPiece.selected = False
                game_over=check_game_over()
                blue_victory=False
                orange_victory=False
            elif event.key==pg.K_r or event.key==pg.K_SPACE:
                B = newBoard()
                reset_board(B)
                turn = 1
                memory = []
                game_over=False
                blue_victory = False
                orange_victory = False
    if leftClicking:
        newPos=V(pg.mouse.get_pos())
        dX=sensitivity*(newPos-mPos).pmul((-1,1))
        mPos=newPos
        P=r(P,dX)
    if rotating:
        hyper_theta+=folding_speed*rotating
        if hyper_theta==180 or hyper_theta==-180:
            rotating=0
            hyper_theta=180
        if hyper_theta==360 or hyper_theta==0:
            rotating=0
            hyper_theta=0
    screen.blit(background,(0,0))
    if debug:
        pg.draw.line(screen,(0,0,0),(50,250),(50,350))
        line_width_slider.blit(screen)
    if game_over:
        screen.blit(go_text,go_text_rect)
        if orange_victory:
            screen.blit(ov_text,ov_text_rect)
        else:
            screen.blit(bv_text, bv_text_rect)
    screen.blit(instr_1, instr_1_rect)
    screen.blit(instr_2, instr_2_rect)
    screen.blit(instr_3, instr_3_rect)
    for piece in pieces:
        piece.update(P,zoom,shift,hyper_theta,rotating)

    screen.blit(turnIm,turnImRect)
    if turn==1:
        screen.blit(blue_turn_text,orange_turn_text_rect)
    elif turn==0:
        screen.blit(orange_turn_text,orange_turn_text_rect)
    # for corn1,corn2 in zip(outsideCorners,insideCorners):
    #     Line(corn1.pos,corn2.pos,(160,160,160)).blit(screen)
    if debug and line_width_slider.pressed:
        line_width_slider.center((50,max(min(pg.mouse.get_pos()[1],350),250)))
        line_width=int(line_width_slider.rect.centery/10-24)
    for i in pieces:
        i.ORDER=(P.apply(i.pos3))[0]
    pieces.sort(key = lambda x: x.order())
    objects.sort(key = lambda x: x.order())
    for i in objects:
        i.blit(screen)




    pg.display.update()
    clock.tick(60)