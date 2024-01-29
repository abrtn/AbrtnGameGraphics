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


def transferInventory(itmIndex: str, count, i1: SC.Inventory, i2: SC.Inventory, shop=False):
    # transfer from i1 to i2
    # if shop, also change gold
    # buying/selling will have shop True, chests will be False
    # both shops and chests will have gold = None
    if count > i1.inventory[itmIndex].count:
        return    
            
    if shop:
        if i2.gold is not None and i2.gold > int(i1.inventory[itmIndex].buyCost):          #TODO can buy to negative amounts
            valid_move = True
        else:
            valid_move = True
    else:
        valid_move = True
    if len(i2.emptySpots) == 0:
        valid_move = False
    if not valid_move:
        return
    
    itm = DF.getItem(i1.inventory[itmIndex].name, count)
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
           
    y = 120
    if invnt2 is not None:
        for i in range(len(invnt2.inventory)):
            if invnt2.inventory[i].name != "Null_Item":
                try:                        # TODO fix when adding item icons
                    item = pygame.image.load("Art\\" + invnt2.inventory[i].name + ".png")
                except:
                    item = pygame.image.load("Art\\" + invnt2.inventory[i].name + "_Grown.png")
                WIN.blit(item, (520, y))
                if shop:
                    numToDisplay(invnt2.inventory[i].sellCost, (710, y), WIN)
                else:
                    numToDisplay(invnt2.inventory[i].count, (710, y), WIN)
                y += 50
                
    if player is not None:
        plyr = pygame.image.load(player.images[0])
        plyr = pygame.transform.scale(plyr, (250,250))
        WIN.blit(plyr, (600,350))
        
def getItemClick(invnt: SC.Inventory, mousePos, startindex, invnt2: SC.Inventory =None, start2=None):
    # both or neither invnt2 and start2 must be None
    if invnt2 is not None:
        if mousePos[0] >= 520 and mousePos[0] <= 710:
            if mousePos[1] >= 120 and mousePos[1] <= 610:
                item = (mousePos[1] - 115) // 50
                return start2 + item, 2

    if mousePos[0] < 110 or mousePos[0] > 400:
        return
    elif mousePos[1] < 120 or mousePos[1] > 610:
        return
    item = (mousePos[1] - 115) // 50
    return startindex + item, 1
        
def inventoryPlant(invnt: SC.Inventory, plot, invntindex, WIN, windowSize):
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
                print(coords)
                item = getItemClick(invnt, coords, invntindex)
                if item is not None and invnt.inventory[item[0]].type == "Seed":
                    plot.plant(invnt.inventory[item[0]].name, item[0], invnt, WIN)
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
    pygame.mouse.set_visible(True)
    count = 0
    last_mouse = 10
    keys = pygame.key.get_pressed()
    clock = pygame.time.Clock()
    animal = None
    print(len(pen.animals))
    # deal with rotation for drawing pen
    while True:
        clock.tick(20)
        count += 1
        pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and count > 10:
            break
        # butcher animal
        # feed animal
        if pygame.mouse.get_pressed()[0]:
            if count - last_mouse >= 10:
                last_mouse = count
                coords = pygame.mouse.get_pos()
                print(coords)
                animal = getPenAnimal(pen, coords)
                if animal is not None:
                    print(animal.species)
        if keys[pygame.K_b]:
            if animal is None:
                continue
            pen.butcher(animal, invnt)
            animal = None
        if keys[pygame.K_DOWN]:
            invntindex += 1
        if keys[pygame.K_UP]:
            invntindex -= 1
        if invntindex > 20:
            invntindex = 20
        elif invntindex < 0:
            invntindex = 0
        displayInventory(WIN, invnt, invntindex, open=True)
        pen.draw(WIN, None, windowSize, 600, 200, rotation=1)
        pygame.display.update()
    
def getPenAnimal(pen, mousePos):
    if mousePos[0] > 840 or mousePos[0] < 690:
        return None
    elif mousePos[1] > 580 or mousePos[1] < 220:
        return None
    space = (mousePos[1] - 210) // 72 + 1
    size = 0
    for i in pen.animals:
        size += i.size
        if size >= space:
            if i.name != "Null_Animal":
                return i
            return None
    return None

def inventoryShop(invnt: SC.Inventory, invnt2: SC.Inventory, invntindex, WIN, windowsize, shop=False):
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
        if keys[pygame.K_b] and count > 10:
            break
        
        if pygame.mouse.get_pressed()[0]:
            if count - last_mouse >= 10:
                last_mouse = count
                coords = pygame.mouse.get_pos()
                item = getItemClick(invnt, coords, invntindex, invnt2=invnt2, start2=0)
                print(item)
                if item is not None:
                    if item[1] == 1:
                        transferInventory(item[0], 1, invnt, invnt2, shop=shop)
                    elif item[1] == 2:
                        transferInventory(item[0], 1, invnt2, invnt, shop=shop)
        
        if keys[pygame.K_DOWN]:
            invntindex += 1
        if keys[pygame.K_UP]:
            invntindex -= 1
        if invntindex > 20:
            invntindex = 20
        elif invntindex < 0:
            invntindex = 0
            
        WIN.fill((0,0,0)) 
        displayInventory(WIN, invnt, invntindex, invnt2=invnt2, shop=shop, open=True)
        pygame.display.update()

