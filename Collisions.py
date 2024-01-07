import pygame
import random
import GraphicsClasses as GC
import GraphicsClassFunctions as GCF
import BackgroundMap as BG
import StructureClasses as SC
import DataFunctions as DF

# Collisions and obstacles
class Collision:
    
    def __init__(self):
        self.obsList = [None] * 10
        
        self.PermanentCollisionsX = {}

        self.PermanentCollisionsY = {}

        self.tempCollPlacements = set([(100,100), (200,200), (300,300), (400,400), (500,500), (600,600), (700,700), (800,800), (900,900), (1000,1000), (200, 100), (300,100), (500,600), (100,400), (200, 600)])
        self.tempCollPositions  = set()
        
        self.onScreenTempColl = []

    #When called, x and y coords need to be edge of player, not player x and y
    def checkColl(self, newX, newY, direction, plots=None, pens=None):
        # Check with permanent collision boxes
                                    # TODO check with list of coords
        #print(len(self.onScreenTempColl))
        #if direction == "x":
        #    if newX in self.PermanentCollisionsX:
        #        for i in self.PermanentCollisionsX[newX]:
        #            if newY > i[0] and newY < i[1]:
        #                return True, "perma"
        #if direction == "y":
        #    if newY in self.PermanentCollisionsY:
        #        for i in self.PermanentCollisionsY[newY]:
        #            if newX > i[0] and newX < i[1]:
        #                return True, "perma"
            
        # TODO Check with temp collision boxes
        for i in self.onScreenTempColl:
            temp = i.checkColl(newX, newY, direction)
            if temp[0]:
                return temp
        
        #for i in plots:
        #    temp = i.checkColl(newX, newY, direction)
        #    if temp[0]:
        #        return temp
        
        #for i in pens:
        #    temp = i.checkColl(newX, newY, direction)
        #    if temp[0]:
        #        return temp
        return False, None


    def generate(self):
        for i in range(len(self.obsList)):
            if self.obsList[i] is None:
                self.obsList[i] = Obstacle()
            if self.obsList[i].name is None:
                coords = random.choice(list(self.tempCollPlacements))
                index = random.choices([0,1,2,3,4], weights=[30,30,17,17,6])[0]
                self.obsList[i].build(coords, index)
                self.tempCollPlacements.remove(coords)
                self.tempCollPositions.add(coords)
                

    def removeFromCollision(self, inventory):
        # Mine item
        coords = (0,0)
        self.tempCollPlacements.add(coords)
        self.tempCollPositions.remove(coords)
        

    def drawObstacles(self, bg: BG.Background, window, size):
        self.onScreenTempColl = []
        for i in self.obsList:
            if i is not None and i.name is not None:
                add = i.draw(bg, window, size)
                if add:
                    self.onScreenTempColl.append(i)


class Obstacle:
    
    #TODO get this from file based on location
    types = ["smallRock", "smallTree", "largeRock", "largeTree", "massiveRock"]
    size = [(40,40), (40,40), (60,60), (60,60), (80,80)]
    drops = [("Stone", (2,4)), ("Wood", (2,4)), ("Stone", (3,6)), ("Wood", (5,8)), ("Stone", (6,10))]
    images = ["Art\Pic3.png", "Art\pic4.png", "Art\pic5.png", "Art\pic6.png", "Art\pic7.png"]

    def __init__(self):
        self.name = None
        self.absx = 0
        self.absy = 0
        self.width = 0
        self.height = 0
        self.drops = None
        self.dropQty = 0
        self.health = 20
        self.image = None
        self.onscreen = False
        
    def build(self, coords, index):
        self.name = Obstacle.types[index]
        self.absx = coords[0]
        self.absy = coords[1]
        self.width = Obstacle.size[index][0]
        self.height = Obstacle.size[index][1]
        self.drops = Obstacle.drops[index][0]
        self.dropQty = Obstacle.drops[index][1]
        self.image = pygame.image.load(Obstacle.images[index])
        self.image = pygame.transform.scale(self.image, Obstacle.size[index])
        
    def mine(self, inventory: SC.Inventory, num=None):
        if num is None:
            itm = DF.getItem(self.drops, random.choice(range(self.dropQty[0], self.dropQty[1] + 1)))
        else:
            itm = DF.getItem(self.drops, 1)
        inventory.addToInvnt(itm)
        self.name = None
        
    def draw(self, bg: BG.Background, window, size):
        coords = GCF.absToRelCoords((self.absx,self.absy), bg, size)
        self.onscreen = GCF.onScreen(coords, (self.width,self.height), size)
        if self.onscreen:
            window.blit(self.image, GCF.absToRelCoords((self.absx, self.absy), bg))
            return True
        return False
    
    def checkColl(self, newX, newY, direction):
        # needs to take in abs coords
        if direction == 'X' or direction == 'x':
            if newX == self.absx or newX == self.absx + self.width:
                for y in newY:
                    if y >= self.absy and y <= self.absy + self.height:
                        return True, self.name
        else:
            if newY == self.absy or newY == self.absy + self.height:
                for x in newX:
                    if x >= self.absx and x <= self.absx + self.width:
                        return True, self.name
        return False, None
    