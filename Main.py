import pygame

import GraphicsClasses as GC
import GraphicsClassFunctions as GCF
import BackgroundMap as BGM
import StructureClasses as SC
import DataFunctions as DF


WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Window")
clock = pygame.time.Clock()

run = True
last_pressG = 0
last_pressP = 0
count = 0
player = GC.Player(200,200,75,75,animated=True)
bg = BGM.Background("Test", 0, 0)
plots = []
while run:
    clock.tick(20)
    count += 1
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    keys = pygame.key.get_pressed()

    if keys[pygame.K_s]:
        #plt = GC.Plot(100,100,bg,(WIDTH,HEIGHT))
        plt = SC.Plot(WIN)
        plots.append(plt)
        plt.build(100, 100, bg, (WIDTH,HEIGHT), WIN) 
        invt = SC.Inventory()
        invt.addToInvnt(DF.getItem("Turnip_Seed", 26))
    if keys[pygame.K_p]:
       if count - last_pressP >= 10:
             last_pressP = count
             #plt.crops.append(GC.Crop("Turnip"))
             #plt.crops[plt.cropNum].plant(WIN, plt)
             plt.plant("Turnip", 1, invt, WIN)
    if keys[pygame.K_h]:
        plt.harvest(invt)
    if keys[pygame.K_d]:
        for i in invt.inventory:
            if i.name != "Null_Item":
                print(i.name + ", " + str(i.count) + '\n')
        for i in plt.emptySpots:
            print(i)
        print('\n' + str(len(plt.emptySpots)))
    if keys[pygame.K_g]:
         if count - last_pressG >= 10:
             last_pressG = count
             for crp in plt.crops:
                if crp.name != "Null_Crop":
                    crp.advanceDay()
    
    player.controlPlayer((WIDTH, HEIGHT), keys, bg)
    WIN.fill((0,0,0))
    bg.draw(WIN)
    for i in plots:
        i.draw(WIN, bg, (WIDTH,HEIGHT))
    player.draw(WIN)
    pygame.display.update()

         
         


