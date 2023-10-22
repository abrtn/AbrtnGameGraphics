import pygame
import GraphicsClassFunctions as func


class Player:
    def __init__(self,x,y,images,width,height,animated=False):
        self.x = x
        self.y = y
        self.images = images
        self.width = width
        self.height = height
        self.animationIndex = 0
        player = pygame.image.load(images[0])
        player = pygame.transform.scale(player, (width,height))
        self.player = player
        self.animated = animated
        
    def stepAnimation(self):
        player = pygame.image.load(self.images[self.animationIndex])
        player = pygame.transform.scale(player, (self.width,self.height))
        self.animationIndex += 1
        self.animationIndex %= len(self.images)
        self.player = player

    def draw(self, window, moving=False, x=None, y=None):
        if(not x or not y):
            x = self.x
            y = self.y
        else:
            self.x = x
            self.y = y
        if(self.animated and moving):
            self.stepAnimation
        
        window.blit(self.player, (x,y))
        pygame.display.update()
        

class Plot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 250
        self.height = 250
        self.image = "Art/Plot.png"
        self.crops = []
        self.cropStart = (self.x + 35, self.y + 30)
        self.step = 35
        plot = pygame.image.load(self.image)
        plot = pygame.transform.scale(plot, (self.width,self.height))
        self.plot = plot
        
    def draw(self, window, x=None, y=None):
        if(not x or not y):
            x = self.x
            y = self.y
        else:
            self.x = x
            self.y = y
        window.blit(self.plot, (x,y))
        pygame.display.update()
        
class Crop:
    def __init__(self, name):
        self.name = name
        self.width = 20
        self.height = 20
        self.images = func.getImage(name)
        self.imageIndex = 0
        crop = pygame.image.load(self.images[1])
        crop = pygame.transform.scale(crop, (self.width,self.height))
        self.crop = crop
        self.loc = None
        
    def plant(self, window, plot: Plot):
        #TODO call c++ plant
        if(len(plot.crops) >= 25):
            return
        if(not self.loc):
            self.loc = plot.cropStart
            plot.crops.append(self)
            #TODO get multiple crops
        plot.draw(window)
        window.blit(self.crop, self.loc)
        pygame.display.update()
        
    def grow(self, window, plot: Plot):
        #TODO called in c++ new day
        self.imageIndex += 1
        self.imageIndex %= len(self.images) - 1
        crop = pygame.image.load(self.images[self.imageIndex + 1])
        crop = pygame.transform.scale(crop, (self.width,self.height))
        self.crop = crop
        self.plant(window, plot)
        
    def harvest(self):
        #TODO call c++ harvest method
        self.kill