import pygame
import Collisions as Col
import BackgroundMap as bg
import StructureClasses as SC

def initLocs():
    pass

class Location:
    
    def __init__(self):
        self.name = ""
        self.background = None
        self.collisions = None
        
        self.pens = []
        self.plots = []
        self.shops = []
        self.characters = []
        self.shopModifier = 1
        
    def drawBeforePlayer(self, WIN, size):
        WIN.fill((0,0,0))
        self.background.draw(WIN)
        for i in self.plots:
            i.draw(WIN, self.background, size)             #Already checks if on screen for plots, pens
        for i in self.pens:
            i.draw(WIN, self.background, size)
    
    def drawAfterPlayer(self, WIN, size, plyr):
        self.collisions.drawObstacles(self.background, WIN, size, plyr)
        
        
        
