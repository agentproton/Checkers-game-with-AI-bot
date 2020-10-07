import pygame
import math
import copy
from copy import *
from Board import Board
from gameplay import gameplay
height=800
width=800
row=8
col=8
size= width//col
window= pygame.display.set_mode((width,height))
FPS=60
RED=(255,0,0)
GREY=(128,128,128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)
pygame.display.set_caption('Checkers')
def heuristics(position):
    return (position.com_player-position.human_player)*50+(position.comp_king-position.human_king)*15
def alpha_beta_pruning(checkersboard,alpha,beta,depth,max_player,game):
    if depth == 0 or game.board.human_player<=0 or game.board.com_player<=0:
        return heuristics(checkersboard),checkersboard
    best_move=None
    if max_player:
        mx=-math.inf
        func=total_moves(checkersboard,GREY,game)
        for i in func:
            answer=alpha_beta_pruning(i,alpha,beta,depth-1,False,game)[0]
            if(mx>=beta):return mx,best_move
            alpha=max(alpha,mx);
            if mx<answer:
                best_move=i
                mx=answer
        return mx,best_move
    else:
        mn=math.inf
        func=total_moves(checkersboard,RED,game)
        for i in func:
            answer=alpha_beta_pruning(i,alpha,beta,depth-1,True,game)[0]
            if(mn<=alpha):return mn,best_move
            beta=min(beta,mn)
            if mn>answer:
                best_move=i
                mn=answer
        return mn, best_move
def get_pieces(board,color):
    func=[]
    for i in board:
        for j in i:
            if j!=0 and j.color==color:
                func.append(j)
    return func
def total_moves(board,color,game):
    moves = []
    func=get_pieces(board.board,color)
    for piece in func:
        possible_move=board.getpossiblemove(piece)
        for move,spawn in possible_move.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.board[(piece.row)][( piece.col)]
            new_board=temp_board
            new_board.move(temp_piece,move[0],move[1])
            if spawn:
                new_board.remove_items(spawn)
            moves.append(new_board)
    return moves
def main():
    game=gameplay(window)
    run=True
    while run:
        if game.turn == GREY:
            value, new_board =alpha_beta_pruning(game.board,-math.inf,math.inf,4,GREY,game)
            game.board=new_board 
            game.jump_moves={}
            game.turn=RED
        if game.board.human_player<=0:
            print("COMPUTER WINS")
            run=False
        elif game.board.com_player<=0:
            print("Human player")
            run=False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                x=pos[1]//100
                y=pos[0]//100
                game.selection(x,y)
        game.update()
    pygame.quit()
main()
