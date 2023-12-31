import pygame
import StructureClasses as SC
import GraphicsClasses as GC
import DataFunctions as DF
import GraphicsClassFunctions as GCF

class Crop:
    
    def __init__(self, name):
        self.name = name
        self.growTime = 0
        self.timeInGround = 0
        self.boostMultiplier = 1
        self.grown = False
        self.evil = False
        self.crop = GC.Crop(name)
        self.images = GCF.getImage(name)
        self.imageIndex = 0
        
    def plant(self, window, plot):
        self.crop.plant(window, plot)
        
    def harvest(self, plotG):
        self.crop.harvest(plotG)
        
    def advanceDay(self):
        if self.grown:
            return
        self.timeInGround += 1 * self.boostMultiplier
        if self.timeInGround == self.growTime // 4:
            self.crop.grow()
        if self.timeInGround >= self.growTime:
            self.crop.grow()
            self.grown = True
            
    def draw(self, window, plot):
        self.crop.draw(window, plot)
    

class Item:

    def __init__(self, name, num):
        self.name = name
        self.count = num
        self.buyCost = 0
        self.sellCost = 0
        self.type = ""
        

NULL_ITEM = DF.getItem("Null", 1)

class Animal:
    
    def __init__(self, species, name):
        self.species = species
        self.name = name
        self.buyCost = 0
        self.sellCost = 0
        self.size = 1
        self.produced = NULL_ITEM
        self.productionTime = 0
        self.onDeath = NULL_ITEM
        self.growTime = 0
        self.predatorRating = 0
        self.grown = False
        self.age = 0
        self.timeLastItem = 0
        self.timeLastFed = 0
        
    def advanceDay(self, food):
        if not self.grown:
            self.age += 1
            if self.age == self.growTime:
                self.grown = True
        self.timeLastItem += 1
        if len(food) < 1:
            self.timeLastFed += 1
            return
        self.timeLastFed = 0
        self.timeLastItem += 2
        food[0].count -= 1
        if food[0].count == 0:
            food.pop(0)
            
    def draw(self, WIN, pen):
        pass
        
    
