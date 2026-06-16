import pygame
pygame.init()

ANCHO = 800
ALTO = 600
ROJO = (255, 0, 0)

ventana = pygame.display.set_mode((ANCHO, ALTO)) 

pygame.time.delay(4000)

jugando = True 
while jugando:
    ventana.fill(ROJO)
    pygame.display.update

pygame.quit()