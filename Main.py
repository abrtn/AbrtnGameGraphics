from re import A
import pygame

import GraphicsClasses as GC
import GraphicsClassFunctions as GCF
import BackgroundMap as BGM
import StructureClasses as SC
import DataFunctions as DF
import InventoryShopFunctions as InvntF
import Collisions as C
import Locations as L

###########################################################
###########################################################
# NEXT TODO: Alignments, select box for items, fertilizer #
# Fix placing plots, pens inside others                   #
# Obstacles generating inside plots, pens, buildings      #
# Finalize shops                                          #
# Obstacles generated based on location                   #
# Buying animals, buying pens/plots                       #
###########################################################
###########################################################
# Add in dictionaries
# Use .convert() after loading each image?
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Window")
clock = pygame.time.Clock()

pygame.font.init()
textFont = pygame.font.SysFont('Times New Roman', 20)

run = True
last_pressG = 0
last_pressP = 0
last_pressD = 0
last_mouse = 0
count = 0
player = GC.Player(0,0,80,80)
bg = BGM.Background("Test", 0, 0)

locations = {"Field" : L.Location("Field"),
             "Shop" : L.Location("Shop")}
curr_loc = locations["Shop"]
curr_loc.shops.append(SC.Inventory("Shop"))
curr_loc.background = BGM.Background("mapTest", 0, 0)
curr_loc.shops[0].addToInvnt(DF.getItem("Turnip_Seed", 50))
curr_loc.shops[0].addToInvnt(DF.getItem("Carrot_Seed", 50))
curr_loc.shops[0].addToInvnt(DF.getItem("Turnip", 50))
curr_loc.shops[0].addToInvnt(DF.getItem("Carrot", 50))
curr_loc.shops[0].addToInvnt(DF.getItem("Evil_Carrot", 50))
curr_loc.shops[0].addToInvnt(DF.getItem("Holy_Carrot", 50))
curr_loc.collisions = C.Collision()
curr_loc = locations["Field"]

placableLocs = ["Shop"]

# TODO Initialize location background, shops, collisions in separate file/function
curr_loc.background = BGM.Background("Test", 0, 0)

curr_loc.collisions = C.Collision()

shop = GC.Building("Shop", 100, 500)
curr_loc.buildings.append(shop)

invt = SC.Inventory("Player", 50)
invnt_open = False
check = False
pygame.mouse.set_visible(False)
invntindex = 0
rotation = 0
chest = SC.Inventory("Storage")
pen = None
while run:
    clock.tick(20)
    count += 1
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                          
    keys = pygame.key.get_pressed()

    if keys[pygame.K_s]:
        if curr_loc.name in placableLocs:
            if count - last_pressP >= 10:
                last_pressP = count
                plt = SC.Plot()
                if GCF.placePenPlot(plt, (260,260), WIN, (WIDTH,HEIGHT), locations["Field"]):
                    locations["Field"].plots.append(plt)
            
    if keys[pygame.K_q]:
        if curr_loc.name == "Field":
            if count - last_pressP >= 10:        
                curr_loc.collisions.obsList = [None] * 10
                curr_loc.collisions.tempCollPlacements = set([(100,100), (200,200), (300,300), (400,400), (500,500), (600,600), (700,700), (800,800), (900,900), (1000,1000), (200, 100), (300,100), (500,600), (100,400), (200, 600)])
                curr_loc.collisions.tempCollPositions  = set()
                curr_loc.collisions.generate()
        
    if keys[pygame.K_m]:
        interactive_plot = []
        interactive_plot = [player.checkTouching(curr_loc)]
        if isinstance(interactive_plot[0], SC.Pen):
            interactive_plot[0].milk(invt)
            
    if keys[pygame.K_r]:
        if count - last_pressP >= 10:
            last_pressP = count
            rotation = (rotation + 1 ) % 4
    
    if keys[pygame.K_t]:
        if count - last_pressP >= 10:
            last_pressP = count
            InvntF.inventoryShop(invt, chest, invntindex, WIN, (WIDTH,HEIGHT))

    if keys[pygame.K_a]:
        if curr_loc.name in placableLocs:
            if count - last_pressP >= 10:
                last_pressP = count
                pen = SC.Pen()
                if GCF.placePenPlot(pen, (260,260), WIN, (WIDTH,HEIGHT), locations["Field"]):
                    locations["Field"].pens.append(pen)
               
    if keys[pygame.K_w]:
        interactive_plot = []
        interactive_plot = [player.checkTouching(curr_loc)]
        if isinstance(interactive_plot[0], SC.Pen):
            interactive_plot[0].addAnimal("Lesser_Wyrm", str(count))
    
    if keys[pygame.K_c]:
        interactive_plot = []
        interactive_plot = [player.checkTouching(curr_loc)]
        if isinstance(interactive_plot[0], SC.Pen):
            interactive_plot[0].addAnimal("Cow", str(count))

    if keys[pygame.K_p]:
        #check = True
        if count - last_pressP >= 10:
            last_pressP = count
            if curr_loc.name == "Shop":
                # exit shop
                curr_loc = L.swapLoc(curr_loc, locations["Field"], player, (WIDTH,HEIGHT))
                continue
            interactive_plot = []
            interactive_plot = [player.checkTouching(curr_loc)]
            if isinstance(interactive_plot[0], SC.Plot):
                 InvntF.inventoryPlant(invt, interactive_plot[0], invntindex, WIN, (WIDTH,HEIGHT))
            if isinstance(interactive_plot[0], SC.Pen):
                 InvntF.inventoryAnimal(invt, interactive_plot[0], invntindex, WIN, (WIDTH,HEIGHT))
            if isinstance(interactive_plot[0], GC.Building):
                if interactive_plot[0].checkEntrance((player.absx, player.absx+player.width), (player.absy, player.absy+player.height)):
                    # enter shop 
                     print("Enter")
                     curr_loc = L.swapLoc(curr_loc, locations["Shop"], player, (WIDTH,HEIGHT))
                
    if keys[pygame.K_h]:
        interactive_plt = [player.checkTouching(curr_loc)]
        if isinstance(interactive_plt[0], SC.Plot):
            interactive_plt[0].harvest(invt)
    if keys[pygame.K_x]:
        interactive = [player.checkTouching(curr_loc)]
        if isinstance(interactive[0], C.Obstacle):
            interactive[0].health -= 10
            if interactive[0].health <= 0:
                curr_loc.collisions.removeFromCollision(interactive[0], invt)
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
             for plt in curr_loc.plots:
                 plt.newDay()
             for pn in curr_loc.pens:
                 pn.newDay()
                 
    if keys[pygame.K_b]:
        if curr_loc.name == "Shop":
            if count - last_pressP >= 10:
                last_pressP = count
                InvntF.inventoryShop(invt, curr_loc.shops[0], invntindex, WIN, (WIDTH,HEIGHT), shop=True)
    
    if not invnt_open:
        player.controlPlayer((WIDTH, HEIGHT), keys, curr_loc)
        
        curr_loc.drawBeforePlayer(WIN, (WIDTH,HEIGHT))        

        player.draw(WIN)
        InvntF.displayInventory(WIN, invt)
        
        curr_loc.drawAfterPlayer(WIN, (WIDTH,HEIGHT), player)
        
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
