import pygame
import GraphicsClasses as GC
import BackgroundMap as bg

def getImage(name: str, bypassTo=None):
    f = open("refArt.txt", 'r')
    artList = []
    next(f)
    bypassMet = True
    if bypassTo is not None:
        bypassMet = False
    for line in f:
        if bypassMet == False:
            if line[2:len(bypassTo) + 2] == bypassTo:
                bypassMet = True
            continue
        if(line[0] == '_'):
            continue
        artList = line.split()
        if(artList[0] == name):
            print(artList)
            f.close()
            return artList
    return ["NULL", "Art\Turnip_Grown.png", "Art\Turnip_Grown.png"]


def absToRelCoords(absCoords, background: bg.Background, windowSize=()):
    #background coords will always be <= 0
    windowCoords = (0 - background.x, 0 - background.y)
    relCoords = (absCoords[0] - windowCoords[0], absCoords[1] - windowCoords[1])
    return relCoords

def onScreen(relCoords, size, windowSize):
    if(relCoords[0] < windowSize[0] and relCoords[0] + size[0] > 0):
        return True
    if(relCoords[1] < windowSize[1] and relCoords[1] + size[1] > 0):
        return True
    return False

def checkInside(coords1, width1, height1, coords2, width2, height2):
    # check if object 2 is inside boundary of object 1
    # check upper left corner
    if coords2[0] >= coords1[0] and coords2[0] <= coords1[0] + width1:
        if coords2[1] > coords1[1] and coords2[1] < coords1[1] + height1:
            return True
    # check upper right corner
    if coords2[0] + width2 >= coords1[0] and coords2[0] + width2 <= coords1[0] + width1:
        if coords2[1] > coords1[1] and coords2[1] < coords1[1] + height1:
            return True
    # check lower left corner
    if coords2[0] >= coords1[0] and coords2[0] <= coords1[0] + width1:
        if coords2[1] + height2 > coords1[1] and coords2[1] + height2 < coords1[1] + height1:
            return True
    # check lower right corner
    if coords2[0] + width2 >= coords1[0] and coords2[0] + width2 <= coords1[0] + width1:
        if coords2[1] + height2 > coords1[1] and coords2[1] + height2 < coords1[1] + height1:
            return True
    return False

def placePenPlot(item, size, WIN, winSize, loc):
    # Returns if operation was successful, if so need to subtract item/gold from inventory
    pygame.mouse.set_visible(True)
    count = 0
    last_mouse = 10
    keys = pygame.key.get_pressed()
    clock = pygame.time.Clock()
    last_press = 10
    rotation = 0
    coords = [0,0]
    width = item.width
    height = item.height
    while True:
        clock.tick(20)
        count += 1
        pygame.event.get()
        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        break
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return False
        if keys[pygame.K_RIGHT]:
            if count - last_press >= 10:
                last_press = count
                rotation = (rotation + 1)%4
                width, height = height, width
        if keys[pygame.K_LEFT]:
            if count - last_press >= 10:
                last_press = count
                rotation = (rotation +3)%4
                width, height = height, width
        coords = pygame.mouse.get_pos()
        absCoords = (coords[0] + loc.background.x - 100, coords[1] + loc.background.y - 100)
        if pygame.mouse.get_pressed()[0]:
            if count - last_mouse >= 10:
                last_mouse = count
                
                validMove = True
                for i in loc.collisions.obsList:
                    if i is not None and i.name is not None:
                        if checkInside(absCoords, width, height, (i.absx, i.absy), i.width, i.height):
                            validMove = False
                for i in loc.plots:
                    if checkInside(absCoords, width, height, (i.plot.abs_x, i.plot.abs_y), 260, 260):
                        validMove = False
                for i in loc.buildings:
                    if checkInside(absCoords, width, height, (i.absx, i.absy), i.width, i.height):
                        validMove = False
                print(len(loc.pens))
                for i in loc.pens:
                    iwidth = i.width
                    iheight = i.height
                    if i.rotation %2 != 0:
                        iwidth, iheight = iheight, iwidth
                    if checkInside(absCoords, width, height, (i.abs_x, i.abs_y), iwidth, iheight):
                        validMove = False
                
                if validMove:
                    x = (coords[0]//20)*20 - 100
                    y = (coords[1]//20)*20 - 100
                    if coords[0] % 20 > 10:
                        x += 20
                    if coords[1] % 20 > 10:
                        y += 20
                    item.build(x, y, loc.background, winSize, WIN, rotation)                     #x, y, background, size, window, rotation
                    return True
        WIN.fill((0,0,0))
        loc.drawBeforePlayer(WIN, winSize)
        loc.drawAfterPlayer(WIN, winSize, None)
        item.draw(WIN, loc.background, winSize, x=coords[0] - 100, y=coords[1] - 100, rotation=rotation, bypass=True)         #window, background, size, x, y, rotation
        pygame.display.update()
    return False
        
        