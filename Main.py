import pygame

import GraphicsClasses as GC
import GraphicsClassFunctions as GCF


WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Window")
clock = pygame.time.Clock()

run = True
last_press = 0
count = 0
while run:
    clock.tick(20)
    count += 1
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        plt = GC.Plot(100,100)
        plt.draw(WIN) 
    if keys[pygame.K_p]:
       crp = GC.Crop("Turnip")
       crp.plant(WIN, plt)
    if keys[pygame.K_g]:
         if count - last_press >= 10:
             last_press = count
             crp.grow(WIN, plt)
         


