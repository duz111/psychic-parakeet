import pygame

pygame.init()

res = (720,720)
screen = pygame.display.set_mode(res)

color_light = (170,170,170)
color_dark = (100,100,100)

smallfont = pygame.font.SysFont('Corbel',35)
text = smallfont.render('quit' , True , (255,255,255))

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if screen.get_width()/2 <= mouse[0] <= screen.get_width()/2+140 and screen.get_height()/2 <= mouse[1] <= screen.get_height()/2+40:
                pygame.quit()

    screen.fill((60,25,60))
    mouse = pygame.mouse.get_pos()

    if screen.get_width()/2 <= mouse[0] <= screen.get_width()/2+140 and screen.get_height()/2 <= mouse[1] <= screen.get_height()/2+40:
        pygame.draw.rect(screen,color_light,[screen.get_width()/2,screen.get_height()/2,140,40])
    else:
        pygame.draw.rect(screen,color_dark,[screen.get_width()/2,screen.get_height()/2,140,40])

    screen.blit(text , (screen.get_width()/2+50,screen.get_height()/2))

    pygame.display.update()
