import pygame
import os 
from logica import (Chef, VegetalesYFrutas, PanesYBases, Proteina, Papas, Cocina, recetas_nivel1, recetas_nivel2, recetas_nivel3)

# Encontrar archivos de imagen en la misma carpeta del presente archivo
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Se utiliza init para que las funciones dentro de pygame puedan funcionar 
pygame.init()

#Se desarrollan ciertas variables que se utilizaran constantemente con el fin de facilitar su modificación de ser necesario
ANCHO = 1280
ALTO = 720
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 220, 0)
ROJO = (255, 0, 0)
CHEF_ANCHO = 200
CHEF_ALTO = 200

#Con esto, se crea la ventana principal 
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN) 
pygame.display.set_caption("Crazy Snack Rush")
reloj = pygame.time.Clock()

#IMAGENES------------------------------------------
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

#Objetos creados en la lógica
chef1_obj = Chef("Chef 1")
chef2_obj = Chef("Chef 2")
cocina = Cocina(tiempo = 120, chefs = [chef1_obj, chef2_obj], recetas_posibles = recetas_nivel1)
cocina.GenerarReceta() #Para generar la primer receta

#VARIABLES----------------------------------------------------
#variables de posiciones para chef 1 
chef1_pos_x = 425
chef1_pos_y = 210
chef1_velocidad_x = 0
chef1_velocidad_y = 0
chef1_direccion = "abajo"

#variables de posiciones para el chef 2
chef2_pos_x = 735
chef2_pos_y = 210
chef2_velocidad_x = 0
chef2_velocidad_y = 0
chef2_direccion = "abajo"

#estado o mapa del juego
estado = "menu"
chef_activo = 1

#ingredientes que lleva cada chef, para iniciar ninguno, se utiliza el objeto creado en la lógica
chef1_ingrediente = None
chef2_ingrediente = None

# diccionario para dispensadores según la estación al presionar letra E, se utiliza lambda para escribir las funciones en una sola línea y que el objeto no se guarde inmediatamente en memoria, sino hasta que se llame a la función
#Para el mapa 1 - ensaladas
dispensadores_mapa1 = { 
    11: lambda: VegetalesYFrutas("Banano"), 
    12: lambda: VegetalesYFrutas("Fresa"), 
    13: lambda: VegetalesYFrutas("Mango"), 
    14: lambda: VegetalesYFrutas("Lechuga"), 
    15: lambda: Proteina("Pollo")}

#Para el mapa 2 - perros calientes
dispensadores_mapa2 = {
    11: lambda: PanesYBases("Pan"),
    12: lambda: Proteina("Salchicha"),
    13: lambda: VegetalesYFrutas("Repollo"),
    14: lambda: Papas()}

#Para el mapa 3 - empanadas "soda"
dispensadores_mapa3 = {
    11: lambda: Proteina("Pollo"),
    12: lambda: PanesYBases("Queso"),
    13: lambda: PanesYBases("Empanada"),
    14: lambda: Proteina("Salchicha"),
    15: lambda: Papas()}

# Indicar qué acción realiza cada estación
procesadores_est ={
    2: "freir",
    3: "freir",
    4: "cortar",
    5: "cortar",
    7: "cocinar",
    8: "cocinar",
    9: "cocinar"}

#Mesa de ensamblaje en las estaciones 6 y 10 para guardar recetas armadas
mesa_a = [] #Es la estación 6
mesa_b = [] #Es la estación 10


