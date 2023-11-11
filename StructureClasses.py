import pygame
import ObjectClasses as OC


class Inventory:
    
    def __init__(self):
        self.inventory = []
        self.capacity = 30


class Plot:
    
    def __init__(self):
        self.crops = []
        self.capacity = 25
        self.numCrops = 0
        
    def newDay(self):
        pass
    
    def plant(self):
        pass
    
    def harvest(self):
        pass
    
    def boost(self):
        pass


class Pen:
    
    def __init__(self):
        self.animals = []
        self.food = []
        self.capacity = 5
