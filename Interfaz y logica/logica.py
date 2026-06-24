import random
from collections import Counter

# Todos los ingredientes del juego heredan de aquí
class Ingrediente:
    def __init__(self, nombre, estado="crudo"):
        self.nombre = nombre   # Nombre del ingrediente
        self.estado = estado   # Estado actual: "crudo", "preparado", "quemado", "listo"

    def __str__(self):
        return f"{self.nombre} ({self.estado})"



# Vegetales y Frutas
# Se preparan cortándolos en la tabla de picar
class VegetalesYFrutas(Ingrediente):
    def __init__(self, nombre):
        # Los vegetales y frutas empiezan en estado crudo
        super().__init__(nombre, estado="crudo")

    def cortar(self):
        # Al cortarlos pasan a preparado
        self.estado = "preparado"


# Panes y Bases
# No necesitan preparación siempre están listos
class PanesYBases(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre, estado="listo")


# Proteína (Pollo y Salchicha)
# Se cocina en la olla, tiene un tiempo mínimo y máximo
# Antes del mínimo crudo
# Entre mínimo y máximo preparado
# Después del máximo quemado
class Proteina(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre, estado="crudo")
        self.tiempo_coccion = 0    # Acumulador de tiempo cocinando en segundos
        self.tiempo_minimo = 3     # Segundos necesarios para estar listo
        self.tiempo_maximo = 8     # Segundos a partir de los cuales se quema

    def cocinar(self, delta):
        # Se llama cada frame con el tiempo transcurrido es el delta en segundos
        self.tiempo_coccion += delta
        if self.tiempo_coccion >= self.tiempo_maximo:
            self.estado = "quemado"
        elif self.tiempo_coccion >= self.tiempo_minimo:
            self.estado = "preparado"


# Papas
# Se fríen en la freidora, solo tienen tiempo mínimo
class Papas(Ingrediente):
    def __init__(self):
        super().__init__("Papas", estado="crudo")
        self.tiempo_fritura = 0    # Acumulador de tiempo friendo
        self.tiempo_minimo = 3     # Segundos para quedar preparadas

    def freir(self, delta):
        self.tiempo_fritura += delta
        if self.tiempo_fritura >= self.tiempo_minimo:
            self.estado = "preparado"


# Estación de trabajo
# Representa una zona del mapa como un dispensador, tabla de picar, olla, freidora, entrega.
class Estacion:
    def __init__(self, nombre, ingredientes_aceptados, tipo):
        self.nombre = nombre                         
        self.ingredientes_aceptados = ingredientes_aceptados  # Lista de tipos aceptados
        self.tipo = tipo                              # cortar, cocinar, freir, entrega

    def __str__(self):
        return self.nombre


# Chef
# Guarda el nombre, puntos y el ingrediente que lleva en la mano
class Chef:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntos = 0
        self.ingrediente = None   # El chef solo puede cargar un ingrediente a la vez

    def recoger(self, ingrediente):
        #Recoger un ingrediente, solo funciona si las manos están vacías
        if self.ingrediente is None:
            self.ingrediente = ingrediente
            return True
        return False

    def soltar(self):
        #Suelta el ingrediente que lleva y lo devuelve
        ing = self.ingrediente
        self.ingrediente = None
        return ing

    def sumar_puntos(self, puntos):
        #Suma o resta puntos. El mínimo es 0
        self.puntos = max(0, self.puntos + puntos)

    def __str__(self):
        return f"{self.nombre} - Puntos: {self.puntos}"


