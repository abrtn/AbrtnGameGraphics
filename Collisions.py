import pygame
import random
import GraphicsClasses as GC
import GraphicsClassFunctions as GCF
import BackgroundMap as BG
import StructureClasses as SC
import DataFunctions as DF

# Collisions and obstacles
class Collision:
    
    canopy = pygame.image.load("Art\Canopy.png")
    canopy = pygame.transform.scale(canopy, (300,300))
    canopyTransp = pygame.image.load("Art\CanopyTransparent.png")
    canopyTransp = pygame.transform.scale(canopyTransp, (300,300))
    
    def __init__(self):
        self.obsList = [None] * 10
        
        self.PermanentCollisionsX = {}

        self.PermanentCollisionsY = {}

        self.tempCollPlacements = set([(100,100), (200,200), (300,300), (400,400), (500,500), (600,600), (700,700), (800,800), (900,900), (1000,1000), (200, 100), (300,100), (500,600), (100,400), (200, 600)])
        self.tempCollPositions  = set()
        
        self.onScreenTempColl = []
        
        self.canopy = {}

    #When called, x and y coords need to be edge of player, not player x and y
    def checkColl(self, newX, newY, direction, loc):
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
            if i.checkColl(newX, newY, direction):
                return i
        
        for j in loc.plots:
            if j.checkColl(newX, newY, direction):
                return j
        
        for i in loc.pens:
            if i.checkColl(newX, newY, direction):
                return i

        for i in loc.buildings:
            if i.checkColl(newX, newY, direction):
                return i
        return None


    def generate(self):                     # TODO take in location and change generated obs based on loc
        for i in range(len(self.obsList)):
            if self.obsList[i] is None:
                self.obsList[i] = Obstacle()
            if self.obsList[i].name is None:
                coords = random.choice(list(self.tempCollPlacements))
                index = random.choices([0,1,2,3,4], weights=[30,30,17,17,6])[0]
                self.obsList[i].build(coords, index)
                self.tempCollPlacements.remove(coords)
                self.tempCollPositions.add(coords)
                

    def removeFromCollision(self, obst, inventory):
        # Mine item
        coords = (obst.absx, obst.absy)
        obst.mine(inventory)
        self.tempCollPlacements.add(coords)
        self.tempCollPositions.remove(coords)
        

    def drawObstacles(self, bg: BG.Background, window, size, player):
        canopies = []
        self.onScreenTempColl = []
        for i in self.obsList:
            if i is not None and i.name is not None:
                add = i.draw(bg, window, size, canopies)
                if add:
                    self.onScreenTempColl.append(i)
        transp = []
        canopy = set()
        if player is not None:
            for i in canopies:
                if GCF.checkInside(i, 300, 300, (player.x,player.y), player.width, player.height):
                    transp.append(i)
                else:
                    canopy.add(i)
            for i in transp:
                window.blit(Collision.canopyTransp, i)
                for j in list(canopy):
                    if GCF.checkInside(j, 300, 300, i, 300, 300):
                        transp.append(j)
                        canopy.remove(j)
            for i in canopy:
                window.blit(Collision.canopy, i)
        else:
            for i in canopies:
                window.blit(Collision.canopyTransp, i)


class Obstacle:
    
    #TODO get this from file based on location
    types = ["smallRock", "smallTree", "largeRock", "largeTree", "massiveRock"]
    size = [(40,40), (40,40), (60,60), (60,60), (80,80)]
    drops = [("Stone", (2,4)), ("Wood", (2,4)), ("Stone", (3,6)), ("Wood", (5,8)), ("Stone", (6,10))]
    images = ["Art\small_rock.png", "Art\small_tree.png", "Art\large_rock.png", "Art\large_tree.png", "Art\massive_rock.png"]

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
        self.canopyTransp = False
        
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
        #inventory.addToInvnt(itm)                  Temporarily disabled
        self.name = None
        
    def draw(self, bg: BG.Background, window, size, canopies):
        coords = GCF.absToRelCoords((self.absx,self.absy), bg, size)
        self.onscreen = GCF.onScreen(coords, (self.width,self.height), size)
        if self.onscreen:
            window.blit(self.image, GCF.absToRelCoords((self.absx, self.absy), bg))
            if self.name == "smallTree" or self.name == "largeTree":
                canopies.append(tuple([coords[0]-((300-self.width)//2), coords[1]-((300-self.width)//2)]))
            return True
        return False
    
    def checkColl(self, newX, newY, direction):
        # needs to take in abs coords
        if direction == 'X' or direction == 'x':
            if newX == self.absx or newX == self.absx + self.width:
                for y in newY:
                    if y >= self.absy and y <= self.absy + self.height:
                        return True
        else:
            if newY == self.absy or newY == self.absy + self.height:
                for x in newX:
                    if x >= self.absx and x <= self.absx + self.width:
                        return True
        return False
