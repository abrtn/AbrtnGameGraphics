import pygame
import ObjectClasses as OC

CROP_INDEX = {}
ITEM_INDEX = {}
ANIMAL_INDEX = {}


def getCrop(name, num=1):
    #if name in CROP_INDEX:
    #    newCrop = CROP_INDEX[name]         TODO
    #    return newCrop
    f = open("RefData\Crops.txt", 'r')
    cropData = ["Null_Crop", 0, "Null"]
    for line in f:
        if line[0] == '_':
            continue
        lineList = line.split()
        if lineList[0] == name:
            cropData = lineList
            break
    newCrop = OC.Crop(cropData[0])
    newCrop.growTime = int(cropData[1])
    CROP_INDEX[name] = newCrop
    return newCrop
        

def getItem(name, num):
    #if name in ITEM_INDEX:
    #    newItem = ITEM_INDEX[name]
    #    return newItem
    f = open("RefData\Items.txt", 'r')
    itemData = ["Null_Item", 0, 0, '-', '-']
    for line in f:
        if line[0] == '_':
            continue
        lineList = line.split()
        if lineList[0] == name:
            itemData = lineList
            break
    newItem = OC.Item(itemData[0], num)
    newItem.buyCost = int(itemData[1])
    newItem.sellCost = int(itemData[2])
    newItem.type = itemData[3]
    newItem.alignment = itemData[4]
    ITEM_INDEX[name] = newItem
    return newItem


def getAnimal(species, name):
    #if species in ANIMAL_INDEX:
    #    newAnml = ANIMAL_INDEX[species]
    #    newAnml.name = name
    #    return newAnml
    f = open("RefData\Animals.txt", 'r')
    anmlData = ["Null_Animal", 0, 0, '-', 0, '-', 0, 0, 0]
    for line in f:
        if line[0] == '_':
            continue
        lineList = line.split()
        if lineList[0] == species:
            anmlData = lineList
            break
    newAnml = OC.Animal(anmlData[0], name)
    newAnml.buyCost = list(map(int, anmlData[1].split('_')))
    newAnml.sellCost = list(map(int, anmlData[2].split('_')))
    produced = anmlData[3].split('_')
    newAnml.produced = [getItem(itm, 1) for itm in produced]
    newAnml.productionTime = int(anmlData[4])
    produced = anmlData[5].split('_')
    newAnml.onDeath = [getItem(itm, 1) for itm in produced]
    newAnml.growTime = int(anmlData[6])
    newAnml.predatorRating = int(anmlData[7])
    newAnml.size = int(anmlData[8])
    ANIMAL_INDEX[species] = newAnml
    if newAnml.predatorRating == 0 or newAnml.predatorRating == 1:
        newAnml.eats = "Crop"
    elif newAnml.predatorRating == 2:
        newAnml.eats = "Meat"
    return newAnml

