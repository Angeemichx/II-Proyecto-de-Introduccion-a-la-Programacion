import pygame
import os 
from logica import Chef, VegetalesYFrutas, PanesYBases, Proteina, Papas, Cocina, recetas_nivel1, recetas_nivel2, recetas_nivel3
from mejoras import ChefControlado
 
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()
 
ANCHO = 1280
ALTO = 720
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 220, 0)
ROJO = (255, 0, 0)
 
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN) 
pygame.display.set_caption("Crazy Snack Rush")
reloj = pygame.time.Clock()
 
menu_img = pygame.image.load("menu.png").convert()
mapa_1 = pygame.image.load("mapa_1.png").convert()
mapa_2 = pygame.image.load("mapa_2.png").convert()
mapa_3 = pygame.image.load("mapa_3.png").convert()
 
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
 
chef1_ensalada_imgs = {
    "abajo": pygame.image.load("chef1_ensalada_a.png").convert_alpha(),
    "arriba": pygame.image.load("chef1_ensalada_a.png").convert_alpha(),
    "izquierda": pygame.image.load("chef1_ensalada_c.png").convert_alpha(),
    "derecha": pygame.image.load("chef1_ensalada_b.png").convert_alpha()}
 
chef2_ensalada_imgs = {
    "abajo": pygame.image.load("chef2_ensalada_a.png").convert_alpha(),
    "arriba": pygame.image.load("chef2_ensalada_a.png").convert_alpha(),
    "izquierda": pygame.image.load("chef2_ensalada_c.png").convert_alpha(),
    "derecha": pygame.image.load("chef2_ensalada_b.png").convert_alpha()}
 
chef1_hd_imgs = {
    "abajo": pygame.image.load("chef1_hd_a.png").convert_alpha(),
    "arriba": pygame.image.load("chef1_hd_a.png").convert_alpha(),
    "izquierda": pygame.image.load("chef1_hd_c.png").convert_alpha(),
    "derecha": pygame.image.load("chef1_hd_b.png").convert_alpha()}
 
chef2_hd_imgs = {
    "abajo": pygame.image.load("chef2_hd_a.png").convert_alpha(),
    "arriba": pygame.image.load("chef2_hd_a.png").convert_alpha(),
    "izquierda": pygame.image.load("chef2_hd_c.png").convert_alpha(),
    "derecha": pygame.image.load("chef2_hd_b.png").convert_alpha()}
 
chef1_empanada_imgs = {
    "abajo": pygame.image.load("chef1_empanada_a.png").convert_alpha(),
    "arriba": pygame.image.load("chef1_empanada_a.png").convert_alpha(),
    "izquierda": pygame.image.load("chef1_empanada_c.png").convert_alpha(),
    "derecha": pygame.image.load("chef1_empanada_b.png").convert_alpha()}
 
chef2_empanada_imgs = {
    "abajo": pygame.image.load("chef2_empanada_a.png").convert_alpha(),
    "arriba": pygame.image.load("chef2_empanada_a.png").convert_alpha(),
    "izquierda": pygame.image.load("chef2_empanada_c.png").convert_alpha(),
    "derecha": pygame.image.load("chef2_empanada_b.png").convert_alpha()}
 
chef1_salch_imgs = {
    "abajo": pygame.image.load("chef1_salch_a.png").convert_alpha(),
    "arriba": pygame.image.load("chef1_salch_a.png").convert_alpha(),
    "izquierda": pygame.image.load("chef1_salch_c.png").convert_alpha(),
    "derecha": pygame.image.load("chef1_salch_b.png").convert_alpha()}
 
chef2_salch_imgs = {
    "abajo": pygame.image.load("chef2_salch_a.png").convert_alpha(),
    "arriba": pygame.image.load("chef2_salch_a.png").convert_alpha(),
    "izquierda": pygame.image.load("chef2_salch_c.png").convert_alpha(),
    "derecha": pygame.image.load("chef2_salch_b.png").convert_alpha()}
 
chef1_obj = ChefControlado("Chef 1", chef1_imgs, 425, 210)
chef2_obj = ChefControlado("Chef 2", chef2_imgs, 735, 210)
chef1_obj.activo = True
 
estado = "menu"
chef_activo = 1
mesa_a = []
mesa_b = []
 
