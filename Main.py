import pygame

import GraphicsClasses as GC
import GraphicsClassFunctions as GCF
import BackgroundMap as BGM
import StructureClasses as SC
import DataFunctions as DF
import InventoryShopFunctions as InvntF
import Collisions as C


WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Window")
clock = pygame.time.Clock()

run = True
last_pressG = 0
last_pressP = 0
last_pressD = 0
count = 0
player = GC.Player(0,0,80,80)
bg = BGM.Background("Test", 0, 0)
plots = []
shop = SC.Inventory()
shop.addToInvnt(DF.getItem("Turnip_Seed", 50))
invt = SC.Inventory(50)
invnt_open = False
coll = C.Collision()
check = False
while run:
    clock.tick(20)
    count += 1
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    keys = pygame.key.get_pressed()

    if keys[pygame.K_s]:
        if count - last_pressP >= 10:
            last_pressP = count
            coll.obsList = [None] * 10
            coll.tempCollPlacements = set([(100,100), (200,200), (300,300), (400,400), (500,500), (600,600), (700,700), (800,800), (900,900), (1000,1000), (200, 100), (300,100), (500,600), (100,400), (200, 600)])
            coll.tempCollPositions  = set()
            coll.generate()
            #plt = GC.Plot(100,100,bg,(WIDTH,HEIGHT))
            #plt = SC.Plot()
            #plt.build(100, 100, bg, (WIDTH,HEIGHT), WIN)
            #plots.append(plt)
        
        
    if keys[pygame.K_p]:         #TODO fix references
        check = True
        if count - last_pressP >= 10:
             last_pressP = count
             #invt.plant(player.checkTouching(coll, plots), WIN)
             interactive_plot = []
             interactive_plot = [player.checkTouching(coll, plots)]
             if isinstance(interactive_plot[0], SC.Plot):
             #for i in plots:
              #   if i.plot.abs_x == interactive_plot[0].plot.abs_x and i.plot.abs_y == interactive_plot[0].plot.abs_y:
               #      i.plant("Turnip", 1, invt, WIN)
                interactive_plot[0].plant("Turnip", 1, invt, WIN)
                #print(plots[0].plot.crops[0].name)
            
    if keys[pygame.K_h]:
        interactive_plt = [player.checkTouching(coll, plots)]
        print(str(type(interactive_plt[0])))
        if isinstance(interactive_plt[0], SC.Plot):
            interactive_plt[0].harvest(invt)
    if keys[pygame.K_x]:
        interactive = [player.checkTouching(coll, plots)]
        if isinstance(interactive[0], C.Obstacle):
            interactive[0].health -= 10
            if interactive[0].health <= 0:
                coll.removeFromCollision(interactive[0], invt)
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
             for plt in plots:
                 for crp in plt.crops:
                    if crp.name != "Null_Crop":
                        crp.advanceDay()
    if keys[pygame.K_b]:
        InvntF.transferInventory("Turnip_Seed", 5, shop, invt, shop=True)
    if keys[pygame.K_l]:
         InvntF.transferInventory("Turnip", 1, invt, shop, shop=True)
        
    if not invnt_open:
        player.controlPlayer((WIDTH, HEIGHT), keys, bg, coll, plots)
        WIN.fill((0,0,0))
        bg.draw(WIN)
        for i in plots:
            i.draw(WIN, bg, (WIDTH,HEIGHT))
        #if check:
        #    for i in plots:
        #        print(i.plot.cropNum)
        #    check = False
            
        player.draw(WIN)
        InvntF.displayInventory(WIN, invt)
        coll.drawObstacles(bg, WIN, (WIDTH,HEIGHT), player)
    else:
        InvntF.displayInventory(WIN, invt, open=True, player=player)
    pygame.display.update()

         
         


