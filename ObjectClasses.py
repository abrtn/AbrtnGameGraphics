from itertools import filterfalse
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
        self.images = GCF.getImage(species)
        self.imageIndex = 1
        self.animal = pygame.image.load(self.images[self.imageIndex])
        
    def advanceDay(self, food):
        if not self.grown:
            self.age += 1
            if self.age == self.growTime:
                self.grown = True
                self.imageIndex = 2
                self.animal = pygame.image.load(self.images[self.imageIndex])
        self.timeLastItem += 1
        if len(food) < 1:
            self.timeLastFed += 1
            return
        self.timeLastFed = 0
        self.timeLastItem += 2
        food[0].count -= 1
        if food[0].count == 0:
            food.pop(0)
            
    def draw(self, WIN, animalStart, i, rotation):
        # Animal size of 1 is 52x150 pixels
        # For size of i, image size is (52*i)+(20*(i-1))x150 pixels
            # doubles size and adds the 20 pixels in between

        # fix coords of animal incrementing so can go from bottom up
        if rotation % 4 == 0:
            coords = [animalStart[0] + (i * 72), animalStart[1]]
        elif rotation % 4 == 1:
            coords = [animalStart[0], animalStart[1] + (i * 72)]
        elif rotation % 4 == 2:
            coords = [animalStart[0] - (i * 72) - (self.size * 72), animalStart[1] - 150]
        elif rotation % 4 == 3:
            coords = [animalStart[0], animalStart[1] - (i * 72) - (self.size * 72)]

        animal = pygame.transform.rotate(self.animal, rotation * -90)
        WIN.blit(animal, coords)
        
    
