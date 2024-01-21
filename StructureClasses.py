import pygame
import ObjectClasses as OC
import DataFunctions as DF
import GraphicsClasses as GC
import GraphicsClassFunctions as GCF
import BackgroundMap as bg

NULL_CROP = DF.getCrop("Null_Crop", 1)
NULL_ITEM = DF.getItem("Null_Item", 1)

class Inventory:
        
    def __init__(self, gold=None):
        self.capacity = 30
        self.inventory = [NULL_ITEM] * self.capacity
        self.emptySpots = [i for i in range(self.capacity -1, -1, -1)]
        self.gold = gold
        
    
    def clearEmpty(self):
        for i in range(len(self.inventory) - 1, -1, -1):
            if self.inventory[i].count == 0:
                self.inventory[i] = NULL_ITEM
                self.emptySpots.append(i)
    
    def addToInvnt(self, itm: OC.Item):                 #TODO deal with full invnt
        for i in self.inventory:
            if i.name == itm.name:
                i.count += itm.count
                return
        self.inventory[self.emptySpots[-1]] = itm
        self.emptySpots.pop()
        
    


class Plot:
    
    def __init__(self):
        self.capacity = 25
        self.numCrops = 0
        self.crops = []
        self.emptySpots = [i for i in range(self.capacity)]
        self.plot = None
        
    def build(self, x, y, background, size, window):
        self.plot = GC.Plot(x, y, background, size)
        #self.plot.draw(window, background, size)
        self.crops = [NULL_CROP] * self.capacity
        
    def newDay(self):
        for i in self.crops:
            i.advanceDay()
    
    def plant(self, name, i, invnt: Inventory, window):
        #for i in range(len(invnt.inventory)):               #i is item class
        #    if invnt.inventory[i].name == name: #+ "_Seed":                
                #TODO plant multiple at once
                if self.numCrops < self.capacity:
                    self.crops[self.emptySpots[-1]] = DF.getCrop(name.split('_')[0])

                    self.plot.crops.append(self.crops[self.emptySpots[-1]].crop)
                    
                    self.plot.next_empty = self.emptySpots[-1]
                    self.crops[self.emptySpots[-1]].plant(window, self.plot)

                    self.emptySpots.pop()
                    self.numCrops += 1
                    invnt.inventory[i].count -= 1
                    invnt.clearEmpty()
                    return
                
    def draw(self, window, background, size, x=None, y=None):
        if GCF.onScreen((self.plot.x, self.plot.y), (self.plot.width,self.plot.height), size):
            self.plot.draw(window, background, size, x=x, y=y)
            if self.plot.cropNum == 0:
                return
            for i in range(len(self.crops)):
                if self.crops[i].name != "Null_Crop":
                    self.crops[i].draw(window, self.plot)
        else:
            self.plot.updateRelCoords(window, background, size)
          
    
    def harvest(self, invnt: Inventory):
        for i in range(len(self.crops)):
            if self.crops[i].grown:
                invnt.addToInvnt(DF.getItem(self.crops[i].name, 1))
                self.plot.cropPos.append(self.crops[i].crop.posInPlot)
                self.crops[i] = NULL_CROP
                self.numCrops -= 1
                self.emptySpots.append(i)
                self.emptySpots.sort()
                
    
    def boost(self, mult):              #TODO
        for i in self.crops:
            if i.boostMultiplier < mult:
                i.boostMultiplier = mult

    def checkColl(self, newX, newY, direction):
        # needs to take in abs coords
        if direction == 'X' or direction == 'x':
            if newX == self.plot.abs_x or newX == self.plot.abs_x + self.plot.width:
                for y in newY:
                    if y >= self.plot.abs_y and y <= self.plot.abs_y + self.plot.height:
                        return True
        else:
            if newY == self.plot.abs_y or newY == self.plot.abs_y + self.plot.height:
                for x in newX:
                    if x >= self.plot.abs_x and x <= self.plot.abs_x + self.plot.width:
                        return True
        return False



