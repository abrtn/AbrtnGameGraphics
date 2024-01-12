import pygame
import GraphicsClasses as GC
import BackgroundMap as bg

def getImage(name: str):
    f = open("refArt.txt", 'r')
    artList = []
    next(f)
    for line in f:
        if(line[0] == '_'):
            continue
        artList = line.split()
        if(artList[0] == name):
            f.close()
            return artList
    return [name, "Art\Turnip_Grown.png", "Art\Turnip_Grown.png"]


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
    if coords2[0] > coords1[0] and coords2[0] < coords1[0] + width1:
        if coords2[1] > coords1[1] and coords2[1] < coords1[1] + height1:
            return True
    # check upper right corner
    if coords2[0] + width2 > coords1[0] and coords2[0] + width2 < coords1[0] + width1:
        if coords2[1] > coords1[1] and coords2[1] < coords1[1] + height1:
            return True
    # check lower left corner
    if coords2[0] > coords1[0] and coords2[0] < coords1[0] + width1:
        if coords2[1] + height2 > coords1[1] and coords2[1] + height2 < coords1[1] + height1:
            return True
    # check lower right corner
    if coords2[0] + width2 > coords1[0] and coords2[0] + width2 < coords1[0] + width1:
        if coords2[1] + height2 > coords1[1] and coords2[1] + height2 < coords1[1] + height1:
            return True
    return False