import pygame
import ObjectClasses as OC
import DataFunctions as DF
import GraphicsClasses as GC
import GraphicsClassFunctions as GCF
import BackgroundMap as bg

NULL_CROP = DF.getCrop("Null_Crop", 1)
NULL_ITEM = DF.getItem("Null_Item", 1)

class Inventory:
        
    def __init__(self, use, gold=None):
        self.capacity = 30
        self.inventory = [NULL_ITEM] * self.capacity
        self.emptySpots = [i for i in range(self.capacity -1, -1, -1)]
        self.gold = gold
        self.type = use
        
    
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
    
    def __init__(self):
        self.capacity = 25
        self.numCrops = 0
        self.crops = []
        self.emptySpots = [i for i in range(self.capacity)]
        self.plot = GC.Plot()
        self.width = 260
        self.height = 260
        
    def build(self, x, y, background, size, window, rotation=None):
        self.plot.build(x, y, background)
        #self.plot.draw(window, background, size)
        self.crops = [NULL_CROP] * self.capacity
        
    def newDay(self):
        for i in self.crops:
            if i.name != "Null_Crop":
                i.advanceDay()
    
    def plant(self, name, i, j, invnt: Inventory, window):
        #for i in range(len(invnt.inventory)):               #i is item class
        #    if invnt.inventory[i].name == name: #+ "_Seed":                
                if self.numCrops < self.capacity:
                    self.crops[j] = DF.getCrop(name.split('_')[0])

                    self.plot.crops[j] = self.crops[j].crop
                    
                    #self.plot.next_empty = self.emptySpots[-1]
                    self.crops[j].plant(window, j, self.plot)

                    #self.emptySpots.pop()
                    self.numCrops += 1
                    invnt.inventory[i].count -= 1
                    invnt.clearEmpty()
                    return
                
    def draw(self, window, background, size, x=None, y=None, rotation=None, bypass=False):
        if bypass or GCF.onScreen((self.plot.x, self.plot.y), (self.plot.width,self.plot.height), size):
            self.plot.draw(window, background, size, x=x, y=y)
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

    def checkColl(self, newX, newY, direction):
        # needs to take in abs coords
        if direction == 'X' or direction == 'x':
            if newX == self.plot.abs_x or newX == self.plot.abs_x + self.plot.width:
                for y in newY:
                    if y >= self.plot.abs_y and y <= self.plot.abs_y + self.plot.height:
                        return True
        else:
            if newY == self.plot.abs_y or newY == self.plot.abs_y + self.plot.height:
                for x in newX:
                    if x >= self.plot.abs_x and x <= self.plot.abs_x + self.plot.width:
                        return True
        return False



