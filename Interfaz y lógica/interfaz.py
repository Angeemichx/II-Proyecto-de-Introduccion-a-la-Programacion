import pygame
import os 

# Encontrar archivos de imagen en la misma carpeta del presente archivo
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Se utiliza init para que las funciones dentro de pygame puedan funcionar 
pygame.init()

#Se desarrollan ciertas variables que se utilizaran constantemente con el fin de facilitar su modificación de ser necesario
ANCHO = 1280
ALTO = 720
BLANCO = (255, 255, 255)

#Con esto, se crea la ventana principal 
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN) 
pygame.display.set_caption("Crazy Snack Rush")
reloj = pygame.time.Clock()

#imágenes fondo
menu_img = pygame.image.load("menu.png").convert()
mapa_1 = pygame.image.load("mapa_1.png").convert()
mapa_2 = pygame.image.load("mapa_2.png").convert()
mapa_3 = pygame.image.load("mapa_3.png").convert()

#Imágenes de chefs 
chef1_imgs = {
    "abajo": pygame.image.load("chef1_a.png").convert_alpha(),
    "arriba": pygame.image.load("chef1_b.png").convert_alpha(),
    "izquierda": pygame.image.load("chef1_c.png").convert_alpha(),
    "derecha": pygame.image.load("chef1_d.png").convert_alpha()}

chef2_imgs = {
"abajo": pygame.image.load("chef2_a.png").convert_alpha(),
"arriba": pygame.image.load("chef2_b.png").convert_alpha(),
"izquierda": pygame.image.load("chef2_c.png").convert_alpha(),
"derecha": pygame.image.load("chef2_d.png").convert_alpha()}

#variables para chef 1
chef1_pos_x = 425
chef1_pos_y = 220
chef1_velocidad_x = 0
chef1_velocidad_y = 0
chef1_direccion = "abajo"

#variables para el chef 2
chef2_pos_x = 735
chef2_pos_y = 220
chef2_velocidad_x = 0
chef2_velocidad_y = 0
chef2_direccion = "abajo"

#estado o mapa del juego
estado = "menu"
chef_activo = 1

# Rectángulos de colisión de las estaciones (mapa_1)
estaciones = [
    pygame.Rect(1025, 228, 162, 182),  # estación 1
    pygame.Rect(757,  397, 100, 109),  # estación 2
    pygame.Rect(657,  399,  95, 106),  # estación 3
    pygame.Rect(506,  396, 103, 109),  # estación 4
    pygame.Rect(397,  395,  98, 114),  # estación 5
    pygame.Rect(329,  117,  90,  96),  # estación 6
    pygame.Rect(455,  115, 104,  97),  # estación 7
    pygame.Rect(571,  113, 103,  99),  # estación 8
    pygame.Rect(684,  113, 106, 101),  # estación 9
    pygame.Rect(824,  119,  87, 102),  # estación 10
    pygame.Rect(121,  115,  97,  82),  # estación 11
    pygame.Rect(121,  211,  95,  66),  # estación 12
    pygame.Rect(120,  293,  95,  70),  # estación 13
    pygame.Rect(120,  377,  98,  70),  # estación 14
    pygame.Rect(120,  460,  98,  68),  # estación 15 
    ]

#Esta función permite que la pantalla no se cierre mientras se está jugando, además se añade la x superior derecha y la tecla esc para cerrar la ventana (salir del bucle)
jugando = True 

