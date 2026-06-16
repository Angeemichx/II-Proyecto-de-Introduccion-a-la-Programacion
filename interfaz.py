import pygame

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
chef1_pos_x = 200
chef1_pos_y = 300
chef1_velocidad_x = 0
chef1_velocidad_y = 0
chef1_direccion = "abajo"

#variables para el chef 2
chef2_pos_x = 400
chef2_pos_y = 300
chef2_velocidad_x = 0
chef2_velocidad_y = 0
chef2_direccion = "abajo"

#estado o mapa del juego
estado = "menu"
chef_activo = 1


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
    chef1_pos_x += chef1_velocidad_x
    chef1_pos_y += chef1_velocidad_y
    chef2_pos_x += chef2_velocidad_x
    chef2_pos_y += chef2_velocidad_y

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
