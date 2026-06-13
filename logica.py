class Cocina: 
    tiempo = 0
    chefs = []
    ordenes = []

    def __initi__(self, tiempo, chefs, ordenes):
        self.tiempo = tiempo 
        self.chefs = chefs 
        self.ordenes = ordenes 

    def GenerarReceta(tiempo, chefs, ordenes):
        pass

class Estación:
    nombre = ""
    ingredientes = []
    receta = []

    def __init__(self, nombre, ingredientes, receta):
        self.nombre = nombre 
        self.ingredientes = ingredientes 
        self.receta = receta 

    def GenerarReceta(nombre, ingredientes, receta):
        pass

class Chef:
    nombre = ""
    puntos = 0

    def __init__(self, nombre, puntos):
        self.nombre = nombre
        self.puntos = puntos 
        
class Ingrediente:
    nombre = ""
    estado = ""

    def __init__(self, nombre, estado):
        self.nombre = nombre
        self.estado = estado 

class VegetalesYFrutas(Ingrediente):
    pass

class PanesYBases(Ingrediente):
    pass

class Proteina(Ingrediente):
    cocinada = False 

class Receta:
    ListaIngredientes = []
    PuntosReceta = 0
    MaxTimeReceta = 0 

    def __init__(self, ListaIngredientes, PuntosReceta, MaxTimeReceta):
        self.ListaIngredientes = ListaIngredientes
        self.PuntosReceta = PuntosReceta
        self.MaxTimeReceta = MaxTimeReceta