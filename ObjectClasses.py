import pygame
import StructureClasses as SC

class Crop:
    
    def __init__(self, name, num):
        self.name = name
        self.count = num
        self.growTime
        self.timeInGround = 0
        self.boostMultiplier = 1
        self.grown = False
        self.evil = False
        
    def advanceDay(self):
        pass
    

class Item:

    def __init__(self, name, num):
        self.name = name
        self.count = num
        self.buyCost
        self.sellCost
        self.type
        

class Animal:
    
    def __init__(self, species, name):
        self.species = species
        self.name = name
        self.buyCost
        self.sellCost
        self.produced
        self.productionTime
        self.onDeath
        self.growTime
        self.predatorRating
        self.grown = False
        self.age = 0
        self.timeLastItem = 0
        self.timeLastFed = 0
        #self.evil = False          Maybe not needed
        
    
