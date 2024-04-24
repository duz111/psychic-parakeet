import pygame
import random

pygame.init()
pygame.display.set_caption('井字棋')
screen = pygame.display.set_mode((320,370))
myfont = pygame.font.Font(None, 30)

game_over = True
first_open=True
game_continue=True
white = (255, 255, 255)
yellow = (250, 249, 222)
blue = (147,213,220)
black=(0,0,0)
color_light = (170,170,170)
color_dark = (100,100,100)
button_rect=(220,10,80,35)
text_rect=(115,5,20,20)

grid_size = 100#九宫格大小
grid_padding = 10
score=0

textImage = myfont.render('Your score: {}'.format(score), True, blue)#文本字体
textWin = myfont.render('You win!', True, blue)# Press Again and stard again
textlose = myfont.render('You lose!', True, blue)
textdraw = myfont.render('draw!',True,blue)
textagain =myfont.render('Again',True,color_dark)

grid_positions = [(x * (grid_size + grid_padding),50 + y * (grid_size + grid_padding))
                  for y in range(3) for x in range(3)]

rects = [pygame.Rect(x, y, grid_size, grid_size) for x, y in grid_positions]
button_rects = [pygame.Rect(220, 10, 80, 35)]

board = [' ' for i in range(9)]

def check_win(board,player):
    win_cond = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for condition in win_cond:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def is_board_full():
    return ' ' not in board[1:]

def computer_move():
    empty_positions = [i for i in range(9) if board[i] == ' ']
    random_walk = []
    boardcopy = board[:]
    move = True
    
    # 检查电脑是否获胜
    for j in empty_positions:
        boardcopy[j] = 'O'
        if check_win(boardcopy,'O'):
            board[j] = 'O'
            return True
        boardcopy[j] = ' '

    # 阻止X获胜
    if move:
        for k in empty_positions:
            boardcopy[k] = 'X'
            if check_win(boardcopy,'X'):
                board[k] = 'O'
                move = False
                break   
            boardcopy[k] = ' '

    #占四个角
    if move:
        for i in empty_positions:
            if i in [1, 3, 7, 9]:
                random_walk.append(i)
        if len(random_walk) != 0:
            board[random.choice(random_walk)] = 'O'
            move = False

    #占5
    if move:
        if 5 in empty_positions:
            board[5] = 'O'
            move = False

    #随便走一个
    if move and empty_positions !=[]:
        board[random.choice(empty_positions)] = 'O'
        move = False

    if check_win(board,'O'):
        return True
      
def draw_board(board):
    # 重绘所有 X 和 O
    for index, value in enumerate(board):
        if value != ' ':
            rect = rects[index]
            if value == 'X':
                pygame.draw.line(screen, white, (rect[0]+10, rect[1]+10), (rect[0]+90, rect[1]+90), 5)
                pygame.draw.line(screen, white, (rect[0]+90, rect[1]+10), (rect[0]+10, rect[1]+90), 5)
            elif value == 'O':
                pygame.draw.ellipse(screen, white, rect.inflate(-20, -20), 5)  
    pygame.display.flip()  # 更新屏幕

def initial_screen():
    screen.fill(yellow)
    pygame.draw.rect(screen,blue,button_rect)
    screen.blit(textagain, (230, 17))
    textImage = myfont.render('Your score: {}'.format(score), True, blue)
    screen.blit(textImage, (5, 5))#文本
    for rect in rects:#画格子
        pygame.draw.rect(screen, blue, rect)  

def renew_screen():
    textImage = myfont.render('Your score: {}'.format(score), True, blue)
    pygame.draw.rect(screen,yellow,text_rect)
    screen.blit(textWin, (25, 25))
    screen.blit(textImage, (5, 5))

while game_over:
    initial_screen()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            for index, rect in enumerate(rects):
                if rect.collidepoint(mouse_pos) and board[index]!='O' and board[index]!='X' and game_continue: 
                    board[index] = 'X'
                    if check_win(board,'X'):
                        score+=1 
                        renew_screen()
                        game_continue=False                                                                    
                    else:
                        computer_move()
                    if check_win(board,'O'):
                        screen.blit(textlose, (25, 25))
                        game_continue=False                       
                    if is_board_full():
                        screen.blit(textdraw, (25, 25))

            #监听是否按了Again
            for button_click in button_rects:
                if  button_click.collidepoint(mouse_pos):
                    board = [' ' for i in range(9)] 
                    game_continue=True

            draw_board(board)                

        if event.type == pygame.QUIT:
            game_over = False
        
        if first_open:
            first_open=False
            pygame.display.flip()
pygame.quit()
