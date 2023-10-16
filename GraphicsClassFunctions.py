import pygame

def getImage(name: str):
    f = open("refArt.txt", 'r')
    artList = []
    next(f)
    for line in f.readline():
        if(line[0] == '_'):
            continue
        artList = line.split()
        if(artList[0] == name):
            f.close()
            return artList
    return [name, "nullImg1", "nullImg2"]
