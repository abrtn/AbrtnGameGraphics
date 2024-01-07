import pygame
import GraphicsClassFunctions as GCF
import BackgroundMap as bg
#import Collisions as C
        

class Player:
    def __init__(self,x,y,width,height,animated=False):
        self.x = x                  #TODO fix start pos
        self.y = y
        self.absx = x
        self.absy = y
        self.images = ["Art\Test_Player.png"]
        self.speed = 20
        self.width = width
        self.height = height
        self.animationIndex = 0
        player = pygame.image.load(self.images[0])
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
        if(x is None):
            x = self.x
            y = self.y
        else:
            self.x = x
            self.y = y
        if(self.animated and moving):
            self.stepAnimation
        
        window.blit(self.player, (x,y))
        
    def controlPlayer(self, window_size, keys, background: bg.Background, coll):
        if keys[pygame.K_LEFT]:
            collision = coll.checkColl(self.absx, [*range(self.absy+10, self.absy+self.height, 20)],'X')
            if collision[0]:
                print("Collision: " + collision[1])
                return
            if self.x <= 100 and background.x < 0:
                background.x += self.speed
                self.absx -= self.speed
            elif self.x > 0:
                self.x -= self.speed
                self.absx -= self.speed
        if keys[pygame.K_RIGHT]:
            collision = coll.checkColl(self.absx + self.width, [*range(self.absy+10, self.absy+self.height, 20)],'X')
            if collision[0]:
                print("Collision: " + collision[1])
                return
            if self.x + self.width >= window_size[0] - 100 and background.x > window_size[0] - background.locationData[1]:
                background.x -= self.speed
                self.absx += self.speed
            elif self.x + self.width < window_size[0]:
                self.x += self.speed
                self.absx += self.speed
        if keys[pygame.K_UP]:
            collision =  coll.checkColl([*range(self.absx+10, self.absx+self.width, 20)], self.absy,'Y')
            if collision[0]:
                print("Collision: " + collision[1])
                return
            if self.y <= 100 and background.y < 0:
                background.y += self.speed
                self.absy -= self.speed
            elif self.y > 0:
                self.y -= self.speed
                self.absy -= self.speed
        if keys[pygame.K_DOWN]:
            collision = coll.checkColl([*range(self.absx+10, self.absx+self.width, 20)], self.absy + self.height,'Y')
            if collision[0]:
                print("Collision: " + collision[1])
                return
            if self.y + self.height >= window_size[1] - 100 and background.y > window_size[1] - background.locationData[2]:
                background.y -= self.speed
                self.absy += self.speed
            elif self.y + self.height < window_size[1]:
                self.y += self.speed
                self.absy += self.speed
                
        #print(str(self.absx) + ", " + str(self.absy) + " : " + str(self.x) + ", " + str(self.y))


class Plot:
    def __init__(self, x, y, background: bg.Background, windowSize):
        self.x = x
        self.y = y
        self.abs_x = x + (0-background.x)
        self.abs_y = y + (0-background.y)
        self.location = background.locationData
        self.width = 250
        self.height = 250
        self.image = "Art/Plot.png"
        self.crops = []
        self.cropNum = 0
        self.cropStart = [self.x + 35, self.y + 30]
        self.step = 35
        self.next_empty = 24
        self.cropPos = [(4,4),(3,4),(2,4),(1,4),(0,4),
                        (4,3),(3,3),(2,3),(1,3),(0,3),
                        (4,2),(3,2),(2,2),(1,2),(0,2),
                        (4,1),(3,1),(2,1),(1,1),(0,1),
                        (4,0),(3,0),(2,0),(1,0),(0,0)]
        
        plot = pygame.image.load(self.image)
        plot = pygame.transform.scale(plot, (self.width,self.height))
        self.plot = plot
        
    def draw(self, window, background: bg.Background, windowSize, x=None, y=None):
        if(x is None or y is None):
            absCoords = (self.abs_x, self.abs_y)
            coords = GCF.absToRelCoords(absCoords, background, windowSize)
        self.x = coords[0]
        self.y = coords[1]
        self.cropStart = [self.x + 35, self.y + 30]
        window.blit(self.plot, coords)
        
    def updateRelCoords(self, window, background: bg.Background, windowSize):
        absCoords = (self.abs_x, self.abs_y)
        coords = GCF.absToRelCoords(absCoords, background, windowSize)
        self.x = coords[0]
        self.y = coords[1]
        self.cropStart = [self.x + 35, self.y + 30]
        

class Pen:
    def __init__(self, x, y, background: bg.Background, windowSize):
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
    
    def draw(self, window, background: bg.Background, windowSize, x=None, y=None):
        if(x is None or y is None):
            absCoords = (self.abs_x, self.abs_y)
            coords = GCF.absToRelCoords(absCoords, background, windowSize)
        self.x = coords[0]
        self.y = coords[1]
        window.blit(self.plot, coords)
        
    def updateRelCoords(self, window, background: bg.Background, windowSize):
        absCoords = (self.abs_x, self.abs_y)
        coords = GCF.absToRelCoords(absCoords, background, windowSize)
        self.x = coords[0]
        self.y = coords[1]


class Crop:
    def __init__(self, name):
        self.name = name
        self.width = 20
        self.height = 20
        self.images = GCF.getImage(name)
        self.imageIndex = 0
        crop = pygame.image.load(self.images[1])
        crop = pygame.transform.scale(crop, (self.width,self.height))
        self.crop = crop
        self.loc = [-100, -100]
        self.cropNumInPlot = 0
        self.posInPlot = (0,0)
        
    def plant(self, window, plot: Plot):
        self.cropNumInPlot = plot.cropNum
        self.posInPlot = plot.cropPos[plot.next_empty]
        #plot.cropPos.pop()
        self.loc[0] = plot.cropStart[0] + (plot.step * self.posInPlot[0])
        self.loc[1] = plot.cropStart[1] + (plot.step * self.posInPlot[1])
        plot.cropNum += 1
        window.blit(self.crop, self.loc)
        
    def draw(self, window, plot:Plot):
        self.loc[0] = plot.cropStart[0] + (plot.step * self.posInPlot[0])
        self.loc[1] = plot.cropStart[1] + (plot.step * self.posInPlot[1])
        window.blit(self.crop, self.loc)
        
    def grow(self):
        self.imageIndex += 1
        self.imageIndex %= len(self.images) - 1
        crop = pygame.image.load(self.images[self.imageIndex + 1])
        crop = pygame.transform.scale(crop, (self.width,self.height))
        self.crop = crop
        
        

class Animal:
    def __init__(self, name):
        self.name = name
        self.width = 20
        self.height = 20
        self.images = GCF.getImage(name)
        self.imageIndex = 0
        anm = pygame.image.load(self.images[1])
        anm = pygame.transform.scale(anm, (self.width,self.height))
        self.anm = anm
        self.loc = [-100, -100]
        self.anmNumInPen = 0