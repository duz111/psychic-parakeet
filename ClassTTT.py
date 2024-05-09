import pygame
import random

class TTTGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('井字棋')
        self.screen = pygame.display.set_mode((320, 370))
        self.myfont = pygame.font.Font(None, 30)
        self.open, self.game_over, self.game_continue, self.first_open = \
            True, True, True, True
        self.white = (255, 255, 255)
        self.yellow = (250, 249, 222)
        self.blue = (147, 213, 220)
        self.black = (0, 0, 0)
        self.color_light = (170, 170, 170)
        self.color_dark = (100, 100, 100)
        self.button_rect = (220, 10, 80, 35)
        self.text_rect = (115, 5, 20, 20)
        self.grid_positions = [(x * (100 + 10),50 + y * (100 + 10))
                  for y in range(3) for x in range(3)]
        self.button_rects = [pygame.Rect(220, 10, 80, 35)]

        # self.rects = [pygame.Rect(x, y, 100, 100) for x, y in 10]
        self.rects = [pygame.Rect(x, y, 100, 100) for x in range(0, 310, 110) for y in range(50, 360, 110)]

        self.score = 0
        self.board = [' ' for i in range(9)]




    def render_text(self, text, colors, position):
        text_name = self.myfont.render(text, True, colors)
        self.screen.blit(text_name, position)

    def check_win(self, board, player):
        win_cond = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                    (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for condition in win_cond:
            if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
                return True
        return False

    def is_board_full(self):
        return ' ' not in self.board[1:]

    def computer_move(self):
        empty_positions = [i for i in range(9) if self.board[i] == ' ']
        random_walk = []
        boardcopy = self.board[:]
        move = True
        
        # 检查电脑是否获胜
        for j in empty_positions:
            boardcopy[j] = 'O'
            if self.check_win(boardcopy,'O'):
                self.board[j] = 'O'
                return True
            boardcopy[j] = ' '

        # 阻止X获胜
        if move:
            for k in empty_positions:
                boardcopy[k] = 'X'
                if self.check_win(boardcopy,'X'):
                    self.board[k] = 'O'
                    move = False
                    break   
                boardcopy[k] = ' '

        #占四个角
        if move:
            for i in empty_positions:
                if i in [1, 3, 7, 9]:
                    random_walk.append(i)
            if len(random_walk) != 0:
                self.board[random.choice(random_walk)] = 'O'
                move = False

        #占5
        if move:
            if 5 in empty_positions:
                self.board[5] = 'O'
                move = False

        #随便走一个
        if move and empty_positions !=[]:
            self.board[random.choice(empty_positions)] = 'O'
            move = False

        if self.check_win(self.board,'O'):
            return True
      
    def draw_board(self):
        # 重绘所有 X 和 O
        for index, value in enumerate(self.board):
            if value != ' ':
                rect = self.rects[index]
                if value == 'X':
                    pygame.draw.line(self.screen, self.white, (rect[0]+10, rect[1]+10), (rect[0]+90, rect[1]+90), 5)
                    pygame.draw.line(self.screen, self.white, (rect[0]+90, rect[1]+10), (rect[0]+10, rect[1]+90), 5)
                elif value == 'O':
                    pygame.draw.ellipse(self.screen, self.white, rect.inflate(-20, -20), 5)  
        pygame.display.flip()  # 更新屏幕

    def initial_screen(self):
        self.screen.fill(self.yellow)
        pygame.draw.rect(self.screen, self.blue, self.button_rect)
        self.render_text('Again', self.color_dark, (230, 17))
        self.render_text('Your score: {}'.format(self.score), self.blue, (5, 5))#文本
        for rect in self.rects:#画格子
            pygame.draw.rect(self.screen, self.blue, rect)  

    def renew_screen(self):
        pygame.draw.rect(self.screen, self.yellow, self.text_rect)
        self.render_text('You win!', self.blue, (25, 25))
        self.render_text('Your score: {}'.format(self.score), self.blue, (5, 5))

    def loop(self):
        while self.game_over:
            self.initial_screen()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    
                    for index, rect in enumerate(self.rects):
                        if rect.collidepoint(mouse_pos) and self.board[index]!='O' and \
                                self.board[index] != 'X' and self.game_continue: 
                            self.board[index] = 'X'
                            if self.check_win(self.board, 'X'):
                                self.score += 1 
                                self.renew_screen()
                                self.game_continue = False                                                                    
                            else:
                                self.computer_move()
                            if self.check_win(self.board, 'O'):
                                self.render_text('You lose!', self.blue, (25, 25))
                                self.game_continue = False                       
                            if self.is_board_full():
                                self.render_text('Draw!', self.blue, (25, 25))

                    #监听是否按了Again
                    for button_click in self.button_rects:
                        if  button_click.collidepoint(mouse_pos):
                            self.board = [' ' for i in range(9)] 
                            self.game_continue = True

                    self.draw_board()                

                if event.type == pygame.QUIT:
                    self.game_over = False
                
                if self.first_open:
                    self.first_open=False
                    pygame.display.flip()
        pygame.quit()

play = TTTGame()
play.loop()