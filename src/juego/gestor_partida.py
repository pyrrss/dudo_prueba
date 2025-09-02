from src.juego.cacho import Cacho
from src.juego.arbitro_ronda import ArbitroRonda
from src.servicios.generador_aleatorio import GeneradorAleatorio
from src.juego.validador_apuesta import ValidadorApuesta

import time

class GestorPartida:
    def __init__(self, num_jugadores: int):
        self.lista_cachos = [Cacho() for _ in range(num_jugadores)]
        self.arbitro_ronda = ArbitroRonda()
        self.cacho_actual = None
        self.apuesta_actual = (0, 0)
        self.estado_especial = False
        self.estado_especial_pendiente = False
        self.tipo_ronda_especial = None
        self.tipo_ronda_especial_pendiente = None
        self.direccion = None
        self.validador_apuesta = ValidadorApuesta()
        self.ultimo_apostador = None
        self.jugador_idx = None
        self.iniciador_proxima_ronda = None
        self.cacho_que_obligo = None
        self.cachos_que_usaron_especial = set()

    def determinar_cacho_inicial(self) -> Cacho:
        cachos_participantes = self.lista_cachos.copy()

        while True: # -> hasta que no haya un ganador
            valores = [(cacho, GeneradorAleatorio.generar_valor_aleatorio()) for cacho in cachos_participantes]

            max_valor = max(valores, key=lambda x: x[1])[1]
            ganadores = [cacho for cacho, valor in valores if valor == max_valor]

            # -> si no hay empate
            if len(ganadores) == 1:
                self.cacho_actual = ganadores[0]
                return ganadores[0]

            # -> si hay empate (solo empatados siguen participando)
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

    def iniciar_ronda(self) -> None:
        self.apuesta_actual = (0, 0)
        self.ultimo_apostador = None

        if self.iniciador_proxima_ronda is not None:
            self.cacho_actual = self.iniciador_proxima_ronda
            self.iniciador_proxima_ronda = None

        for cacho in self.lista_cachos:
            cacho.agitar()
            cacho.ocultar_dados() # -> visibilidad se ajusta luego en cada turno

        # -> activar ronda especial si estaba pendiente
        if self.estado_especial_pendiente:
            self.estado_especial = True
            self.tipo_ronda_especial = self.tipo_ronda_especial_pendiente
            self.estado_especial_pendiente = False
            self.tipo_ronda_especial_pendiente = None
        else:
            self.estado_especial = False
            self.tipo_ronda_especial = None
            self.cacho_que_obligo = None

    def partida_terminada(self) -> bool:
        cachos_con_dados = [c for c in self.lista_cachos if c.get_cantidad_dados() > 0]
        return len(cachos_con_dados) <= 1

    def obtener_ganador(self) -> Cacho:
        cachos_con_dados = [c for c in self.lista_cachos if c.get_cantidad_dados() > 0]
        return cachos_con_dados[0] if cachos_con_dados else None

    def verificar_ronda_especial(self, cacho: Cacho) -> None:
        if cacho.get_cantidad_dados() == 1 and cacho not in self.cachos_que_usaron_especial:
            self.cacho_que_obligo = cacho
            self.estado_especial_pendiente = True
            self.cachos_que_usaron_especial.add(cacho)
            self.actualizar_visibilidad_dados()

    def actualizar_visibilidad_dados(self) -> None:
        
        for cacho in self.lista_cachos:
            cacho.ocultar_dados()

        if self.estado_especial and self.tipo_ronda_especial == "abierto":
            # -> abierto: el jugador actual no ve sus dados, pero sí los de los demás
            for cacho in self.lista_cachos:
                if cacho is not self.cacho_actual:
                    cacho.mostrar_dados()

        elif self.estado_especial and self.tipo_ronda_especial == "cerrado":
            # -> cerrado: sólo el obligador ve sus dados, los demás no ven nada, tampoco en su propio turno
            if self.cacho_que_obligo is not None and self.cacho_que_obligo is self.cacho_actual:
                self.cacho_que_obligo.mostrar_dados()

        else:
            # -> ronda normal: cada jugador ve sólo sus propios dados en su turno
            if self.cacho_actual is not None:
                self.cacho_actual.mostrar_dados()