# Receta
# Contiene la lista de ingredientes requeridos, los puntos que vale y el tiempo máximo para entregarla
class Receta:
    def __init__(self, nombre, ListaIngredientes, PuntosReceta, MaxTimeReceta):
        self.nombre = nombre
        self.ListaIngredientes = ListaIngredientes  # Lista de dicts diccionarios 
        self.PuntosReceta = PuntosReceta            # Puntos de la receta
        self.MaxTimeReceta = MaxTimeReceta          # Tiempo máximo antes de penalización
        self.tiempo_transcurrido = 0                # Tiempo acumulado desde que apareció
        self.puntos_actuales = PuntosReceta         # Puntos que dará al entregarla

    def actualizar_tiempo(self, delta):
        #Avanza el reloj de la receta. Si se supera MaxTimeReceta, los puntos se reducen a la mitad hasta llegar a 0
        self.tiempo_transcurrido += delta
        if self.tiempo_transcurrido >= self.MaxTimeReceta:
            self.puntos_actuales = max(0, self.puntos_actuales // 2)
            self.tiempo_transcurrido = 0  # Reinicia el ciclo de penalización

    def CompararReceta(self, ingredientes_entregados):
        #Compara solo por nombre sin el estado, sirve para detectar si los ingredientes son correctos, pero mal preparados
        requeridos = Counter()
        for req in self.ListaIngredientes:
            requeridos[req["nombre"]] += 1

        entregados = Counter()
        for ing in ingredientes_entregados:
            entregados[ing.nombre] += 1

        print("REQUERIDOS (nombres): ", requeridos)
        print("ENTREGADOS (nombres): ", entregados)

        return requeridos == entregados

    def CompararRecetaEstricta(self, ingredientes_entregados):
        #Compara por nombre y estado, si hay coincidencia perfecta el jugador recibe los puntos completos
        requeridos = Counter()
        for req in self.ListaIngredientes:
            requeridos[(req["nombre"], req["estado"])] += 1

        entregados = Counter()
        for ing in ingredientes_entregados:
            entregados[(ing.nombre, ing.estado)] += 1

        return requeridos == entregados

    def __str__(self):
        return f"{self.nombre} - {self.puntos_actuales} pts"


# Cocina
# Administra el tiempo, las recetas activas y los chefs
class Cocina:
    def __init__(self, tiempo, chefs, recetas_posibles):
        self.tiempo = tiempo                          # Duración total del nivel en segundos
        self.tiempo_restante = tiempo                 # Tiempo que va quedando
        self.chefs = chefs                            # Lista de chefs
        self.ordenes = []                             # Recetas actualmente visibles en pantalla
        self.recetas_posibles = recetas_posibles      # Recetas del nivel
        self.max_ordenes = 3                          # Máximo de órdenes simultáneas
        self.intervalo_generacion = 25                # Cada cuántos segundos aparece una nueva orden
        self.tiempo_desde_ultima = 0                  # Contador para generar la próxima orden

    def GenerarReceta(self):
        #Agrega una receta aleatoria a las órdenes activas si hay espacio
        if len(self.ordenes) < self.max_ordenes:
            receta = random.choice(self.recetas_posibles)
            # Se crea una nueva instancia para que cada orden tenga su propio temporizador
            nueva = Receta(
                receta.nombre,
                receta.ListaIngredientes,
                receta.PuntosReceta,
                receta.MaxTimeReceta
            )
            self.ordenes.append(nueva)

    def actualizar(self, delta):
        #Avanza el tiempo del nivel y de cada orden activa, si una orden llega a 0 puntos, se elimina y se penaliza al jugador
        self.tiempo_restante -= delta
        self.tiempo_desde_ultima += delta

        # Generar nueva receta cuando corresponda
        if self.tiempo_desde_ultima >= self.intervalo_generacion:
            self.GenerarReceta()
            self.tiempo_desde_ultima = 0

        # Actualizar el tiempo de cada orden activa
        for orden in self.ordenes[:]:  # se copia la lista para poder eliminar mientras iteramos
            orden.actualizar_tiempo(delta)
            if orden.puntos_actuales <= 0:
                # Penalización se descuenta el valor original de la receta
                self.chefs[0].sumar_puntos(-orden.PuntosReceta)
                self.ordenes.remove(orden)

    def entregar(self, ingredientes_entregados):
        #Intenta hacer coincidir los ingredientes entregados con alguna orden activa
        #Coincidencia perfecta (nombre + estado correcto) → puntos completos
        #Coincidencia solo por nombre (estado incorrecto) → se entrega con -10 pts
        #Sin coincidencia → -10 pts y no se entrega nada
        #Devuelve el nombre de la receta entregada, o None si no hubo coincidencia

        # buscar coincidencia perfecta
        perfectas = []
        for orden in self.ordenes:
            if orden.CompararRecetaEstricta(ingredientes_entregados):
                perfectas.append(orden)

        if perfectas:
            # Si hay varias perfectas, se elige la que tiene menos tiempo restante
            orden = min(perfectas, key=lambda o: o.MaxTimeReceta - o.tiempo_transcurrido)
            self.chefs[0].sumar_puntos(orden.puntos_actuales)
            self.ordenes.remove(orden)
            return orden.nombre

        # coincidencia solo por nombre (ingredientes mal preparados)
        por_nombre = []
        for orden in self.ordenes:
            if orden.CompararReceta(ingredientes_entregados):
                por_nombre.append(orden)

        if por_nombre:
            orden = min(por_nombre, key=lambda o: o.MaxTimeReceta - o.tiempo_transcurrido)
            self.chefs[0].sumar_puntos(-10)  # Penalización por mal preparado
            self.ordenes.remove(orden)
            return f"{orden.nombre} (mal preparada, -10pts)"

        # No coincide nada 
        self.chefs[0].sumar_puntos(-10)
        return None

    def juego_terminado(self):
        #Retorna True cuando el tiempo del nivel se agotó
        return self.tiempo_restante <= 0


# Recetas del nivel 1 - Ensaladas simples
recetas_nivel1 = [
    Receta("Ensalada de Frutas", [
        {"nombre": "Banano",  "estado": "preparado"},
        {"nombre": "Fresa",   "estado": "preparado"},
        {"nombre": "Mango",   "estado": "preparado"},
    ], PuntosReceta=30, MaxTimeReceta=60),

    Receta("Ensalada de Pollo", [
        {"nombre": "Pollo",   "estado": "preparado"},
        {"nombre": "Lechuga", "estado": "preparado"},
    ], PuntosReceta=40, MaxTimeReceta=90),
]

# Recetas del nivel 2 – Perros calientes
recetas_nivel2 = [
    Receta("Perro Caliente", [
        {"nombre": "Pan",      "estado": "listo"},
        {"nombre": "Salchicha","estado": "preparado"},
    ], PuntosReceta=30, MaxTimeReceta=60),

    Receta("Perro con Repollo", [
        {"nombre": "Pan",      "estado": "listo"},
        {"nombre": "Salchicha","estado": "preparado"},
        {"nombre": "Repollo",  "estado": "preparado"},
    ], PuntosReceta=40, MaxTimeReceta=75),

    Receta("Perro con Papas", [
        {"nombre": "Pan",      "estado": "listo"},
        {"nombre": "Salchicha","estado": "preparado"},
        {"nombre": "Papas",    "estado": "preparado"},
    ], PuntosReceta=40, MaxTimeReceta=75),

    Receta("Perro Completo", [
        {"nombre": "Pan",      "estado": "listo"},
        {"nombre": "Salchicha","estado": "preparado"},
        {"nombre": "Repollo",  "estado": "preparado"},
        {"nombre": "Papas",    "estado": "preparado"},
    ], PuntosReceta=60, MaxTimeReceta=90),
]

# Recetas del nivel 3 – Empanadas y salchipapas
recetas_nivel3 = [
    Receta("Empanada de Pollo", [
        {"nombre": "Empanada", "estado": "listo"},
        {"nombre": "Pollo",    "estado": "preparado"},
    ], PuntosReceta=40, MaxTimeReceta=90),

    Receta("Empanada Arreglada", [
        {"nombre": "Empanada", "estado": "listo"},
        {"nombre": "Pollo",    "estado": "preparado"},
        {"nombre": "Repollo",  "estado": "preparado"},
    ], PuntosReceta=50, MaxTimeReceta=100),

    Receta("Empanada de Queso", [
        {"nombre": "Empanada", "estado": "listo"},
        {"nombre": "Queso",    "estado": "listo"},
    ], PuntosReceta=30, MaxTimeReceta=60),

    Receta("Salchipapas", [
        {"nombre": "Salchicha","estado": "preparado"},
        {"nombre": "Papas",    "estado": "preparado"},
    ], PuntosReceta=35, MaxTimeReceta=70),
]