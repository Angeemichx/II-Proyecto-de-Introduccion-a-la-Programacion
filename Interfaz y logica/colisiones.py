import pygame
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

ANCHO = 1280
ALTO = 720
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)  # ← agregá FULLSCREEN
mapa = pygame.image.load("mapa_1.png").convert()

estaciones = [
    #pygame.Rect(1025, 228, 162, 182),
    #pygame.Rect(757,  397, 100, 109),
    #pygame.Rect(657,  399,  95, 106),
    #pygame.Rect(506,  396, 103, 109),
    #pygame.Rect(397,  395,  98, 114),
    #pygame.Rect(329,  117,  90,  96),
    #pygame.Rect(455,  115, 104,  97),
    pygame.Rect(571,  113, 103,  99),
    pygame.Rect(684,  113, 106, 101),
    pygame.Rect(824,  119,  87, 102),
    pygame.Rect(121,  115,  97,  82),
    pygame.Rect(121,  211,  95,  66),
    #pygame.Rect(120,  293,  95,  70),
    pygame.Rect(120,  377,  98,  70),
    #pygame.Rect(120,  460,  98,  68),
]

corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                corriendo = False

    ventana.blit(mapa, (0, 0))
    for est in estaciones:
        pygame.draw.rect(ventana, (255, 0, 0), est, 3)

    pygame.display.update()

pygame.quit()

"""import pygame
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

chef = pygame.image.load("chef1_a.png")
print("Ancho:", chef.get_width())
print("Alto:", chef.get_height())

pygame.quit()"""