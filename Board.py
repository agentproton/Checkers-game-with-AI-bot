import pygame
ROW=8
COL=8
cell_size=100
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)
king_pic= pygame.transform.scale(pygame.image.load('/home/ankit/Pictures/crown.png'), (44, 25))
class Piece:
    def __init__(self, row, col, color):
        self.row=row
        self.col=col
        self.king=False
        self.color=color
        self.x=100*col+50
        self.y=100*row+50
    
    def draw(self,window):
        pygame.draw.circle(window,BLACK,(self.x,self.y),45)
        pygame.draw.circle(window,self.color,(self.x, self.y),30)
        if self.king:
            window.blit(king_pic,(self.x -king_pic.get_width()//2, self.y -king_pic.get_height()//2))
class Board:
    def __init__(self):
        self.human_king=0
        self.comp_king=0
        self.com_player=12
        self.human_player=12
        self.board=[]
        self.create_checkersboard()

    def create_checkersboard(self):
        for i in range(ROW):
            self.board.append([])
            for j in range(COL):
                if ((i+j)%2!=0):
                    self.board[i].append(0)
                else:
                    if i<3:
                        self.board[i].append(Piece(i,j,GREY))
                    elif i>4:
                        self.board[i].append(Piece(i,j,RED))
                    else:
                        self.board[i].append(0)
    def draw(self,window):
        window.fill(BLACK)
        for i in range(ROW):
            for j in range(COL):
                if((i+j)%2==0):
                    pygame.draw.rect(window,WHITE,(i*cell_size,j*cell_size,cell_size,cell_size))
        for i in range(ROW):
            for j in range(COL):
                piece=self.board[i][j]
                if piece!=0:
                    piece.draw(window)
    def getpossiblemove(self,piece):
        possible_move={}
        rows=piece.row
        cols=piece.col
        h=max(rows-3,-1)
        k=min(rows+3,ROW)
        if piece.color==RED or piece.king:
            possible_move.update(self.getmove(rows-1,h,-1,cols,piece.color,True))
            possible_move.update(self.getmove(rows-1,h,-1,cols,piece.color,False))
        if piece.color==GREY or piece.king:
            possible_move.update(self.getmove(rows+1,k,1,cols,piece.color,True))
            possible_move.update(self.getmove(rows+1,k,1,cols,piece.color,False))
        return possible_move

    def getmove(self,start,over,step,jump,color,temp,flip=[]):
        moves = {}
        last = []
        if temp:
            jump-=1
        else:
            jump+=1
        for i in range(start,over,step):
            if temp:
                if jump<0:
                    break
            else:
                if jump>=COL:
                    break
            current = self.board[i][jump]
            if current == 0:
                if flip and not last:
                    break
                elif flip:
                    moves[(i,jump)]=last+flip
                else:
                    moves[(i,jump)] =last
                if last:
                    if step == -1:
                        row = max(i-3, 0)
                    else:
                        row = min(i+3,ROW)
                    next_step=i+step
                    moves.update(self.getmove(next_step,row,step,jump-1,color,temp,flip=last))
                    moves.update(self.getmove(next_step,row,step,jump+1,color,temp,flip=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            if temp:
                jump-=1
            else:
                jump+=1
        
        return moves
    def remove_items(self,availaible_pieces):
        for i in availaible_pieces:
            self.board[i.row][i.col]=0
            if i !=0:
                if i.color==GREY:
                    self.com_player=self.com_player-1
                else:
                    self.human_player=self.human_player-1
    def checke(self,piece,row,col):
        if (row== ROW-1)or(row==0):
            piece.king=True
        if piece.color==GREY:
            self.comp_king=self.comp_king+1
        else:
            self.human_king=self.human_king+1
    def moveinboard(self,piece,row,col):
        piece.col=col
        piece.row=row
        piece.x=100*col+50
        piece.y=100*row+50
    def move(self, piece, row, col):
        self.board[piece.row][piece.col],self.board[row][col]=self.board[row][col],self.board[piece.row][piece.col]
        self.moveinboard(piece,row,col)
        self.checke(piece,row,col)
    def gameWinner(self):
        if self.human_player<= 0:
            return GREY
        elif self.com_player<= 0:
            return RED
        return None 