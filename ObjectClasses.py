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
        self.alignment = "-"
        

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
        self.food = None
        self.eats = ""
        self.timeLastItem = 0
        self.timeLastFed = 0
        self.images = GCF.getImage(species)
        self.imageIndex = 1
        self.alignment = "Neutral"
        self.dataIndex = 0
        self.animal = pygame.image.load(self.images[self.imageIndex])
        
    def advanceDay(self):
        if not self.grown:
            self.age += 1
            if self.age == self.growTime:
                self.grown = True
                self.imageIndex = 2
                self.animal = pygame.image.load(self.images[self.imageIndex])
        self.timeLastItem += 1
        if self.food is None:
            self.timeLastFed += 1
            return
        self.timeLastFed = 0
        self.timeLastItem += 2

        # check if alignment changes
        if not self.grown:
            self.food[1] -= 1
            if self.food[1] == 0:
                self.food = None
            return
        
        if self.alignment != self.food[2]:                  # TODO get image change when alignment changes
            if self.alignment != "Neutral" and self.food[2] != "Neutral":
                self.alignment = "Neutral"
                #self.imageIndex = 1
            elif self.alignment == "Neutral":
                self.alignment = self.food[2]
                #if self.alignment == "Evil":
                #    self.imageIndex = 2
                #else:
                #    self.imageIndex = 3
            

        self.food[1] -= 1
        if self.food[1] == 0:
            self.food = None
            
    def draw(self, WIN, animalStart, i, rotation, x=None, y=None):
        # Animal size of 1 is 52x150 pixels
        # For size of i, image size is (52*i)+(20*(i-1))x150 pixels
            # doubles size and adds the 20 pixels in between

        # fix coords of animal incrementing so can go from bottom up
        if x is None or y is None:
            if rotation % 4 == 0:
                coords = [animalStart[0] + (i * 72), animalStart[1]]
            elif rotation % 4 == 1:
                coords = [animalStart[0], animalStart[1] + (i * 72)]
            elif rotation % 4 == 2:
                coords = [animalStart[0] - (i * 72) - (self.size * 72), animalStart[1] - 150]
            elif rotation % 4 == 3:
                coords = [animalStart[0], animalStart[1] - (i * 72) - (self.size * 72)]
        else:
            coords = (x,y)

        animal = pygame.transform.rotate(self.animal, rotation * -90)
        WIN.blit(animal, coords)
    
    def feed(self, item: Item):
        if self.food is not None:
            if item.name == self.food[0] and self.food[1] < 9:
                self.food[1] += 1
                return True
            return False
        if self.eats == item.type:
            self.food = [item.name, 1, item.alignment]
            return True
        return False
                
        
    
