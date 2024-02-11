import pygame
import Collisions as Col
import BackgroundMap as bg
import StructureClasses as SC
import GraphicsClassFunctions as GCF

def initLocs():
    pass

class Location:
    
    def __init__(self, name):
        self.name = name
        self.background = None
        self.collisions = None
        
        self.pens = []
        self.plots = []
        self.shops = []
        self.characters = []
        self.buildings = []
        self.shopModifier = 1
        self.lastPlayerX = 0
        self.lastPlayerY = 0
        
    def drawBeforePlayer(self, WIN, size):
        WIN.fill((0,0,0))
        self.background.draw(WIN)
        for i in self.plots:
            i.draw(WIN, self.background, size)             #Already checks if on screen for plots, pens
        for i in self.pens:
            i.draw(WIN, self.background, size)
        for i in self.buildings:
            i.draw(WIN, self.background, size)
    
    def drawAfterPlayer(self, WIN, size, plyr):
        if self.collisions is not None:
            self.collisions.drawObstacles(self.background, WIN, size, plyr)
        
        
def swapLoc(curr_loc, loc2, player, size):
    curr_loc.lastPlayerX = player.absx
    curr_loc.lastPlayerY = player.absy
    curr_loc.lastBGPos = (curr_loc.background.x, curr_loc.background.y)
    curr_loc = loc2
    player.absx = curr_loc.lastPlayerX
    player.absy = curr_loc.lastPlayerY
    coords = GCF.absToRelCoords((player.absx,player.absy), curr_loc.background, size)
    player.x = coords[0]
    player.y = coords[1]
    return curr_loc
