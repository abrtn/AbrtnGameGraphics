import pygame

import GraphicsClasses as GC
import GraphicsClassFunctions as GCF
import BackgroundMap as BGM
import StructureClasses as SC
import DataFunctions as DF
import InventoryShopFunctions as InvntF


WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Window")
clock = pygame.time.Clock()

run = True
last_pressG = 0
last_pressP = 0
last_pressD = 0
count = 0
player = GC.Player(200,200,75,75,animated=True)
bg = BGM.Background("Test", 0, 0)
plots = []
shop = SC.Inventory()
shop.addToInvnt(DF.getItem("Turnip_Seed", 50))
invt = SC.Inventory(50)
invnt_open = False
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
        
        #invt.addToInvnt(DF.getItem("Turnip_Seed", 26))
    if keys[pygame.K_p]:
       if count - last_pressP >= 10:
             last_pressP = count
             #plt.crops.append(GC.Crop("Turnip"))
             #plt.crops[plt.cropNum].plant(WIN, plt)
             plt.plant("Turnip", 1, invt, WIN)
    if keys[pygame.K_h]:
        plt.harvest(invt)
    if keys[pygame.K_d]:
        if count - last_pressD >= 10:
            last_pressD = count
            print(invt.gold)
            for i in invt.inventory:
                if i.name != "Null_Item":
                    print(i.name + ", " + str(i.count) + '\n')
            invnt_open = not invnt_open
    if keys[pygame.K_g]:
         if count - last_pressG >= 10:
             last_pressG = count
             for crp in plt.crops:
                if crp.name != "Null_Crop":
                    crp.advanceDay()
    if keys[pygame.K_b]:
        InvntF.transferInventory("Turnip_Seed", 5, shop, invt, shop=True)
    if keys[pygame.K_l]:
         InvntF.transferInventory("Turnip", 1, invt, shop, shop=True)
        
    if not invnt_open:
        player.controlPlayer((WIDTH, HEIGHT), keys, bg)
        WIN.fill((0,0,0))
        bg.draw(WIN)
        for i in plots:
            i.draw(WIN, bg, (WIDTH,HEIGHT))
        player.draw(WIN)
        InvntF.displayInventory(WIN, invt)
    else:
        InvntF.displayInventory(WIN, invt, open=True, player=player)
    pygame.display.update()

         
         


