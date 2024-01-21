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
last_mouse = 0
count = 0
player = GC.Player(0,0,80,80)
bg = BGM.Background("Test", 0, 0)
plots = []
pens = []
shop = SC.Inventory()
shop.addToInvnt(DF.getItem("Turnip_Seed", 50))
shop.addToInvnt(DF.getItem("Carrot_Seed", 50))
invt = SC.Inventory(50)
invnt_open = False
coll = C.Collision()
check = False
pygame.mouse.set_visible(False)
invntindex = 0
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
            plt = SC.Plot()
            plt.build(100, 100, bg, (WIDTH,HEIGHT), WIN)
            plots.append(plt)
        
        
    if keys[pygame.K_a]:
        if count - last_pressP >= 10:
            last_pressP = count
            pen = SC.Pen()
            pen.build(100, 100, bg, (WIDTH,HEIGHT), WIN)
            pens.append(pen)
    
    if keys[pygame.K_w]:
        pens[len(pens)-1].addAnimal("Lesser_Wyrm", str(count))
    
    if keys[pygame.K_c]:
        pens[len(pens)-1].addAnimal("Cow", str(count))

    if keys[pygame.K_p]:
        check = True
        if count - last_pressP >= 10:
             last_pressP = count
             interactive_plot = []
             interactive_plot = [player.checkTouching(coll, plots)]
             if isinstance(interactive_plot[0], SC.Plot):
                InvntF.inventoryPlant(invt, player.checkTouching(coll, plots), invntindex, WIN, (WIDTH,HEIGHT))
                
    if keys[pygame.K_h]:
        interactive_plt = [player.checkTouching(coll, plots)]
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
            pygame.mouse.set_visible(invnt_open)
            pygame.mouse.set_pos((100,100))
            invntindex = 0
    if keys[pygame.K_g]:
         if count - last_pressG >= 10:
             last_pressG = count
             for plt in plots:
                 for crp in plt.crops:
                    if crp.name != "Null_Crop":
                        crp.advanceDay()
    if keys[pygame.K_b]:
        InvntF.transferInventory("Turnip_Seed", 5, shop, invt, shop=True)
        InvntF.transferInventory("Carrot_Seed", 5, shop, invt, shop=True)
    if keys[pygame.K_l]:
         InvntF.transferInventory("Turnip", 1, invt, shop, shop=True)
         InvntF.transferInventory("Carrot", 1, invt, shop, shop=True)
         
    
        
        
    if not invnt_open:
        player.controlPlayer((WIDTH, HEIGHT), keys, bg, coll, plots)
        WIN.fill((0,0,0))
        bg.draw(WIN)
        for i in plots:
            i.draw(WIN, bg, (WIDTH,HEIGHT))
        for i in pens:
            i.draw(WIN, bg, (WIDTH,HEIGHT))
            
        player.draw(WIN)
        InvntF.displayInventory(WIN, invt)
        coll.drawObstacles(bg, WIN, (WIDTH,HEIGHT), player)
        #if len(pens) > 0:
        #    if len(pens[0].animals) > 0:
        #        WIN.blit(pens[0].animals[0].animal, (100,100))
    else:
        if pygame.mouse.get_pressed()[0]:
            if count - last_mouse >= 10:
                last_mouse = count
                coords = pygame.mouse.get_pos()
                InvntF.getItemClick(invt, coords, invntindex) 
        if keys[pygame.K_DOWN]:
            invntindex += 1
        if keys[pygame.K_UP]:
            invntindex -= 1
        if invntindex > 20:
            invntindex = 20
        elif invntindex < 0:
            invntindex = 0
        InvntF.displayInventory(WIN, invt, invntindex, open=True, player=player)
    pygame.display.update()

         
         


