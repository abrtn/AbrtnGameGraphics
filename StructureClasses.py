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
    
    def __init__(self, window):
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
    
    def plant(self, name, num, invnt: Inventory, window):
        for i in range(len(invnt.inventory)):               #i is item class
            if invnt.inventory[i].name == name + "_Seed":                
                #TODO plant multiple at once
                if self.numCrops < self.capacity:
                    self.crops[self.emptySpots[-1]] = DF.getCrop(name)

                    self.plot.crops.append(self.crops[self.emptySpots[-1]].crop)
                    self.plot.cropNum += 1
                    
                    self.plot.next_empty = self.emptySpots[-1]
                    self.crops[self.emptySpots[-1]].plant(window, self.plot)

                    self.emptySpots.pop()
                    self.numCrops += 1
                    invnt.inventory[i].count -= 1
                    invnt.clearEmpty()
                    return
                
    def draw(self, window, background, size):
        if GCF.onScreen((self.plot.x, self.plot.y), (self.plot.width,self.plot.height), size):
            self.plot.draw(window, background, size)
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
                
    
    def boost(self, mult):
        for i in self.crops:
            if i.boostMultiplier < mult:
                i.boostMultiplier = mult



class Pen:
    
    def __init__(self, x, y, background: bg.Background, windowSize):
        self.animals = []
        self.food = []
        self.capacity = 5
        self.spaceFilled = 0
        self.names = {}
        self.x = x
        self.y = y
        self.abs_x = x + (0-background.x)
        self.abs_y = y + (0-background.y)
        self.location = background.locationData
        self.width = 250
        self.height = 250
        self.image = "Art/Pen.png"
        pen = pygame.image.load(self.image)
        pen = pygame.transform.scale(pen, (self.width,self.height))
        self.pen = pen
        
    def build(self, x, y, background, size, window):
        self.x = x
        self.y = y
    
    def draw(self, window, background: bg.Background, windowSize, x=None, y=None):      #TODO
        pass
        
    def updateRelCoords(self, window, background: bg.Background, windowSize):
        absCoords = (self.abs_x, self.abs_y)
        coords = GCF.absToRelCoords(absCoords, background, windowSize)
        self.x = coords[0]
        self.y = coords[1]
    
    def newDay(self):
        for i in self.animals:
            i.advanceDay(self.food)
    
    def addAnimal(self, anmlType, name, invnt: Inventory):
        anml = DF.getAnimal(anmlType, name)
        if self.spaceFilled + anml.size > self.capacity:
            return
        if invnt.gold < anml.buyCost:
            return
        if name in self.names:
            return
        self.names.add(name)
        invnt.gold -= anml.buyCost
        self.animals.append(anml)
        self.spaceFilled += anml.size
        
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
                
