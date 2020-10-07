import pygame
from Board import Board
ROW=8
COL=8
cell_size=100
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)
class gameplay:
    def __init__(self,window):
        self.selectpiece=None
        self.board=Board()
        self.turn=RED
        self.jump_moves={}
        self.window=window
    def update(self):
        self.board.draw(self.window)
        for move in self.jump_moves:
            l,m =move
            pygame.draw.circle(self.window, BLUE, (m*100+50,l*100+50), 15)
        pygame.display.update()

    def detect(self,row,col):
        detect_piece=self.board.board[row][col]
        if detect_piece!=0 and detect_piece.color==self.turn:
            self.selectpiece=detect_piece
            self.jump_moves=self.board.getpossiblemove(detect_piece)
            return True
        return False

    def selection(self,row,col):
        if self.selectpiece:
            result = self.movement(row, col)
            if not result:
                self.selectpiece = None
                self.selection(row,col)
        return self.detect(row,col)
    def movement(self,row,col):
        move_to_cell=self.board.board[row][col]
        if (row,col) in self.jump_moves:
            if move_to_cell==0:
                self.board.move(self.selectpiece,row,col)
                deleted_piece=self.jump_moves[(row,col)]
                if deleted_piece:
                    self.board.remove_items(deleted_piece)
                self.jump_moves={}
                if self.turn==GREY:
                    self.turn=RED
                else:
                    self.turn=GREY
            else:
                return False
        else:
            return False
        return True