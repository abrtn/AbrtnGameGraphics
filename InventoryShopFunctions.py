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
    

def displayInventory(WIN, invnt, player=None, open=False, invnt2=None, shop=False):
    if not open:
        numToDisplay(invnt.gold, (960, 15), WIN)
        return
    WIN.fill((0,0,0))
    inventory = pygame.image.load("Art\InventoryTest.png")
    WIN.blit(inventory, (100,100))
    numToDisplay(invnt.gold, (860, 115), WIN)
    y = 120
    for i in invnt.inventory:
        if i.name != "Null_Item":
            try:                        # TODO fix when adding item icons
                item = pygame.image.load("Art\\" + i.name + ".png")
            except:
                item = pygame.image.load("Art\\" + i.name + "_Grown.png")
            WIN.blit(item, (110, y))
            numToDisplay(i.count, (300, y), WIN)
            y += 40
    if not shop:
        plyr = pygame.image.load(player.images[0])
        plyr = pygame.transform.scale(plyr, (250,250))
        WIN.blit(plyr, (600,350))
        