class Pen:
    
    def __init__(self):
        self.animals = []
        self.food = []
        self.capacity = 5
        self.spaceFilled = 0
        self.names = set()
        self.animalStart = (0,0)
        self.x = 0
        self.y = 0
        self.abs_x = 0
        self.abs_y = 0
        self.width = 400
        self.height = 260
        self.image = "Art/Pen.png"
        pen = pygame.image.load(self.image)
        pen = pygame.transform.scale(pen, (self.width,self.height))
        self.pen = pen
        self.rotated = False
        
    def build(self, x, y, background, size, window):
        self.x = x
        self.y = y
        self.abs_x = x + (0-background.x)
        self.abs_y = y + (0-background.y)
        self.animalStart = (x+20, y+20)
    
    def draw(self, window, background: bg.Background, windowSize, x=None, y=None):
        # Animal size of 1 is 52x150
        # For size of i, image size is (52*i)+(20*(i-1))x150
            # doubles size and adds the 20 pixels in between
        if GCF.onScreen((self.x, self.y), (self.width,self.height), windowSize):
            if(x is None or y is None):
                absCoords = (self.abs_x, self.abs_y)
                coords = GCF.absToRelCoords(absCoords, background, windowSize)
                self.x = coords[0]
                self.y = coords[1]
                self.animalStart = (self.x+20, self.y+20)
            else:
                coords = [x, y]
                self.animalStart = (x+20, y+20)
            window.blit(self.pen, coords)
            if self.spaceFilled == 0:
                return
            j = 0
            for i in range(len(self.animals)):
                if self.animals[i].name != "Null_Animal":
                    self.animals[i].draw(window, self.animalStart, j)
                    j += self.animals[i].size
        else:
            self.updateRelCoords(background, windowSize)
        
        
    def updateRelCoords(self, background: bg.Background, windowSize):
        absCoords = (self.abs_x, self.abs_y)
        coords = GCF.absToRelCoords(absCoords, background, windowSize)
        self.x = coords[0]
        self.y = coords[1]
    
    def newDay(self):
        for i in self.animals:
            i.advanceDay(self.food)
    
    def addAnimal(self, anmlType, name, invnt: Inventory = None):
        anml = DF.getAnimal(anmlType, name)
        print(anml.species)
        if self.spaceFilled + anml.size > self.capacity:
            return
        #if invnt.gold < anml.buyCost:
        #    return
        if name in self.names:
            return
        self.names.add(name)
        #invnt.gold -= anml.buyCost
        self.animals.append(anml)
        print(len(self.animals))
        self.spaceFilled += anml.size
        print(self.spaceFilled)
        
    def milk(self, invnt: Inventory):
        for i in self.animals:
            if i.produced.name == "Null":
                continue
            if i.timeLastItem < i.productionTime:
                continue
            i.timeLastItem = 0
            invnt.addToInvnt(i.produced)
            
    def butcher(self, name, invnt: Inventory):
        for i in range(len(self.animals)):
            if self.animals[i].name == name:
                if self.animals[i].onDeath.name != "Null":
                    invnt.addToInvnt(self.animals[i].onDeath)
                self.names.remove(name)
                self.animals.pop(i)
                return
            
    def feed(self, item, invnt: Inventory, count):
        if len(self.food) >= 3:
            return
        for i in invnt.Inventory:
            if i.name == item:
                if i.count < count:
                    count = i.count
                i.count -= count
                itm = DF.getItem(item, count)
                self.food.append(itm)
                invnt.clearEmpty()
                return
            
    def checkColl(self, newX, newY, direction):
        # needs to take in abs coords
        if direction == 'X' or direction == 'x':
            if newX == self.abs_x or newX == self.abs_x + self.width:
                for y in newY:
                    if y >= self.abs_y and y <= self.abs_y + self.height:
                        return True
        else:
            if newY == self.abs_y or newY == self.abs_y + self.height:
                for x in newX:
                    if x >= self.abs_x and x <= self.abs_x + self.width:
                        return True
        return False
                