# Rectángulos de colisión de las estaciones en todos los mapas
estaciones = [
    pygame.Rect(1025, 228, 162, 182),  # estación 1, entregas
    pygame.Rect(757,  397, 100, 109),  # estación 2, freidora a
    pygame.Rect(657,  399,  95, 106),  # estación 3, freidora b
    pygame.Rect(506,  396, 103, 109),  # estación 4, tabla a 
    pygame.Rect(397,  395,  98, 114),  # estación 5, tabla b
    pygame.Rect(329,  117,  90,  96),  # estación 6, mesa con plato a
    pygame.Rect(455,  115, 104,  97),  # estación 7, cocina a
    pygame.Rect(571,  113, 103,  99),  # estación 8, cocina b 
    pygame.Rect(684,  113, 106, 101),  # estación 9, cocina c 
    pygame.Rect(824,  119,  87, 102),  # estación 10, mesa con plato b
    pygame.Rect(121,  115,  97,  82),  # estación 11, dispensador de bananos
    pygame.Rect(121,  211,  95,  66),  # estación 12, dispensador de fresas
    pygame.Rect(120,  293,  95,  70),  # estación 13, dispensador de mangos 
    pygame.Rect(120,  377,  98,  70),  # estación 14, dispensador de lechuga
    pygame.Rect(120,  460,  98,  68)  # estación 15, dispensador de pollo
    ]

estaciones_mapa2 = [
    pygame.Rect(1026, 231, 161, 174),  # 1  entregas
    pygame.Rect(764,  410,  80,  93),  # 2  freidora a
    pygame.Rect(665,  410,  90,  88),  # 3  freidora b
    pygame.Rect(405,  406,  97,  99),  # 4  tabla a
    pygame.Rect(506,  407,  95,  97),  # 5  tabla b
    pygame.Rect(326,  131,  81,  87),  # 6  mesa plato a
    pygame.Rect(454,  120, 110,  90),  # 7  cocina a
    pygame.Rect(573,  120,  96,  98),  # 8  cocina b
    pygame.Rect(678,  118, 118,  99),  # 9  cocina c
    pygame.Rect(831,  125,  82,  92),  # 10 mesa plato b
    pygame.Rect(112,  151,  97,  84),  # 11 dispensador pan
    pygame.Rect(117,  249,  89,  75),  # 12 dispensador salchicha
    pygame.Rect(121,  345,  74,  71),  # 13 dispensador repollo
    pygame.Rect(128,  435,  65,  74)  # 14 dispensador papas
    ]

estaciones_mapa3 = [
    pygame.Rect(1025, 229, 155, 174),  # 1  entregas
    pygame.Rect(748,  411,  81,  92),  # 2  freidora a
    pygame.Rect(656,  408,  85,  97),  # 3  freidora b
    pygame.Rect(501,  408,  99,  98),  # 4  tabla a
    pygame.Rect(395,  406, 100, 104),  # 5  tabla b
    pygame.Rect(316,  124,  91,  91),  # 6  mesa plato a
    pygame.Rect(451,  117, 114,  98),  # 7  cocina a
    pygame.Rect(562,  118, 120,  97),  # 8  cocina b
    pygame.Rect(681,  123, 112,  99),  # 9  cocina c
    pygame.Rect(835,  123,  85,  93),  # 10 mesa plato b
    pygame.Rect(106,  119,  91,  75),  # 11 dispensador pollo
    pygame.Rect(106,  205,  92,  67),  # 12 dispensador queso
    pygame.Rect(109,  283,  89,  76),  # 13 dispensador empanada
    pygame.Rect(109,  356,  89,  73),  # 14 dispensador salchicha
    pygame.Rect(109,  440,  89,  78)  # 15 dispensador papas
    ]

fuente_grande = pygame.font.SysFont("Arial", 36)
fuente_pequeña = pygame.font.SysFont("Arial", 22)

#Función para realizar cambios de mapa y reiniciar la cocina
def iniciar_nivel(nivel):
    global cocina, chef1_pos_x, chef1_pos_y, chef2_pos_x, chef2_pos_y
    global chef1_ingrediente, chef2_ingrediente
    
    chef1_pos_x, chef1_pos_y = 425, 210
    chef2_pos_x, chef2_pos_y = 735, 210
    chef1_ingrediente = None
    chef2_ingrediente = None
    mesa_a.clear()
    mesa_b.clear()

    if nivel == 1:
        cocina = Cocina(120, [chef1_obj, chef2_obj], recetas_nivel1)
    elif nivel == 2:
        cocina = Cocina(120, [chef1_obj, chef2_obj], recetas_nivel2)
    elif nivel == 3:
        cocina = Cocina(120, [chef1_obj, chef2_obj], recetas_nivel3)
    cocina.GenerarReceta()