dispensadores_mapa1 = { 
    11: lambda: VegetalesYFrutas("Banano"), 
    12: lambda: VegetalesYFrutas("Fresa"), 
    13: lambda: VegetalesYFrutas("Mango"), 
    14: lambda: VegetalesYFrutas("Lechuga"), 
    15: lambda: Proteina("Pollo")}
 
dispensadores_mapa2 = {
    11: lambda: PanesYBases("Pan"),
    12: lambda: Proteina("Salchicha"),
    13: lambda: VegetalesYFrutas("Repollo"),
    14: lambda: Papas()}
 
dispensadores_mapa3 = {
    11: lambda: Proteina("Pollo"),
    12: lambda: PanesYBases("Queso"),
    13: lambda: Papas(),
    14: lambda: Proteina("Salchicha"),
    15: lambda: PanesYBases("Empanada")}
 
procesadores_est = {
    2: "freir", 3: "freir", 4: "cortar", 5: "cortar",
    7: "cocinar", 8: "cocinar", 9: "cocinar"}
 
estaciones = [
    pygame.Rect(1025, 228, 162, 182), pygame.Rect(757,  397, 100, 109),
    pygame.Rect(657,  399,  95, 106), pygame.Rect(506,  396, 103, 109),
    pygame.Rect(397,  395,  98, 114), pygame.Rect(329,  117,  90,  96),
    pygame.Rect(455,  115, 104,  97), pygame.Rect(571,  113, 103,  99),
    pygame.Rect(684,  113, 106, 101), pygame.Rect(824,  119,  87, 102),
    pygame.Rect(121,  90,  97,  82), pygame.Rect(121,  180,  95,  66),
    pygame.Rect(120,  260,  95,  70), pygame.Rect(120,  340,  98,  70),
    pygame.Rect(120,  420,  98,  68)]
 
estaciones_mapa2 = [
    pygame.Rect(1026, 231, 161, 174), pygame.Rect(764,  410,  80,  93),
    pygame.Rect(665,  410,  90,  88), pygame.Rect(405,  406,  97,  99),
    pygame.Rect(506,  407,  95,  97), pygame.Rect(326,  131,  81,  87),
    pygame.Rect(454,  120, 110,  90), pygame.Rect(573,  120,  96,  98),
    pygame.Rect(678,  118, 118,  99), pygame.Rect(831,  125,  82,  92),
    pygame.Rect(112,  125,  97,  84), pygame.Rect(117,  215,  89,  75),
    pygame.Rect(121,  305,  74,  71), pygame.Rect(128,  395,  65,  74)]
 
estaciones_mapa3 = [
    pygame.Rect(1025, 229, 155, 174), pygame.Rect(748,  411,  81,  92),
    pygame.Rect(656,  408,  85,  97), pygame.Rect(501,  408,  99,  98),
    pygame.Rect(395,  406, 100, 104), pygame.Rect(316,  124,  91,  91),
    pygame.Rect(451,  117, 114,  98), pygame.Rect(562,  118, 120,  97),
    pygame.Rect(681,  123, 112,  99), pygame.Rect(835,  123,  85,  93),
    pygame.Rect(106,  90,  91,  75), pygame.Rect(106,  170,  92,  67),
    pygame.Rect(109,  245,  89,  76), pygame.Rect(109,  310,  89,  73),
    pygame.Rect(109,  390,  89,  78)]
 
fuente_grande = pygame.font.SysFont("Arial", 36)
fuente_pequeña = pygame.font.SysFont("Arial", 22)
 
def iniciar_nivel(nivel):
    global cocina, mesa_a, mesa_b
    
    chef1_obj.pos_x, chef1_obj.pos_y = 425, 210
    chef2_obj.pos_x, chef2_obj.pos_y = 735, 210
    chef1_obj.soltar()
    chef2_obj.soltar()
    chef1_obj.imagenes = chef1_imgs
    chef2_obj.imagenes = chef2_imgs
    chef1_obj.plato_sostenido = None
    chef2_obj.plato_sostenido = None
    mesa_a.clear()
    mesa_b.clear()
 
    if nivel == 1:
        cocina = Cocina(120, [chef1_obj, chef2_obj], recetas_nivel1)
    elif nivel == 2:
        cocina = Cocina(120, [chef1_obj, chef2_obj], recetas_nivel2)
    elif nivel == 3:
        cocina = Cocina(120, [chef1_obj, chef2_obj], recetas_nivel3)
    cocina.GenerarReceta()
 
