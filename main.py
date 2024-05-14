import pygame
import elements

pygame.init()

#size screen
screen_width, screen_height = 600,500

Grid = (24,20)
SizeSquares = 25
numBombs = 40

sizeFont = 25
font = pygame.font.Font('Freshman.ttf', sizeFont)

#create screen
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Campo Minado")

Campo = elements.Campo(screen, Grid, SizeSquares, numBombs, font)

#main loop
run = True
while run:

    Campo.drawCampo()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if event.button == 1:
                Campo.clickEsquerdo(x,y)
            elif event.button == 3:
                Campo.clickDireito(x,y)

    pygame.display.update()