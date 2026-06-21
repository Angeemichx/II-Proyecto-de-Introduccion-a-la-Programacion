import random

# ======================
# INGREDIENTES
# ======================

class Ingrediente:
    def __init__(self, nombre, estado="crudo"):
        self.nombre = nombre
        self.estado = estado  # si está crudo, preparado, quemado

    def __str__(self):
        return f"{self.nombre} ({self.estado})"


class VegetalesYFrutas(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre, estado="crudo")
        self.cortado = False

    def cortar(self):
        self.cortado = True
        self.estado = "preparado"


class PanesYBases(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre, estado="listo")  # alimentos que no necesitan preparación


class Proteina(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre, estado="crudo")
        self.cocinada = False
        self.tiempo_coccion = 0       # segundos que lleva en la cocina
        self.tiempo_minimo = 5        # segundos mínimos para estar cocinado
        self.tiempo_maximo = 10       # a más de 10 segundos se quemará

    def actualizar_coccion(self, delta):
        if self.estado == "quemado":
            return
        self.tiempo_coccion += delta
        if self.tiempo_coccion >= self.tiempo_maximo:
            self.estado = "quemado"
            self.cocinada = False
        elif self.tiempo_coccion >= self.tiempo_minimo:
            self.estado = "preparado"
            self.cocinada = True


class Papas(Ingrediente):
    def __init__(self):
        super().__init__("Papas", estado="crudo")
        self.frito = False
        self.tiempo_fritura = 0
        self.tiempo_minimo = 4

    def actualizar_fritura(self, delta):
        if self.frito:
            return
        self.tiempo_fritura += delta
        if self.tiempo_fritura >= self.tiempo_minimo:
            self.frito = True
            self.estado = "preparado"


# ======================
# ESTACION
# ======================

class Estacion:
    def __init__(self, nombre, ingredientes_aceptados, tipo):
        self.nombre = nombre
        self.ingredientes_aceptados = ingredientes_aceptados  # lista de nombres de los ingredientes
        self.tipo = tipo  # "dispensador", "cocina", "tabla", "freidora", "entrega"
        self.ingrediente_en_proceso = None

    def aceptar_ingrediente(self, ingrediente):
        if ingrediente.nombre in self.ingredientes_aceptados:
            self.ingrediente_en_proceso = ingrediente
            return True
        return False

    def __str__(self):
        return self.nombre


# ======================
# CHEF
# ======================

class Chef:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntos = 0
        self.ingrediente = None  #cada chef solo carga 1 ingrediente a la vez

    def recoger(self, ingrediente):
        if self.ingrediente is None:
            self.ingrediente = ingrediente
            return True
        return False

    def soltar(self):
        ing = self.ingrediente
        self.ingrediente = None
        return ing

    def sumar_puntos(self, puntos):
        self.puntos = max(0, self.puntos + puntos)

    def __str__(self):
        return f"{self.nombre} - Puntos: {self.puntos}"


# ======================
# RECETA
# ======================

class Receta:
    def __init__(self, nombre, ListaIngredientes, PuntosReceta, MaxTimeReceta):
        self.nombre = nombre
        self.ListaIngredientes = ListaIngredientes
        #se definen las recetas como diccionario {nombre: {tipo_clase, estado_requerido}}
        self.PuntosReceta = PuntosReceta
        self.MaxTimeReceta = MaxTimeReceta
        self.tiempo_transcurrido = 0
        self.puntos_actuales = PuntosReceta

    def actualizar_tiempo(self, delta):
        self.tiempo_transcurrido += delta
        if self.tiempo_transcurrido >= self.MaxTimeReceta:
            self.puntos_actuales = max(0, self.puntos_actuales // 2)
            self.tiempo_transcurrido = 0  # reinicia el ciclo 

    def CompararReceta(self, ingredientes_entregados):
        #Verifica si los ingredientes entregados son los correctos y completan la receta
        for req in self.ListaIngredientes:
            nombre_req = req["nombre"]
            estado_req = req["estado"]
            encontrado = False
            for ing in ingredientes_entregados:
                if ing.nombre == nombre_req and ing.estado == estado_req:
                    encontrado = True
                    break
            if not encontrado:
                return False
        return True

    def __str__(self):
        return f"{self.nombre} - {self.puntos_actuales} pts"


# ======================
# COCINA
# ======================

class Cocina:
    def __init__(self, tiempo, chefs, recetas_posibles):
        self.tiempo = tiempo          # tiempo total del nivel en segundos
        self.tiempo_restante = tiempo
        self.chefs = chefs            # lista de chefs
        self.ordenes = []             #recetas activas en pantalla
        self.recetas_posibles = recetas_posibles  #recetas del nivel
        self.max_ordenes = 3
        self.intervalo_generacion = 25  #segundos entre nuevas recetas
        self.tiempo_desde_ultima = 0

    def GenerarReceta(self):
        #Agrega una receta aleatoria a las órdenes activas
        if len(self.ordenes) < self.max_ordenes:
            receta = random.choice(self.recetas_posibles)
            # No reutilizar el mismo objeto
            nueva = Receta(
                receta.nombre,
                receta.ListaIngredientes,
                receta.PuntosReceta,
                receta.MaxTimeReceta
            )
            self.ordenes.append(nueva)

    def actualizar(self, delta):
        #Llamar cada frame con delta en segundos
        self.tiempo_restante -= delta
        self.tiempo_desde_ultima += delta

        if self.tiempo_desde_ultima >= self.intervalo_generacion:
            self.GenerarReceta()
            self.tiempo_desde_ultima = 0

        # Actualizar tiempos de cada orden
        for orden in self.ordenes[:]:
            orden.actualizar_tiempo(delta)
            if orden.puntos_actuales <= 0:
                # Penalizar al chef activo
                self.chefs[0].sumar_puntos(-orden.PuntosReceta)
                self.ordenes.remove(orden)

    def entregar(self, ingredientes_entregados):
        #Verifica si los ingredientes completan alguna orden activa
        for orden in self.ordenes:
            if orden.CompararReceta(ingredientes_entregados):
                self.chefs[0].sumar_puntos(orden.puntos_actuales)
                self.ordenes.remove(orden)
                return orden.nombre
        return None

    def juego_terminado(self):
        return self.tiempo_restante <= 0


# ===========
# RECETAS
# ===========

# ---- NIVEL 1: Ensaladas ----
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

# ---- NIVEL 2: Perros Calientes ----
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

# ---- NIVEL 3: Empanadas ----
recetas_nivel3 = [
    Receta("Empanada de Pollo", [
        {"nombre": "Empanada", "estado": "preparado"},
        {"nombre": "Pollo",    "estado": "preparado"},
    ], PuntosReceta=40, MaxTimeReceta=90),

    Receta("Empanada Arreglada", [
        {"nombre": "Empanada", "estado": "preparado"},
        {"nombre": "Pollo",    "estado": "preparado"},
        {"nombre": "Repollo",  "estado": "preparado"},
    ], PuntosReceta=50, MaxTimeReceta=100),

    Receta("Empanada de Queso", [
        {"nombre": "Empanada", "estado": "preparado"},
        {"nombre": "Queso",    "estado": "listo"},
    ], PuntosReceta=30, MaxTimeReceta=60),

    Receta("Salchipapas", [
        {"nombre": "Salchicha","estado": "preparado"},
        {"nombre": "Papas",    "estado": "preparado"},
    ], PuntosReceta=35, MaxTimeReceta=70),
]