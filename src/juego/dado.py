from src.servicios.generador_aleatorio import GeneradorAleatorio

class Dado:
    denominaciones = {
        1: "As",
        2: "Tonto",
        3: "Tren",
        4: "Cuadra",
        5: "Quina",
        6: "Sexto"
    }

    def __init__(self):
       self.valor_actual = None

    def lanzar(self):
        self.valor_actual = GeneradorAleatorio.generar_valor_aleatorio()

    def get_nombre_pinta(self, num_pinta):
        return self.denominaciones[num_pinta]
