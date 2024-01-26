import pygame
import StructureClasses as SC
import ObjectClasses as OC
import DataFunctions as DF

NUMBERS = {
    '0': pygame.image.load("Art\Zero.png"),
    '1': pygame.image.load("Art\One.png"),
    '2': pygame.image.load("Art\Two.png"),
    '3': pygame.image.load("Art\Three.png"),
    '4': pygame.image.load("Art\Four.png"),
    '5': pygame.image.load("Art\Five.png"),
    '6': pygame.image.load("Art\Six.png"),
    '7': pygame.image.load("Art\Seven.png"),
    '8': pygame.image.load("Art\Eight.png"),
    '9': pygame.image.load("Art\\Nine.png"),}

NUM_WIDTH = 32
NUM_HEIGHT = 32

def numToDisplay(num, pos, WIN):
    # print numbers at given spot
    # pos parameter is upper right corner of number for alignment
    x = pos[0]
    if num < 0:
        num = 0
    num = str(num)
    for i in range(len(num) - 1, -1, -1):
        WIN.blit(NUMBERS[num[i]], (x, pos[1]))
        x -= NUM_WIDTH


def transferInventory(item: str, count, i1: SC.Inventory, i2: SC.Inventory, shop=False):
    # transfer from i1 to i2
    # if shop, also change gold
    # buying/selling will have shop True, chests will be False
    # both shops and chests will have gold = None
    valid_move = False
    for i in range(len(i1.inventory)):
        if i1.inventory[i].name == item and i1.inventory[i].count >= count:
            itmIndex = i
            if shop:
                if i2.gold is not None and i2.gold > int(i1.inventory[i].buyCost):          #TODO can buy to negative amounts
                    valid_move = True
                else:
                    valid_move = True
            else:
                valid_move = True
            continue
    if len(i2.emptySpots) == 0:
        valid_move = False
    if not valid_move:
        return
    
    itm = DF.getItem(item, count)
    i1.inventory[itmIndex].count -= count
    i1.clearEmpty()
    i2.addToInvnt(itm)
    if shop:
        # TODO if case where transfering from two inventories with gold, this creates money
        # low priority, there isn't yet a case where this would come up
        if i1.gold is not None:
            i1.gold += int(itm.sellCost) * count
        if i2.gold is not None:
            i2.gold -= int(itm.buyCost) * count
    

def displayInventory(WIN, invnt, startindex=0, player=None, open=False, invnt2=None, shop=False):
    if not open:
        numToDisplay(invnt.gold, (960, 15), WIN)
        return
    WIN.fill((0,0,0))
    inventory = pygame.image.load("Art\InventoryTest.png")
    WIN.blit(inventory, (100,100))
    numToDisplay(invnt.gold, (860, 115), WIN)
    y = 120
    for i in range(startindex, startindex + 10):
        if invnt.inventory[i].name != "Null_Item":
            try:                        # TODO fix when adding item icons
                item = pygame.image.load("Art\\" + invnt.inventory[i].name + ".png")
            except:
                item = pygame.image.load("Art\\" + invnt.inventory[i].name + "_Grown.png")
            WIN.blit(item, (110, y))
            numToDisplay(invnt.inventory[i].count, (300, y), WIN)
            y += 50
        else:
            numToDisplay(i, (150, y), WIN)
            y += 50
    if not shop and player is not None:
        plyr = pygame.image.load(player.images[0])
        plyr = pygame.transform.scale(plyr, (250,250))
        WIN.blit(plyr, (600,350))
        
def getItemClick(invnt: SC.Inventory, mousePos, startindex, invnt2: SC.Inventory =None, shop=False):
    # Todo work with when 2 inventories
    if mousePos[0] < 110 or mousePos[0] > 400:
        return
    elif mousePos[1] < 120 or mousePos[1] > 610:
        return
    item = (mousePos[1] - 115) // 50
    return startindex + item
        
def inventoryPlant(invnt: SC.Inventory, plot, invntindex, WIN, windowSize):
    if not isinstance(plot, SC.Plot):
        return
    pygame.mouse.set_visible(True)
    count = 0
    last_mouse = 10
    keys = pygame.key.get_pressed()
    clock = pygame.time.Clock()
    while True:
        clock.tick(20)
        count += 1
        pygame.event.get()
        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        break
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and count > 10:
            break
        if pygame.mouse.get_pressed()[0]:
            if count - last_mouse >= 10:
                last_mouse = count
                coords = pygame.mouse.get_pos()
                item = getItemClick(invnt, coords, invntindex)
                if invnt.inventory[item].type == "Seed":
                    plot.plant(invnt.inventory[item].name, item, invnt, WIN)
        if keys[pygame.K_DOWN]:
            invntindex += 1
        if keys[pygame.K_UP]:
            invntindex -= 1
        if invntindex > 20:
            invntindex = 20
        elif invntindex < 0:
            invntindex = 0
        WIN.fill((0,0,0)) 
        displayInventory(WIN, invnt, invntindex, open=True)
        plot.draw(WIN, None, windowSize, 600, 350)
        pygame.display.update()
    pygame.mouse.set_visible(False)
    
def inventoryAnimal(invnt: SC.Inventory, pen, invntindex, WIN, windowSize):
    if not isinstance(pen, SC.Pen):
        return
    pygame.mouse.set_visible(True)
    count = 0
    last_mouse = 10
    keys = pygame.key.get_pressed()
    clock = pygame.time.Clock()
    
    # deal with rotation for drawing pen
    while True:
        clock.tick(20)
        count += 1
        pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and count > 10:
            break
        # select animal
        # butcher animal
        # feed animal
        if pygame.mouse.get_pressed()[0]:
            if count - last_mouse >= 10:
                last_mouse = count
                coords = pygame.mouse.get_pos()
                item = getPenAnimal(invnt, coords)
        displayInventory(WIN, invnt, invntindex, open=True)
        pen.draw(WIN, None, windowSize, 600, 200, rotation=1)
        #pen = pygame.image.load(self.image)
        #pen = pygame.transform.scale(pen, (self.width,self.height))
        #pen = pygame.transform.rotate(pen, -90 * self.rotated)
        pygame.display.update()
    
def getPenAnimal(pen, mousePos):
    pass