#Esta función permite que la pantalla no se cierre mientras se está jugando, además se añade la x superior derecha y la tecla esc para cerrar la ventana (salir del bucle)
jugando = True 
#TECLAS/EVENTOS-----------------------------------------------------------------------------
while jugando:

    delta = reloj.tick(60) / 1000 #segundos desde el últmo frame

    for event in pygame.event.get():
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

            #Recoger alimentos al presionar espacio
            if event.key == pygame.K_SPACE and estado in ("mapa_1", "mapa_2", "mapa_3"):
                
                #Cambio de despesa depende del nivel a jugar
                if estado == "mapa_1":
                    ests_activas = estaciones
                    disps_activos = dispensadores_mapa1
                elif estado == "mapa_2":
                    ests_activas = estaciones_mapa2
                    disps_activos = dispensadores_mapa2
                else:
                    ests_activas = estaciones_mapa3
                    disps_activos = dispensadores_mapa3
                
                # Definir hitbox del chef activo
                if chef_activo == 1:
                    hitbox_cercano = pygame.Rect(chef1_pos_x + 40, chef1_pos_y, 120, 250)
                    ingrediente_actual = chef1_ingrediente
                else:
                    hitbox_cercano = pygame.Rect(chef1_pos_x + 40, chef1_pos_y, 120, 250)
                    ingrediente_actual = chef2_ingrediente

                # Expandir hitbox para detectar estaciones cercanas
                hitbox_cercano = pygame.Rect( chef1_pos_x + 40,   #un poco adentro horizontalmente
                    chef1_pos_y,        #arriba
                    120,                #ancho
                    250)                 #alto, cubre todo el personaje

                for i, est in enumerate(ests_activas):
                    num_est = i + 1
                    if not hitbox_cercano.colliderect(est):
                        continue

                    # Dispensadores cuando las manos están vacías
                    if num_est in disps_activos and ingrediente_actual is None:
                        nuevo_ing = disps_activos[num_est]() #crear el objeto
                        if chef_activo == 1:
                            chef1_ingrediente = nuevo_ing
                        else:
                            chef2_ingrediente = nuevo_ing
                        print(f"Chef {chef_activo} recogió: {nuevo_ing.nombre}")
                        break

                    if num_est in procesadores_est and ingrediente_actual is not None:
                        accion = procesadores_est[num_est]
                        if accion == "cortar":
                            if isinstance(ingrediente_actual, VegetalesYFrutas) and not ingrediente_actual.cortado:
                                ingrediente_actual.cortar()
                                print(f"{ingrediente_actual.nombre} cortado")
                        elif accion == "cocinar":
                            if isinstance(ingrediente_actual, Proteina) and not ingrediente_actual.cocinada:
                                ingrediente_actual.cocinada = True
                                ingrediente_actual.estado = "preparado"
                                print(f"{ingrediente_actual.nombre} cocinado")
                        elif accion == "freir":
                            if isinstance(ingrediente_actual, Papas) and not ingrediente_actual.frito:
                                ingrediente_actual.frito = True
                                ingrediente_actual.estado = "preparado"
                                print(f"{ingrediente_actual.nombre} frito")
                        break

                    #Mesa de ensamblar estación 6 y 10
                    if num_est == 6:
                        if ingrediente_actual is not None:
                            mesa_a.append(ingrediente_actual)
                            if chef_activo == 1: chef1_ingrediente = None
                            else: chef2_ingrediente = None
                        break

                    if num_est == 10:
                        if ingrediente_actual is not None:
                            mesa_b.append(ingrediente_actual)
                            if chef_activo == 1: chef1_ingrediente = None
                            else: chef2_ingrediente = None
                        break

                        # Entrega estación 1
                    if num_est == 1:
                        todos = mesa_a + mesa_b
                        if ingrediente_actual is not None:
                            todos.append(ingrediente_actual)
                        if todos:
                            resultado = cocina.entregar(todos)
                            if resultado:
                                print(f"Receta entregada: {resultado}")
                                mesa_a.clear()
                                mesa_b.clear()
                                if chef_activo == 1: chef1_ingrediente = None
                                else: chef2_ingrediente = None
                            else:
                                print("Receta incorrecta")
                        break
                
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


    #Lógica------------------------------------------------
    
    #terminar el juego o pasar de nivel
    if estado == "mapa_1":
        cocina.actualizar(delta)
        if cocina.juego_terminado():
            estado = "mapa_2"
            iniciar_nivel(2)

    elif estado == "mapa_2":
        cocina.actualizar(delta)
        if cocina.juego_terminado():
            estado = "mapa_3"
            iniciar_nivel(3)

    elif estado == "mapa_3":
        cocina.actualizar(delta)
        if cocina.juego_terminado():
            estado = "fin_juego"



    #COALISIONES---------------------------------
    if estado == "mapa_1":
        ests_colision = estaciones
    elif estado == "mapa_2":
        ests_colision = estaciones_mapa2
    elif estado == "mapa_3":
        ests_colision = estaciones_mapa3
    else:
        ests_colision = []

    # Mover chef1 con colisión
    nuevo_x1 = chef1_pos_x + chef1_velocidad_x
    nuevo_y1 = chef1_pos_y + chef1_velocidad_y
    rect_chef1 = pygame.Rect(nuevo_x1 + 60, nuevo_y1 + 80, 80, 100)
    if not any(rect_chef1.colliderect(e) for e in ests_colision):
        chef1_pos_x, chef1_pos_y = nuevo_x1, nuevo_y1

    #Mover chef2 con colisión
    nuevo_x2 = chef2_pos_x + chef2_velocidad_x
    nuevo_y2 = chef2_pos_y + chef2_velocidad_y
    rect_chef2 = pygame.Rect(nuevo_x2 + 60, nuevo_y2 + 80, 80, 100)
    if not any(rect_chef2.colliderect(e) for e in ests_colision):
        chef2_pos_x, chef2_pos_y = nuevo_x2, nuevo_y2


    #DUBUJOS-----------------------------------------------------
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
        
        # Mostrar ingrediente como sobre los chef

        # ingrediente sobre chef1
        if chef1_ingrediente:
            txt = f"{chef1_ingrediente.nombre} [{chef1_ingrediente.estado}]"
            ventana.blit(fuente_pequeña.render(txt, True, AMARILLO),
                         (chef1_pos_x + 50, chef1_pos_y + 40))

        # ingrediente sobre chef2
        if chef2_ingrediente:
            txt = f"{chef2_ingrediente.nombre} [{chef2_ingrediente.estado}]"
            ventana.blit(fuente_pequeña.render(txt, True, AMARILLO),
                         (chef2_pos_x + 50, chef2_pos_y + 40))

        #tiempo y puntos
        tiempo_txt = fuente_grande.render(
            f"Tiempo: {int(cocina.tiempo_restante)}s", True, BLANCO)
        puntos_txt = fuente_grande.render(
            f"Puntos: {chef1_obj.puntos + chef2_obj.puntos}", True, BLANCO)
        ventana.blit(tiempo_txt, (20, 20))
        ventana.blit(puntos_txt, (ANCHO - 250, 20))

        #órdenes activas
        ventana.blit(fuente_pequeña.render("ÓRDENES:", True, BLANCO), (ANCHO//2 - 60, 10))
        for idx, orden in enumerate(cocina.ordenes):
            color = ROJO if orden.puntos_actuales < orden.PuntosReceta else BLANCO
            txt = f"{orden.nombre} | {orden.puntos_actuales}pts | {int(orden.MaxTimeReceta - orden.tiempo_transcurrido)}s"
            ventana.blit(fuente_pequeña.render(txt, True, color),
                         (ANCHO//2 - 150, 35 + idx * 25))

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
