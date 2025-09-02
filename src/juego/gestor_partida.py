from src.juego.cacho import Cacho
from src.juego.arbitro_ronda import ArbitroRonda
from src.servicios.generador_aleatorio import GeneradorAleatorio
from src.juego.validador_apuesta import ValidadorApuesta

class GestorPartida:
    def __init__(self, num_jugadores: int):
        self.lista_cachos = [Cacho() for _ in range(num_jugadores)]
        self.arbitro_ronda = ArbitroRonda()
        self.validador_apuesta = ValidadorApuesta()
        self.cacho_actual = None
        self.apuesta_actual = (0, 0)
        self.direccion = None
        self.ultimo_apostador = None
        self.jugador_idx = None
        self.ronda_especial = False
        self.tipo_ronda_especial = None 
        self.pinta_fija = None 
        self.cacho_con_un_dado = None  
        self.ya_uso_ronda_especial = set()

    def determinar_cacho_inicial(self) -> Cacho:
        cachos_participantes = self.lista_cachos.copy()

        while True:
            valores = [(cacho, GeneradorAleatorio.generar_valor_aleatorio()) for cacho in cachos_participantes]
            max_valor = max(valores, key=lambda x: x[1])[1]
            ganadores = [cacho for cacho, valor in valores if valor == max_valor]

            if len(ganadores) == 1:
                self.cacho_actual = ganadores[0]
                return ganadores[0]
            
            cachos_participantes = ganadores

    def establecer_direccion(self, direccion: str) -> None:
        self.direccion = direccion

    def obtener_siguiente_cacho(self) -> Cacho:
        if self.direccion is None:
            self.direccion = "horario"
            
        indice_actual = self.lista_cachos.index(self.cacho_actual)
        num_cachos = len(self.lista_cachos)
        
        for _ in range(num_cachos):
            if self.direccion == "horario":
                indice_actual = (indice_actual + 1) % num_cachos
            else:
                indice_actual = (indice_actual - 1) % num_cachos

            siguiente_cacho = self.lista_cachos[indice_actual]
            if siguiente_cacho.get_cantidad_dados() > 0:
                return siguiente_cacho
        return None

    def verificar_cachos_con_un_dado(self) -> Cacho:
        for cacho in self.lista_cachos:
            if cacho.get_cantidad_dados() == 1:
                return cacho
        return None

    def partida_terminada(self) -> bool:
        cachos_con_dados = [c for c in self.lista_cachos if c.get_cantidad_dados() > 0]
        return len(cachos_con_dados) <= 1

    def obtener_ganador(self) -> Cacho:
        cachos_con_dados = [c for c in self.lista_cachos if c.get_cantidad_dados() > 0]
        return cachos_con_dados[0] if cachos_con_dados else None

    def manejar_apuesta(self, nueva_apuesta: tuple = None) -> bool:
        if nueva_apuesta is None:
            raise ValueError("Se debe proporcionar una nueva apuesta")
        
        if self.ronda_especial:
            return self._manejar_apuesta_ronda_especial(nueva_apuesta)
        
        if self.validador_apuesta.validar_nueva_apuesta(self.apuesta_actual, nueva_apuesta):
            self.apuesta_actual = nueva_apuesta
            self.ultimo_apostador = self.cacho_actual
            return True
        else:
            return False

    def _manejar_apuesta_ronda_especial(self, nueva_apuesta: tuple) -> bool:
        cantidad, pinta = nueva_apuesta
        
        if pinta not in range(1, 7) or cantidad <= 0:
            return False
        
        if self.apuesta_actual == (0, 0):
            if pinta != self.pinta_fija:
                return False
            self.apuesta_actual = nueva_apuesta
            self.ultimo_apostador = self.cacho_actual
            return True
        
        if pinta != self.apuesta_actual[1]:
            if not self.puede_cambiar_pinta_en_ronda_especial(self.cacho_actual):
                return False
            if cantidad <= self.apuesta_actual[0]:
                return False
        else:
            if cantidad <= self.apuesta_actual[0]:
                return False
        
        self.apuesta_actual = nueva_apuesta
        self.ultimo_apostador = self.cacho_actual
        return True

    def manejar_duda(self) -> Cacho:
        perdedor = self.arbitro_ronda.manejar_duda(
            self.lista_cachos,
            self.apuesta_actual,
            self.ultimo_apostador,
            self.cacho_actual,
            self.ronda_especial  
        )
        
        if self.ronda_especial:
            self.finalizar_ronda_especial()
            
        return perdedor

    def manejar_calzar(self) -> bool:
        if not self.arbitro_ronda.puede_calzar(self.lista_cachos, self.cacho_actual):
            return False
        
        resultado = self.arbitro_ronda.manejar_calzar(
            self.lista_cachos,
            self.apuesta_actual,
            self.ultimo_apostador,
            self.cacho_actual,
            self.ronda_especial  
        )
        
        if self.ronda_especial:
            self.finalizar_ronda_especial()
            
        return resultado

    def cambiar_cacho_actual(self, nuevo_cacho: Cacho) -> None:
        self.cacho_actual = nuevo_cacho
        self.jugador_idx = self.lista_cachos.index(nuevo_cacho)

    def puede_calzar(self, cacho: Cacho = None) -> bool:

        cacho_a_verificar = cacho if cacho is not None else self.cacho_actual
        if cacho_a_verificar is None:
            return False
        return self.arbitro_ronda.puede_calzar(self.lista_cachos, cacho_a_verificar)

    def puede_obligar_ronda_especial(self, cacho: Cacho) -> bool:

        return (cacho.get_cantidad_dados() == 1 and 
                cacho not in self.ya_uso_ronda_especial)

    def iniciar_ronda_especial(self, cacho: Cacho, tipo: str, pinta_fija: int) -> bool:

        if not self.puede_obligar_ronda_especial(cacho):
            return False
        
        if tipo not in ["abierta", "cerrada"]:
            return False
            
        if pinta_fija not in range(1, 7):
            return False
        
        self.ronda_especial = True
        self.tipo_ronda_especial = tipo
        self.pinta_fija = pinta_fija
        self.cacho_con_un_dado = cacho
        self.cacho_actual = cacho
        self.ya_uso_ronda_especial.add(cacho)
        
        self.apuesta_actual = (0, 0)
        
        return True

    def finalizar_ronda_especial(self) -> None:
        self.ronda_especial = False
        self.tipo_ronda_especial = None
        self.pinta_fija = None
        self.cacho_con_un_dado = None

    def es_ronda_especial(self) -> bool:
        return self.ronda_especial

    def obtener_tipo_ronda_especial(self) -> str:
        return self.tipo_ronda_especial

    def obtener_pinta_fija(self) -> int:
        return self.pinta_fija

    def puede_cambiar_pinta_en_ronda_especial(self, cacho: Cacho) -> bool:

        return (self.ronda_especial and 
                cacho.get_cantidad_dados() == 1 and 
                cacho != self.cacho_con_un_dado)

    def verificar_cachos_disponibles_para_obligar(self) -> list[Cacho]:

        return [cacho for cacho in self.lista_cachos 
                if self.puede_obligar_ronda_especial(cacho)]

    def verificar_oportunidad_ronda_especial(self) -> Cacho:

        cachos_disponibles = self.verificar_cachos_disponibles_para_obligar()
        return cachos_disponibles[0] if cachos_disponibles else None

    def resetear_ronda_especial_usada(self, cacho: Cacho) -> None:

        if cacho in self.ya_uso_ronda_especial:
            self.ya_uso_ronda_especial.remove(cacho)


## faltan funcionalidades de las ronda especiales 