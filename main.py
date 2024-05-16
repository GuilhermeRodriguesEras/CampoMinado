import pygame
import elements

pygame.init()

#size screen
screen_width, screen_height = 600,500

Grid = (24,20)
SizeSquares = 25
numBombs = 99

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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if event.button == 1:
                Campo.clickEsquerdo(x,y)
            elif event.button == 3:
                Campo.clickDireito(x,y)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                Campo = elements.Campo(screen, Grid, SizeSquares, numBombs, font)

    pygame.display.update()