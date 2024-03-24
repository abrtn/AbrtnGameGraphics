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
        player = pygame.image.load(self.images[self.animationIndex],)
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
        
    def controlPlayer(self, window_size, keys, loc):
        outStr = ""
        if keys[pygame.K_LEFT]:
            collision = loc.collisions.checkColl(self.absx, [*range(self.absy+10, self.absy+self.height, 20)],'X', loc)
            if collision is not None:
                #print("Collision: " + collision[1])
                return outStr
            if self.x <= 100 and loc.background.x < 0:
                loc.background.x += self.speed
                self.absx -= self.speed
                outStr += "l"           # lowercase if player is hitting a wall. Keeps calculation for animal rotation
            elif self.x > 0:
                self.x -= self.speed
                self.absx -= self.speed
                outStr += "L"           # uppercase if player is not hitting a wall. Moves animal location and calculates rotation
            
        if keys[pygame.K_RIGHT]:
            collision = loc.collisions.checkColl(self.absx + self.width, [*range(self.absy+10, self.absy+self.height, 20)],'X', loc)
            if collision is not None:
                #print("Collision: " + collision[1])
                return outStr
            if self.x + self.width >= window_size[0] - 100 and loc.background.x > window_size[0] - loc.background.locationData[1]:
                loc.background.x -= self.speed
                self.absx += self.speed
                outStr += "r"
            elif self.x + self.width < window_size[0]:
                self.x += self.speed
                self.absx += self.speed
                outStr += "R"
            
        if keys[pygame.K_UP]:
            collision =  loc.collisions.checkColl([*range(self.absx+10, self.absx+self.width, 20)], self.absy,'Y', loc)
            if collision is not None:
                #print("Collision: " + collision[1])
                return outStr
            if self.y <= 100 and loc.background.y < 0:
                loc.background.y += self.speed
                self.absy -= self.speed
                outStr += "u"
            elif self.y > 0:
                self.y -= self.speed
                self.absy -= self.speed
                outStr += "U"
            
        if keys[pygame.K_DOWN]:
            collision = loc.collisions.checkColl([*range(self.absx+10, self.absx+self.width, 20)], self.absy + self.height,'Y', loc)
            if collision is not None:
                #print("Collision: " + collision[1])
                return outStr
            if self.y + self.height >= window_size[1] - 100 and loc.background.y > window_size[1] - loc.background.locationData[2]:
                loc.background.y -= self.speed
                self.absy += self.speed
                outStr += "d"
            elif self.y + self.height < window_size[1]:
                self.y += self.speed
                self.absy += self.speed
                outStr += "D"
            
        return outStr
            
                
    def checkTouching(self, loc):
        collision = loc.collisions.checkColl(self.absx, [*range(self.absy+10, self.absy+self.height, 20)],'X', loc)
        if collision is not None:
            return loc.collisions.checkColl(self.absx, [*range(self.absy+10, self.absy+self.height, 20)],'X', loc)
        collision = loc.collisions.checkColl(self.absx + self.width, [*range(self.absy+10, self.absy+self.height, 20)],'X', loc)
        if collision is not None:
            return loc.collisions.checkColl(self.absx + self.width, [*range(self.absy+10, self.absy+self.height, 20)],'X', loc)
        collision = loc.collisions.checkColl([*range(self.absx+10, self.absx+self.width, 20)], self.absy,'Y', loc)
        if collision is not None:
            return loc.collisions.checkColl([*range(self.absx+10, self.absx+self.width, 20)], self.absy,'Y', loc)
        collision = loc.collisions.checkColl([*range(self.absx+10, self.absx+self.width, 20)], self.absy + self.height,'Y', loc)
        if collision is not None:
            return loc.collisions.checkColl([*range(self.absx+10, self.absx+self.width, 20)], self.absy + self.height,'Y', loc)
        return None

class Plot:
    def __init__(self):
        self.x = None
        self.y = None
        self.abs_x = None
        self.abs_y = None
        #self.location = background.locationData
        self.width = 260
        self.height = 260
        self.image = "Art/Plot.png"
        self.crops = [None] * 25
        self.cropNum = 0
        self.cropStart = None
        self.step = 35
        self.cropPos = [(4,4),(3,4),(2,4),(1,4),(0,4),
                        (4,3),(3,3),(2,3),(1,3),(0,3),
                        (4,2),(3,2),(2,2),(1,2),(0,2),
                        (4,1),(3,1),(2,1),(1,1),(0,1),
                        (4,0),(3,0),(2,0),(1,0),(0,0)]
        
        plot = pygame.image.load(self.image)
        plot = pygame.transform.scale(plot, (self.width,self.height))
        self.plot = plot
        
    def build(self, x, y, background: bg.Background):
        self.x = x
        self.y = y
        self.abs_x = x + (0-background.x)
        self.abs_y = y + (0-background.y)
        self.cropStart = [self.x + 35, self.y + 30]
        
    def draw(self, window, background: bg.Background, windowSize, x=None, y=None):
        if(x is None or y is None):
            absCoords = (self.abs_x, self.abs_y)
            coords = GCF.absToRelCoords(absCoords, background, windowSize)
            self.x = coords[0]
            self.y = coords[1]
            self.cropStart = [self.x + 35, self.y + 30]
        else:
            coords = [x, y]
            self.cropStart = [x + 35, y + 30]
        window.blit(self.plot, coords)
        
    def updateRelCoords(self, window, background: bg.Background, windowSize):
        absCoords = (self.abs_x, self.abs_y)
        coords = GCF.absToRelCoords(absCoords, background, windowSize)
        self.x = coords[0]
        self.y = coords[1]
        self.cropStart = [self.x + 35, self.y + 30]
        


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
        self.posInPlot = (0,0)
        
    def plant(self, window, posInPlot, plot: Plot):
        self.posInPlot = plot.cropPos[-posInPlot-1]
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


class Building:
    def __init__(self, name, x, y):
        self.name = name
        self.absx = x
        self.absy = y
        image = GCF.getImage(name)
        self.image = pygame.image.load(image[1])
        self.width = int(image[2])
        self.height = int(image[3])
        self.entrance = image[4].split(',')     # form [xedge1, xedge2, yedge1, yedge2], where each value is 0<width/height

    def draw(self, window, background: bg.Background, windowSize, x=None, y=None):
        if(x is None or y is None):
            absCoords = (self.absx, self.absy)
            coords = GCF.absToRelCoords(absCoords, background, windowSize)
            self.x = coords[0]
            self.y = coords[1]
        else:
            coords = [x, y]
        window.blit(self.image, coords)

    def checkColl(self, newX, newY, direction):
        # needs to take in abs coords
        if direction == 'X' or direction == 'x':
            if newX == self.absx or newX == self.absx + self.width:
                for y in newY:
                    if y >= self.absy and y <= self.absy + self.height:
                        return True
        else:
            if newY == self.absy or newY == self.absy + self.height:
                for x in newX:
                    if x >= self.absx and x <= self.absx + self.width:
                        return True
        return False

    def checkEntrance(self, newX, newY):
        for i in newX:
            if i >= self.absx + int(self.entrance[0]) and i <= self.absx + int(self.entrance[1]):
                for j in newY:
                    if j >= self.absy + int(self.entrance[2]) and j <= self.absy + int(self.entrance[3]):
                        return True
        return False