iniciar_nivel(1)
jugando = True 
while jugando:
    delta = reloj.tick(60) / 1000
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                jugando = False 
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                chef_activo = 2 if chef_activo == 1 else 1
            if event.key == pygame.K_RETURN and estado == "menu":
                estado = "mapa_1"
            if event.key == pygame.K_RETURN and estado == "fin_juego":
                estado = "mapa_1"
                iniciar_nivel(1)
                chef1_obj.puntos = 0
                chef2_obj.puntos = 0
            
            if event.key == pygame.K_SPACE and estado in ("mapa_1", "mapa_2", "mapa_3"):
                ests_activas = estaciones if estado == "mapa_1" else (estaciones_mapa2 if estado == "mapa_2" else estaciones_mapa3)
                disps_activos = dispensadores_mapa1 if estado == "mapa_1" else (dispensadores_mapa2 if estado == "mapa_2" else dispensadores_mapa3)
                
                chef_actual = chef1_obj if chef_activo == 1 else chef2_obj
                hitbox = chef_actual.obtener_rect_interaccion()
                
                for i, est in enumerate(ests_activas):
                    num_est = i + 1
                    if not hitbox.colliderect(est):
                        continue
                    
                    if num_est in disps_activos and chef_actual.ingrediente is None:
                        nuevo_ing = disps_activos[num_est]()
                        chef_actual.recoger(nuevo_ing)
                        print(f"Chef {chef_activo} recogió: {nuevo_ing.nombre}")
                        break
                    
                    if num_est in procesadores_est and chef_actual.ingrediente is not None:
                        accion = procesadores_est[num_est]
                        ing = chef_actual.ingrediente
                        try:
                            if accion == "cortar":
                                if isinstance(ing, VegetalesYFrutas):
                                    ing.cortar()
                                    print(f"{ing.nombre} cortado")
                                else:
                                    print(f"{ing.nombre} no puede cortarse")
                            elif accion == "cocinar":
                                if isinstance(ing, Proteina):
                                    ing.estado = "preparado"
                                    print(f"{ing.nombre} cocinado")
                                else:
                                    print(f"{ing.nombre} no puede cocinarse")
                            elif accion == "freir":
                                if isinstance(ing, Papas):
                                    ing.estado= "preparado"
                                    print(f"{ing.nombre} frito")
                                else:
                                    print(f"{ing.nombre} no puede freírse")
                            elif isinstance(ing, Proteina):
                                print(f"{ing.nombre} no pukede freírse")
                                print(f"Friendo {ing.nombre}: estado {ing.estado}")
                            else:
                                print(f"{ing.nombre} no puede freírse")
                        except Exception as e:
                            print("Error procesando ingrediente:", e)
                        break
                    
                    if num_est == 6:
                        if chef_actual.ingrediente is not None:
                            mesa_a.append(chef_actual.soltar())
                            chef_actual.plato_sostenido = "Mesa A"
                            chef_actual.imagenes = chef1_ensalada_imgs if chef_activo == 1 else chef2_ensalada_imgs
                            print(f"Mesa A: {[i.nombre for i in mesa_a]}")
                        break
                        
                    if num_est == 10:
                        if chef_actual.ingrediente is not None:
                            mesa_b.append(chef_actual.soltar())
                            chef_actual.plato_sostenido = "Mesa B"
                            chef_actual.imagenes = chef1_ensalada_imgs if chef_activo == 1 else chef2_ensalada_imgs
                            print(f"Mesa B: {[i.nombre for i in mesa_b]}")
                        break
                    
                    if num_est == 1:
                        todos = mesa_a + mesa_b
                        if chef_actual.ingrediente is not None:
                            todos.append(chef_actual.soltar())
                        if todos:
                            print("ENTREGANDO:")
                            for ing in todos:
                                print(ing.nombre, ing.estado)
                            print("\nORDENES ACTIVAS:")
                            for orden in cocina.ordenes:
                                print(orden.nombre)    
                            resultado = cocina.entregar(todos)
                            if resultado:
                                print(f"Receta entregada: {resultado}")
                                mesa_a.clear()
                                mesa_b.clear()
                                chef_actual.plato_sostenido = None
                                chef1_obj.imagenes = chef1_imgs
                                chef2_obj.imagenes = chef2_imgs
                            else:
                                print("Receta incorrecta, -10 puntos")
                        break
 
            if event.key == pygame.K_p:
                chef_actual = chef1_obj if chef_activo == 1 else chef2_obj
                if chef_actual.plato_sostenido:
                    if chef_actual.plato_sostenido == "Mesa A":
                        mesa_a.clear()
                    elif chef_actual.plato_sostenido == "Mesa B":
                        mesa_b.clear()
                    chef_actual.plato_sostenido = None
                    chef_actual.imagenes = chef1_imgs if chef_activo == 1 else chef2_imgs
                    print("Plato botado")
                elif chef_actual.ingrediente is not None:
                    print(f"botado: {chef_actual.ingrediente.nombre}")
                    chef_actual.soltar()
 
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
 
    ests_colision = (estaciones if estado == "mapa_1" else (estaciones_mapa2 if estado == "mapa_2" else estaciones_mapa3)) if estado in ("mapa_1", "mapa_2", "mapa_3") else []
    teclas = pygame.key.get_pressed()
    
    if chef_activo == 1:
        chef1_obj.mover(teclas, (0, 0, ANCHO, ALTO), ests_colision)
    else:
        chef2_obj.mover(teclas, (0, 0, ANCHO, ALTO), ests_colision)
 
    if estado == "menu":
        ventana.blit(menu_img, (0, 0))
        fuente = pygame.font.SysFont("Arial", 48)
        texto = fuente.render("Presiona ENTER para jugar", True, BLANCO)
        ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2))
    elif estado in ("mapa_1", "mapa_2", "mapa_3"):
        ventana.blit(mapa_1 if estado == "mapa_1" else (mapa_2 if estado == "mapa_2" else mapa_3), (0, 0))
        chef1_obj.dibujar(ventana, resaltar=(chef_activo == 1))
        chef2_obj.dibujar(ventana, resaltar=(chef_activo == 2))
 
        ventana.blit(fuente_grande.render(f"Tiempo: {int(cocina.tiempo_restante)}s", True, BLANCO), (20, 20))
        ventana.blit(fuente_grande.render(f"Puntos: {chef1_obj.puntos + chef2_obj.puntos}", True, BLANCO), (ANCHO - 250, 20))
        ventana.blit(fuente_pequeña.render("ÓRDENES:", True, BLANCO), (ANCHO//2 - 60, 10))
        for idx, orden in enumerate(cocina.ordenes):
            color = ROJO if orden.puntos_actuales < orden.PuntosReceta else BLANCO
            txt = f"{orden.nombre} / {orden.puntos_actuales}pts / {int(orden.MaxTimeReceta - orden.tiempo_transcurrido)}s"
            ventana.blit(fuente_pequeña.render(txt, True, color), (ANCHO//2 - 150, 35 + idx * 25))
 
        ventana.blit(fuente_pequeña.render("P = tirar plato/ingrediente", True, ROJO), (20, ALTO - 40))
 
        y_pos = ALTO - 40
        if mesa_a:
            txt = "Mesa A: " + ", ".join(i.nombre for i in mesa_a)
            ventana.blit(fuente_pequeña.render(txt, True, AMARILLO), (320, y_pos))
            y_pos -= 25
        if mesa_b:
            txt = "Mesa B: " + ", ".join(i.nombre for i in mesa_b)
            ventana.blit(fuente_pequeña.render(txt, True, AMARILLO), (320, y_pos))
 
    elif estado == "fin_juego":
        ventana.fill(NEGRO)
        puntos_totales = chef1_obj.puntos + chef2_obj.puntos
        ventana.blit(fuente_grande.render("¡Juego terminado!", True, BLANCO), (ANCHO//2 - 150, ALTO//2 - 80))
        ventana.blit(fuente_grande.render(f"Puntos totales: {puntos_totales}", True, AMARILLO), (ANCHO//2 - 150, ALTO//2))
        ventana.blit(fuente_grande.render("ENTER para jugar de nuevo", True, BLANCO), (ANCHO//2 - 180, ALTO//2 + 80))
        ventana.blit(fuente_grande.render("ESC para salir", True, BLANCO), (ANCHO//2 - 120, ALTO//2 + 120))
 
    pygame.display.update()
 
pygame.quit()