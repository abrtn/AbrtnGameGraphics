import pygame
import GraphicsClassFunctions as func

LOCATIONS = {
    "Test" : ["Art\Field.png", 12000, 7500],
    "mapTest" : ["Art\mapTest.png", 2560, 1279]
    }

class Background:
    def __init__(self, location, x, y):
        self.location = location
        self.x = x
        self.y = y
        self.maps = LOCATIONS
        self.locationData = self.maps[self.location]
        bg = pygame.image.load(self.locationData[0])
        bg = pygame.transform.scale(bg, (self.locationData[1],self.locationData[2]))
        self.background = bg
     
    def draw(self, window):
        window.blit(self.background, (self.x, self.y))
        
    def changeLoc(self, window):
        #TODO?
        pass
