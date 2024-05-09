import pygame
import random
import time

class MemoryGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('记忆游戏')
        self.screen = pygame.display.set_mode((450, 600))
        self.font = pygame.font.Font(None, 30)
        self.Open, self.start, self.ending, self.game_over, self.first_open, self.second_open=\
        True, True, True, True, True, True
        self.user_click = 16
        self.win_num = 0
        self.duration = 3
        self.last_clicks = [None, None]
        self.grid_positions = [(10+x * (100 + 10),150 + y * (100 + 10))
                  for y in range(4) for x in range(4)]
        self.rects = [pygame.Rect(x, y, 100, 100) for x, y in self.grid_positions]

        self.backgroud = (198, 230, 232)
        self.white = (255, 255, 255)
        self.blue = (147, 213, 220)
        self.yellow = (250, 249, 222)
        self.black = (0,0,0)
        self.colors = self.random_colors()

        self.button_rect = (230, 10, 80, 35)#开始按钮
        self.time_rect = (310, 10, 120, 35)#时间倒计时覆盖
        self.ending_rect = (310, 45, 120, 35)#结束按钮

        self.button_rects = [pygame.Rect(self.button_rect)]
        self.ending_rects = [pygame.Rect(self.ending_rect)]
        self.board = [' ' for i in range(16)]

    #矩形区域显示
    def render_text(self,text,colors,position):
        text_name = self.font.render(text, True, colors)
        self.screen.blit(text_name, position)

    #等待时间
    def wait_time(self,times=3):
        for i in range(times):
            text = 'Time : {0}'.format(times - i)
            textTime = self.font.render(text, True, self.black)
            pygame.draw.rect(self.screen,self.white,self.time_rect)
            self.screen.blit(textTime, (325, 20))
            pygame.display.flip()
            time.sleep(1)
    
    #随机颜色
    def random_colors(self):
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (128, 0, 128), (0, 255, 255), (255, 165, 0), (255, 192, 203)] * 2
        random.shuffle(colors)
        return colors
    
    #只显示两个格子
    def draw_board(self):
        for index, rect in enumerate(self.rects):
            pygame.draw.rect(self.screen, self.yellow, rect)
            if self.last_clicks[0] == index or self.last_clicks[1] == index :
                pygame.draw.rect(self.screen, self.colors[index],rect)
        pygame.display.flip()

    #显示屏幕3s
    def display_screen(self):
        self.screen.fill(self.backgroud)
        for rect, color in zip(self.rects, self.colors):
            pygame.draw.rect(self.screen, color, rect)
            pygame.display.flip()
        self.wait_time(3)
        pygame.draw.rect(self.screen, self.backgroud, self.time_rect)
        pygame.draw.rect(self.screen, self.white, self.ending_rect)#结束按钮
        self.render_text('Ending', self.black,(325, 50))
        for rect, color in zip(self.rects, self.colors):#画格子
            pygame.draw.rect(self.screen, self.yellow, rect)
        pygame.display.flip()

    #初始化屏幕
    def initial_screen(self):
        self.screen.fill(self.backgroud)
        pygame.draw.rect(self.screen, self.white, self.button_rect)#重启按钮
        self.render_text('Start', self.black, (235, 20))
        self.render_text('Only displayed for 3 seconds', self.yellow, (20, 75))
        self.render_text('If you are ready, Please press Start', self.yellow, (20, 100))
        for rect in self.rects:#画格子
            pygame.draw.rect(self.screen, self.yellow, rect)

    #显示点击次数
    def click_display(self):
        pygame.draw.rect(self.screen, self.backgroud, (115, 5, 80, 35))#覆盖点击区域
        textImage = self.font.render('Your score: {}'.format(self.user_click), True, self.blue)
        self.screen.blit(textImage, (5, 5))
        pygame.display.update((0, 0, 200, 50))#click text

    #重新初始化
    def reopen(self):
        self.ending, self.start, self.first_open = True, True, True
        self.user_click = 11
        self.win_num = 0
        return self.ending, self.start, self.first_open, self.second_open, self.user_click, self.win_num

    def loop(self):
        while self.Open:
            self.reopen()
            self.colors = self.random_colors()
            while self.start:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos      
                        #监听是否按了Start                
                        for button_click in self.button_rects: 
                            if  button_click.collidepoint(mouse_pos):
                                self.game_over = False
                                self.start = False
                                self.second_open = True

                if self.first_open:      
                    self.first_open = False
                    self.initial_screen()
                    pygame.display.flip()
                
                if event.type == pygame.QUIT:
                    self.start = False
                    self.Open = False

            while not self.game_over:
                self.click_display()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and self.ending:
                        mouse_pos = event.pos
                        for index, rect in enumerate(self.rects):
                            if rect.collidepoint(mouse_pos) and index != self.last_clicks[0]:
                                self.last_clicks[1] = self.last_clicks[0]
                                self.last_clicks[0] = index
                                self.user_click -= 1
                                self.draw_board()
                                if self.last_clicks[1] != None:
                                    if self.colors[index] == self.colors[self.last_clicks[1]] \
                                    and self.last_clicks[1] != None \
                                    and self.colors[self.last_clicks[1]] != self.backgroud:
                                        self.colors[self.last_clicks[1]] = self.backgroud
                                        self.colors[index] = self.backgroud
                                        self.win_num += 1

                        for ending_click in self.ending_rects:
                            if  ending_click.collidepoint(mouse_pos):
                                self.game_over = True
                                
                if self.second_open:      
                    self.second_open = False
                    self.display_screen()

                if self.win_num == 8:
                    self.render_text('You Win!', (255, 0, 0), (20, 125))
                if self.user_click <= 0:
                    self.render_text('You Lose!', (255, 0, 0), (20, 125))
                    for rect, color in zip(self.rects, self.colors):
                        pygame.draw.rect(self.screen, color, rect)
                    pygame.display.flip()
                    time.sleep(2)
                    break

                if event.type == pygame.QUIT:
                    self.game_over = True
                    self.Open = False
        # pygame.quit()

playgame = MemoryGame()
playgame.loop()