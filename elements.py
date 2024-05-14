import pygame
import random

class Campo():
    def __init__(self, surface, gridSize, sizeSquares, numBombs, font):

        self.surface = surface
        self.gridSize = gridSize
        self.sizeSquares = sizeSquares
        self.firstClick = False
        self.numBombs = numBombs
        self.font = font

        self.end = False

        self.countSquares = self.gridSize[0] * self.gridSize[1]
        self.countBandeiras = self.numBombs
        self.bombsList = []

        print(self.countSquares)

        self.bomb_image = pygame.image.load("imgs/bomba.png").convert_alpha()
        self.bomb_image = pygame.transform.scale(self.bomb_image, (self.sizeSquares, self.sizeSquares))

        self.bandeira_image = pygame.image.load("imgs/bandeira.png").convert_alpha()
        self.bandeira_image = pygame.transform.scale(self.bandeira_image, (self.sizeSquares, self.sizeSquares))

        self.colorsGrid = [(170, 215, 81), (162, 209, 73), (229, 194, 159),(215, 184, 153)]
        self.colorNumbers = [(51,51, 255), (0, 255, 128), (255, 51, 51), (127, 0, 255), (89, 95, 47)]

        self.auxMatriz = [[0 for _ in range(self.gridSize[0])] for _ in range(self.gridSize[1])]
        self.matriz = [[Quadrado(self.colorsGrid[(i+j)%2], (i+j)%2) for i in range(self.gridSize[0])] for j in range(self.gridSize[1])]


    def drawCampo(self):
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[0])):
                self.matriz[i][j].drawQuadrado(self.surface, j*self.sizeSquares, i*self.sizeSquares, self.sizeSquares, self.sizeSquares, self.bomb_image, self.bandeira_image)

    def clickEsquerdo(self, x, y):
        i = y//self.sizeSquares
        j = x//self.sizeSquares

        if not self.matriz[i][j].showed and not self.end and not self.matriz[i][j].bandeira:

            if not self.firstClick:
                self.firstClick = True
                self.randomizeGrid(i, j)

            if self.matriz[i][j].value == 0:
                #self.auxMatriz = [[0 for _ in range(self.gridSize[0])] for _ in range(self.gridSize[1])]
                self.clickNoZero(i, j)
            elif self.matriz[i][j].value == 10:
                self.defeat(self.bombsList)
            else:
                self.matriz[i][j].changeQuadrado(self.colorsGrid)
                self.auxMatriz[i][j] = 1
                self.countSquares -= 1

            print(self.countSquares)

            if self.countSquares == self.numBombs:
                self.win()

    def clickDireito(self, x, y):
        i = y//self.sizeSquares
        j = x//self.sizeSquares

        if not self.matriz[i][j].showed and not self.end:
            if self.matriz[i][j].bandeira:
                self.matriz[i][j].bandeira = not self.matriz[i][j].bandeira
                self.countBandeiras +=1
            elif self.countBandeiras > 0:
                self.matriz[i][j].bandeira = not self.matriz[i][j].bandeira
                self.countBandeiras -= 1

    def randomizeGrid(self, i, j):

        excluse = [(u, v) for u in range(i - 1, i + 2) for v in range(j - 1, j + 2) if 0 <= u < self.gridSize[1] and 0 <= v < self.gridSize[0]]
        temp = list(map(lambda pos: pos[0]*self.gridSize[0] + pos[1], excluse))

        lista = [i for i in range(self.gridSize[0]*self.gridSize[1]) if i not in temp]
        self.bombsList = random.sample(lista, self.numBombs)

        self.defineSqureValues(self.bombsList)

    def defineSqureValues(self, bombList):
        convert = lambda num: (num//self.gridSize[0], num%self.gridSize[0])
        indexColor = lambda num: num-1 if num<=5 else 4

        for x in bombList:
            pos = convert(x)
            self.matriz[pos[0]][pos[1]].value = 10

            for u in range(pos[0]-1, pos[0]+2):
                for v in range(pos[1]-1,pos[1]+2):
                    if 0 <= u < self.gridSize[1] and 0 <= v < self.gridSize[0] and self.matriz[u][v].value != 10:
                        self.matriz[u][v].value +=1

        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[0])):
                self.matriz[i][j].setText(self.colorNumbers[indexColor(self.matriz[i][j].value)], self.font)


    def clickNoZero(self, i, j):
            self.matriz[i][j].changeQuadrado(self.colorsGrid)
            self.auxMatriz[i][j] = 1
            self.countSquares -= 1

            if self.matriz[i][j].value == 0:
                for u in range(i-1, i+2):
                    for v in range(j-1,j+2):
                        if 0 <= u < self.gridSize[1] and 0 <= v < self.gridSize[0] and self.auxMatriz[u][v] != 1:
                            self.clickNoZero(u,v)
                
    def defeat(self, bomblist):
        self.end = True
        print("lose :(")

        convert = lambda num: (num//self.gridSize[0], num%self.gridSize[0])

        for x in bomblist:
            i, j = convert(x)
            self.matriz[i][j].changeQuadrado(self.colorsGrid)

    def win(self):
        self.end = True
        print("win")

    
    def printCampo(self):
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[0])):
                print(f"[{self.matriz[i][j].value}] ", end="")
            print()


class Quadrado():
    def __init__(self, color, atualColor, value = 0):
        self.color = color
        self.value = value
        self.atualColor = atualColor
        self.bandeira = False
        self.showed = False
        self.txtDraw = None

    def drawQuadrado(self, surface, x, y, xsize, ysize, bombImage, bandeiraImage):
        pygame.draw.rect(surface, self.color, pygame.Rect(x,y,xsize,ysize))
        
        if self.showed:
            if self.value != 0 and self.value != 10:
                surface.blit(self.txtDraw, (x+4, y))
        
            elif self.value == 10:
                surface.blit(bombImage, (x,y))

        if self.bandeira:
            surface.blit(bandeiraImage, (x,y))

    def changeQuadrado(self, listColors):
        if(not self.showed and not self.bandeira):
            self.showed = True
            if self.value != 10:
                self.color = listColors[self.atualColor + 2]
            else:
                self.color = (247, 5, 37)

        if self.bandeira and self.value == 10:
            self.color = (247, 5, 37)

    def setText(self, color, font):
        self.txtDraw = font.render(str(self.value), True, color)