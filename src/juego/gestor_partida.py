from src.juego.cacho import Cacho
from src.juego.arbitro_ronda import ArbitroRonda
from src.servicios.interfaz_consola import InterfazConsola
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
        self.interfaz = InterfazConsola()
        self.jugador_idx = None
        self.iniciador_proxima_ronda = None
        self.cacho_que_obligo = None
        self.cachos_que_usaron_especial = set()

    def _determinar_cacho_inicial(self) -> Cacho:
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

    def _establecer_direccion(self, direccion: str) -> None:
        self.direccion = direccion

    def _obtener_siguiente_cacho(self) -> Cacho:
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

    # NOTE: esto devuelve el primer cacho que tenga un dado
    def _verificar_cachos_con_un_dado(self) -> Cacho:
        for cacho in self.lista_cachos:
            if cacho.get_cantidad_dados() == 1:
                return cacho
        return None

    def _iniciar_ronda(self) -> None:
        self.apuesta_actual = (0, 0)
        self.ultimo_apostador = None

        if self.iniciador_proxima_ronda is not None:
            self.cacho_actual = self.iniciador_proxima_ronda
            self.iniciador_proxima_ronda = None

        for cacho in self.lista_cachos:
            cacho.agitar()
            cacho.ocultar_dados() # -> visibilidad se ajusta luego en cada turno

        # -> activar ronda especial si estaba pendiente
        if getattr(self, "estado_especial_pendiente", False):
            self.estado_especial = True
            self.tipo_ronda_especial = self.tipo_ronda_especial_pendiente
            self.estado_especial_pendiente = False
        else:
            self.estado_especial = False
            self.tipo_ronda_especial = None
            self.cacho_que_obligo = None

    def _partida_terminada(self) -> bool:
        cachos_con_dados = [c for c in self.lista_cachos if c.get_cantidad_dados() > 0]
        return len(cachos_con_dados) <= 1

    def _obtener_ganador(self) -> Cacho:
        cachos_con_dados = [c for c in self.lista_cachos if c.get_cantidad_dados() > 0]
        return cachos_con_dados[0] if cachos_con_dados else None

    def _verificar_ronda_especial(self, cacho: Cacho) -> None:
        if cacho.get_cantidad_dados() == 1 and cacho not in self.cachos_que_usaron_especial:
            self.cacho_que_obligo = cacho
            self.tipo_ronda_especial_pendiente = self.interfaz.pedir_tipo_ronda_especial(self.lista_cachos.index(cacho))
            self.estado_especial_pendiente = True
            self.cachos_que_usaron_especial.add(cacho)
            self._actualizar_visibilidad_dados()
            print(f"El Jugador {self.lista_cachos.index(cacho) + 1} obliga ronda {self.tipo_ronda_especial_pendiente}")
            input("Presiona ENTER para continuar...")

    def _manejar_apuesta(self):
        while True: # -> hasta que se ingrese apuesta válida
            nueva_apuesta = self.interfaz.pedir_apuesta(self.jugador_idx, self.apuesta_actual)
            if self.validador_apuesta.validar_nueva_apuesta(self.apuesta_actual, nueva_apuesta):
                self.apuesta_actual = nueva_apuesta
                self.ultimo_apostador = self.cacho_actual # -> se guarda último apostador
                break
            else:
                # NOTE: o se repite hasta obtener apuesta valida?
                print("Apuesta inválida, debes o subir la cantidad de dados o el valor de la pinta")
                print("También puedes transformar tu apuesta a ases")

    def _manejar_duda(self):
        # NOTE: al hacer copy, los cachos de la copia siguen siendo los mismos que los de la lista original
        lista_cachos_previa = self.lista_cachos.copy()
        
        self.interfaz.imprimir_revelacion(lista_cachos_previa, self.apuesta_actual)

        perdedor = self.arbitro_ronda.manejar_duda(
            self.lista_cachos,
            self.apuesta_actual,
            self.ultimo_apostador,
            self.cacho_actual,
            self.estado_especial
        )
        print(f"El Jugador {self.lista_cachos.index(perdedor) + 1} pierde un dado")

        self.iniciador_proxima_ronda = perdedor

        input("Presiona ENTER para continuar...")
        
        self._verificar_ronda_especial(perdedor)

    def _manejar_calzar(self):
        lista_cachos_previa = self.lista_cachos.copy()
        
        self.interfaz.imprimir_revelacion(lista_cachos_previa, self.apuesta_actual)

        gana_dado = self.arbitro_ronda.manejar_calzar(
                self.lista_cachos,
                self.apuesta_actual,
                self.ultimo_apostador,
                self.cacho_actual,
                self.estado_especial
        )
        if gana_dado:
            print(f"El jugador {self.jugador_idx + 1} gana un dado")
        else:
            print(f"El jugador {self.jugador_idx + 1} pierde un dado")

        input("Presiona ENTER para continuar...")

        self.iniciador_proxima_ronda = self.cacho_actual

        self._verificar_ronda_especial(self.cacho_actual)

    def _actualizar_visibilidad_dados(self) -> None:
        
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

    def jugar(self) -> None:
        # TODO: printear elementos de 'interfaz' a la terminal
        # antes de empezar partida
        self.interfaz.limpiar_terminal()
        self.interfaz.imprimir_banner()

        print("Determinando cacho inicial...")
        self.cacho_actual = self._determinar_cacho_inicial()

        # -> elección de dirección de turnos
        self.direccion = self.interfaz.pedir_direccion_de_turnos(self.lista_cachos.index(self.cacho_actual))

        # -> 'game loop'
        # NOTE: ESTO FUNCIONA PERO ESTÁ FEO (game loop -> round loop -> player loop (hasta que haga accion valida))
        num_ronda = 0
        while not self._partida_terminada():
            num_ronda += 1
            self._iniciar_ronda()
            self.interfaz.limpiar_terminal()

            # -> ronda en curso
            ronda_terminada = False
            while not ronda_terminada:
                while self.cacho_actual.get_cantidad_dados() == 0:
                    self.cacho_actual = self._obtener_siguiente_cacho()
            
                self.interfaz.limpiar_terminal()
                self.jugador_idx = self.lista_cachos.index(self.cacho_actual)

                self._actualizar_visibilidad_dados()
                self.interfaz.imprimir_estado(self.lista_cachos, self.cacho_actual, self.apuesta_actual, self.tipo_ronda_especial, num_ronda)

                # -> hasta que jugador actual haga acción válida
                while True:
                    accion = self.interfaz.pedir_accion(self.jugador_idx)
                    if accion == "a":
                        self._manejar_apuesta()
                        time.sleep(1)
                        self.cacho_actual = self._obtener_siguiente_cacho()
                        break
                    elif accion == "d":
                        if self.apuesta_actual == (0, 0):
                            print("No puedes dudar sin apuesta")
                            continue
                        self._manejar_duda()
                        ronda_terminada = True
                        time.sleep(1)
                        break
                    elif accion == "c":
                        if self.apuesta_actual == (0, 0):
                            print("No puedes calzar sin apuesta")
                            continue

                        if not self.arbitro_ronda.puede_calzar(self.lista_cachos, self.cacho_actual):
                            print("No se cumplen las condiciones para calzar")
                            continue

                        self._manejar_calzar()
                        ronda_terminada = True
                        time.sleep(1)
                        break
                    elif accion == "p":
                        # TODO: revisar si se necesitan reglas especiales para poder pasar
                        print(f"Jugador {self.jugador_idx + 1} pasa")
                        time.sleep(1)
                        self.cacho_actual = self._obtener_siguiente_cacho()
                        break
                    else:
                        print("Acción inválida")
                        time.sleep(1)
                        continue

        # -> terminar partida
        ganador = self._obtener_ganador()
        print(f"El ganador es el cacho {self.lista_cachos.index(ganador) + 1}")
        self.interfaz.imprimir_cierre()
