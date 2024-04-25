import pygame
import random
import time

pygame.init()
pygame.display.set_caption('记忆游戏')
screen = pygame.display.set_mode((440,490))#320 370
myfont = pygame.font.Font(None, 30)

game_over = True
first_open=True

white = (255, 255, 255)
black = (198, 230, 232)
# black=(249,244,220)
yellow = (250, 249, 222)
blue = (147,213,220)
# black=(0,0,0)
button_rect=(220,10,80,35)
text_rect=(115,5,20,20)

Red=(255, 0, 0)
Green=(0, 255, 0)
Blue=(0, 0, 255)
Yellow= (255, 255, 0)
Purple= (128, 0, 128)
Cyan=(0, 255, 255)
Orange=(255, 165, 0)
Pink=(255, 192, 203)

grid_size = 100#格大小
grid_padding = 10
score=0

textImage = myfont.render('Your score: {}'.format(score), True, blue)#文本字体
textWin = myfont.render('Bingo!', True, blue)# Press Again and stard again
textlose = myfont.render('You lose!', True, blue)
# textdraw = myfont.render('draw!',True,blue)
# textagain =myfont.render('Again',True,color_dark)

grid_positions = [(x * (grid_size + grid_padding),50 + y * (grid_size + grid_padding))
                  for y in range(4) for x in range(4)]

rects = [pygame.Rect(x, y, grid_size, grid_size) for x, y in grid_positions]
button_rects = [pygame.Rect(220, 10, 80, 35)]

board = [' ' for i in range(16)]

last_clicks = [None, None]

colors = [Red, Green, Blue, Yellow, Purple, Cyan, Orange, Pink]*2
         
random.shuffle(colors)


def draw_board(last_clicks):
    # 重绘 
    for index, rect in enumerate(rects):
        pygame.draw.rect(screen, yellow, rect)
        if last_clicks[0] == index or last_clicks[1] == index :
            pygame.draw.rect(screen, colors[index],rect)
            pygame.display.flip()
    # print(rect.x)

def initial_screen():
    screen.fill(black)
    pygame.draw.rect(screen,black,button_rect)#重启按钮
    # screen.blit(textagain, (230, 17))
    textImage = myfont.render('Your score: {}'.format(score), True, blue)
    screen.blit(textImage, (5, 5))#文本

    for rect in rects:#画格子
        pygame.draw.rect(screen, yellow, rect)


def renew_screen():
    textImage = myfont.render('Your score: {}'.format(score), True, blue)
    pygame.draw.rect(screen,yellow,text_rect)
    screen.blit(textWin, (25, 25))
    screen.blit(textImage, (5, 5))
    pygame.display.flip()

while game_over:
    
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            for index, rect in enumerate(rects):
                if rect.collidepoint(mouse_pos):
                    print(index,rect) 
                    
                    last_clicks[1] = last_clicks[0]
                    last_clicks[0] = index 
                    draw_board(last_clicks)
                    
                    if last_clicks[1]!=None:
                        if colors[index]==colors[last_clicks[1]]:
                            
                            colors[last_clicks[1]]=black
                            colors[index]=black
                            print("win")

                            print(index,rect)
                            print(last_clicks[0],last_clicks[1])
                            score+=1
                            renew_screen()

    if event.type == pygame.QUIT:
        game_over = False
    
    if first_open:
        first_open=False
        initial_screen()
        pygame.display.flip()
pygame.quit()