while jugando:

    reloj.tick(60)

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            jugando = False 

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                jugando = False 

            #cambiar de personaje con shift
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                if chef_activo == 1:
                    chef_activo = 2
                else:
                    chef_activo = 1
            
            #entrar al mapa desde el menú
            if event.key == pygame.K_RETURN and estado == "menu":
                estado = "mapa_1"

            #Controles cuando se presiona una tecla
            if chef_activo == 1:
                if event.key == pygame.K_d:
                    chef1_direccion = "derecha"
                    chef1_velocidad_x = 5

                if event.key == pygame.K_a:
                    chef1_direccion = "izquierda"
                    chef1_velocidad_x = -5

                if event.key == pygame.K_s:
                    chef1_direccion = "abajo"
                    chef1_velocidad_y = 5

                if event.key == pygame.K_w:
                    chef1_direccion = "arriba"
                    chef1_velocidad_y = -5
            else:
                if event.key == pygame.K_d:
                    chef2_direccion = "derecha"
                    chef2_velocidad_x = 5

                if event.key == pygame.K_a:
                    chef2_direccion = "izquierda"
                    chef2_velocidad_x = -5

                if event.key == pygame.K_s:
                    chef2_direccion = "abajo"
                    chef2_velocidad_y = 5

                if event.key == pygame.K_w:
                    chef2_direccion = "arriba"
                    chef2_velocidad_y = -5
        
        #Controles cuando se suelta una tecla 
        elif event.type == pygame.KEYUP:
        
            if event.key == pygame.K_d:
                chef1_velocidad_x = 0
                chef2_velocidad_x = 0

            if event.key == pygame.K_a:
                chef1_velocidad_x = 0
                chef2_velocidad_x = 0

            if event.key == pygame.K_s:
                chef1_velocidad_y = 0
                chef2_velocidad_y = 0

            if event.key == pygame.K_w:
                chef1_velocidad_y = 0
                chef2_velocidad_y = 0
            
    #Lógica de posiciones 
    # Tamaño del chef 

    CHEF_ANCHO = 200
    CHEF_ALTO  = 200

    # Mover chef1 con colisión
    nuevo_x1 = chef1_pos_x + chef1_velocidad_x
    nuevo_y1 = chef1_pos_y + chef1_velocidad_y
    rect_chef1 = pygame.Rect(nuevo_x1 + 60, nuevo_y1 + 80, 80, 100)

    colision1 = False
    for est in estaciones:
        if rect_chef1.colliderect(est):
            colision1 = True
            break

    if not colision1:
        chef1_pos_x = nuevo_x1
        chef1_pos_y = nuevo_y1

    #Mover chef2 con colisión
    nuevo_x2 = chef2_pos_x + chef2_velocidad_x
    nuevo_y2 = chef2_pos_y + chef2_velocidad_y
    rect_chef2 = pygame.Rect(nuevo_x2 + 60, nuevo_y2 + 80, 80, 100)

    colision2 = False
    for est in estaciones:
        if rect_chef2.colliderect(est):
            colision2 = True
            break

    if not colision2:
        chef2_pos_x = nuevo_x2
        chef2_pos_y = nuevo_y2



    #Se configurarán los dibujos de la pantalla y menu
    if estado == "menu":
        ventana.blit(menu_img, (0, 0))
        fuente = pygame.font.SysFont("Arial", 48)
        texto = fuente.render("Presiona ENTER para jugar", True, BLANCO)
        ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2))

    elif estado == "mapa_1":
        ventana.blit(mapa_1, (0, 0))
        #Dibujar chef según dirección actual
        ventana.blit(chef1_imgs[chef1_direccion], (chef1_pos_x, chef1_pos_y))
        ventana.blit(chef2_imgs[chef2_direccion], (chef2_pos_x, chef2_pos_y))
    

    elif estado == "mapa_2":
        ventana.blit(mapa_2, (0, 0))
        ventana.blit(chef1_imgs[chef1_direccion], (chef1_pos_x, chef1_pos_y))
        ventana.blit(chef2_imgs[chef2_direccion], (chef2_pos_x, chef2_pos_y))

    elif estado == "mapa_3":
        ventana.blit(mapa_3, (0, 0))
        ventana.blit(chef1_imgs[chef1_direccion], (chef1_pos_x, chef1_pos_y))
        ventana.blit(chef2_imgs[chef2_direccion], (chef2_pos_x, chef2_pos_y))

    #Actualizar (se produce lo guardado en memoria)
    pygame.display.update()

#Permitir que el juego tenga un final y no se ejecuten las funciones para siempre en el bucle
pygame.quit()
