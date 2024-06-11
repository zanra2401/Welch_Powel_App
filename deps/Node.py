import pygame

class Node():
    def __init__(self, pos):
        self.pos = pos;
        self.collor = (0,0,0)
        self.rad = 20
        self.name = None
        self.edges = 0
        self.linked_to = []
        self.font = pygame.font.Font(None, 30)
    def drawNode(self, win):
        pygame.draw.circle(win, self.collor, self.pos, self.rad)
        text = self.font.render(str(self.name), True, (255,255,255))
        win.blit(text, ((self.pos[0] - self.rad) + self.rad//2, (self.pos[1] - self.rad) + self.rad//2))
    
    def setCollor(self, color):
        self.collor = color
    
    def setName(self, name):
        self.name = name