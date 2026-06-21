import pygame
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

ANCHO = 1280
ALTO = 720
ventana = pygame.display.set_mode((ANCHO, ALTO))
mapa = pygame.image.load("mapa_2.png").convert()

corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(f"Click en: x={x}, y={y}")

    ventana.blit(mapa, (0, 0))
    pygame.display.update()

pygame.quit()