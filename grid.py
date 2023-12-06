import pygame

pygame.init()
color = (255,255,255) 
position = (0,0) 
canvas = pygame.display.set_mode((500,500)) 

while not exit: 
    canvas.fill(color) 
  
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True
    pygame.display.update()