class Pen:
    
    #TODO maybe? get animals to space out like crops when removed and fill in empty spots
    
    def __init__(self):
        self.animals = []
        self.capacity = 5
        self.spaceFilled = 0
        self.names = set()
        self.animalStart = (0,0)
        self.x = 0
        self.y = 0
        self.abs_x = 0
        self.abs_y = 0
        self.width = 400
        self.height = 260
        self.image = "Art/Pen.png"
        self.rotation = 0
        pen = pygame.image.load(self.image)
        pen = pygame.transform.scale(pen, (self.width,self.height))
        pen = pygame.transform.rotate(pen, -90 * self.rotation)
        self.penUnRot = pen
        self.pen = pen
        
    def build(self, x, y, background, size, window, rotation):
        self.x = x
        self.y = y
        self.abs_x = x + (0-background.x)
        self.abs_y = y + (0-background.y)
        self.rotation = rotation
        self.pen = pygame.transform.rotate(self.pen, -90 * self.rotation)
        self.animalStart = (x+20, y+20)
        
    
    def draw(self, window, background: bg.Background, windowSize, x=None, y=None, rotation=None, bypass=False):
        # Animal size of 1 is 52x150
        # For size of i, image size is (52*i)+(20*(i-1))x150
            # doubles size and adds the 20 pixels in between
        if GCF.onScreen((self.x, self.y), (self.width,self.height), windowSize) or bypass:
            # either all three or none should be None
            if(x is None or y is None or rotation is None):
                absCoords = (self.abs_x, self.abs_y)
                coords = GCF.absToRelCoords(absCoords, background, windowSize)
                self.x = coords[0]
                self.y = coords[1]
                
                # figure out start pos from rotation. Always top left corner of unrotated pen
                if self.rotation % 4 == 0:
                    self.animalStart = (self.x+20, self.y+20)
                elif self.rotation % 4 == 1:
                    self.animalStart = (self.x+self.height-20-150, self.y+20)
                elif self.rotation % 4 == 2:
                    self.animalStart = (self.x+self.width-20, self.y+self.height-20)
                elif self.rotation % 4 == 3:
                    self.animalStart = (self.x+20, self.y+self.width-20)
                    
                rotation = self.rotation
                window.blit(self.pen, coords)
            else:
                coords = [x, y]
                pen = pygame.transform.rotate(self.penUnRot, rotation * -90)
                
                # figure out start pos from rotation. Always top left corner of unrotated pen
                if rotation % 4 == 0:
                    self.animalStart = (x+20, y+20)
                elif rotation % 4 == 1:
                    self.animalStart = (x+self.height-20-150, y+20)
                elif rotation % 4 == 2:
                    self.animalStart = (x+self.width-20, y+self.height-20)
                elif rotation % 4 == 3:
                    self.animalStart = (x+20, y+self.width-20)
                    
                window.blit(pen, coords)
                
            if self.spaceFilled == 0:
                return
            j = 0
            for i in range(len(self.animals)):
                if self.animals[i].species != "Null_Animal":
                    self.animals[i].draw(window, self.animalStart, j, rotation)
                    j += self.animals[i].size
        else:
            self.updateRelCoords(background, windowSize)
        
        
    def updateRelCoords(self, background: bg.Background, windowSize):
        absCoords = (self.abs_x, self.abs_y)
        coords = GCF.absToRelCoords(absCoords, background, windowSize)
        self.x = coords[0]
        self.y = coords[1]
    
    def newDay(self):
        for i in range(len(self.animals)):
            if self.animals[i].name != "Null_Animal":
                self.animals[i].advanceDay()
    
    def addAnimal(self, anmlType, name):
        anml = DF.getAnimal(anmlType, name)
        print(anml.species)
        if self.spaceFilled + anml.size > self.capacity:
            return
        if name in self.names:
            return
        self.names.add(name)
        self.animals.append(anml)
        self.spaceFilled += anml.size
        
    def milk(self, invnt: Inventory):
        for i in self.animals:
            if i.produced[i.dataIndex].name == "Null_Item":
                continue
            if i.timeLastItem < i.productionTime:
                continue
            i.timeLastItem = 0
            invnt.addToInvnt(i.produced[i.dataIndex])
            
    def butcher(self, animal, invnt: Inventory, shop=False):
        for i in range(len(self.animals)):
            if self.animals[i].name == animal.name:
                self.animals.pop(i)
                self.names.remove(animal.name)
                break
        if shop:
            invnt.gold += animal.sellCost[animal.dataIndex]
        elif animal.onDeath[animal.dataIndex].name != "Null_Item":
            invnt.addToInvnt(animal.onDeath[animal.dataIndex])
        return
            
    def checkColl(self, newX, newY, direction):
        # needs to take in abs coords
        if self.rotation % 4 == 0 or self.rotation % 4 == 2:
            if direction == 'X' or direction == 'x':
                if newX == self.abs_x or newX == self.abs_x + self.width:
                    for y in newY:
                        if y >= self.abs_y and y <= self.abs_y + self.height:
                            return True
            else:
                if newY == self.abs_y or newY == self.abs_y + self.height:
                    for x in newX:
                        if x >= self.abs_x and x <= self.abs_x + self.width:
                            return True
        else:
            # checks if pen is rotated, if so swap width and height
            if direction == 'X' or direction == 'x':
                if newX == self.abs_x or newX == self.abs_x + self.height:
                    for y in newY:
                        if y >= self.abs_y and y <= self.abs_y + self.width:
                            return True
            else:
                if newY == self.abs_y or newY == self.abs_y + self.width:
                    for x in newX:
                        if x >= self.abs_x and x <= self.abs_x + self.height:
                            return True
        return False
                
