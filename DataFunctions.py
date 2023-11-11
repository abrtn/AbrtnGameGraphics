import pygame
import ObjectClasses as OC

CROP_INDEX = {}
ITEM_INDEX = {}
ANIMAL_INDEX = {}


def getCrop(name, num):
    if name in CROP_INDEX:
        newCrop = CROP_INDEX[name]
        return newCrop
    f = open("RefData\Crops.txt", 'r')
    cropData = ["NullCrop", 0]
    for line in f:
        if line[0] == '_':
            continue
        lineList = line.split()
        if lineList[0] == name:
            cropData = lineList
            break
    newCrop = OC.Crop(cropData[0], num)
    newCrop.growTime = cropData[1]
    CROP_INDEX[name] = newCrop
    return newCrop
        

def getItem(name, num):
    if name in ITEM_INDEX:
        newItem = ITEM_INDEX[name]
        return newItem
    f = open("RefData\Items.txt", 'r')
    itemData = ["NullItem", 0, 0, '-']
    for line in f:
        if line[0] == '_':
            continue
        lineList = line.split()
        if lineList[0] == name:
            itemData = lineList
            break
    newItem = OC.Item(itemData[0], num)
    newItem.buyCost = itemData[1]
    newItem.sellCost = itemData[2]
    newItem.type = itemData[3]
    ITEM_INDEX[name] = newItem
    return newItem

def getAnimal(species, name):
    if species in ANIMAL_INDEX:
        newAnml = ANIMAL_INDEX[species]
        newAnml.name = name
        return newAnml
    f = open("RefData\Animals.txt", 'r')
    anmlData = ["NullAnimal", 0, 0, '-', 0, '-', 0, 0]
    for line in f:
        if line[0] == '_':
            continue
        lineList = line.split()
        if lineList[0] == species:
            anmlData = lineList
            break
    newAnml = OC.Animal(anmlData[0], name)
    newAnml.buyCost = anmlData[1]
    newAnml.sellCost = anmlData[2]
    newAnml.produced = anmlData[3]
    newAnml.productionTime = anmlData[4]
    newAnml.onDeath = anmlData[5]
    newAnml.growTime = anmlData[6]
    newAnml.predatorRating = anmlData[7]
    ANIMAL_INDEX[species] = newAnml
    return newAnml

