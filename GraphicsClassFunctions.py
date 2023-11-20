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
