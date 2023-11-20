import pygame
import ObjectClasses as OC
import DataFunctions as DF
import GraphicsClasses as GC
import GraphicsClassFunctions as GCF

NULL_CROP = DF.getCrop("Null_Crop", 1)
NULL_ITEM = DF.getItem("Null_Item", 1)

class Inventory:
    
    #TODO same as with plot, fill empty spots with null item and keep track of empty when adding or removing
    
    def __init__(self):
        self.capacity = 30
        self.inventory = [NULL_ITEM] * self.capacity
        self.emptySpots = [i for i in range(self.capacity -1, -1, -1)]
        
    
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
    
    def __init__(self):
        self.animals = []
        self.food = []
        self.capacity = 5
