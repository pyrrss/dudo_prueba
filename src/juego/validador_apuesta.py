import math

class ValidadorApuesta:

    def __init__(self):
        pass

    # TODO: creo que falta considerar pinta fija en ronda especial, elegida por quien obliga
    def validar_nueva_apuesta(self, apuesta_actual: tuple[int, int], apuesta_nueva: tuple[int, int]) -> bool:

        # ---------- revisión de dominio --------
        if not apuesta_nueva[1] in range(1, 7) or not apuesta_nueva[0] > 0:
            return False

        # ---------- revisión para no poder partir con ases --------
        if apuesta_actual == (0, 0) and apuesta_nueva[1] == 1: # -> (0, 0) para indicar primer apuesta
            return False

        # ---------- casos basicos ---------

        # -> sin ases involucrados
        if apuesta_nueva[1] != 1 and apuesta_actual[1] != 1:

            if apuesta_nueva[0] > apuesta_actual[0] and apuesta_nueva[1] == apuesta_actual[1]:
                return True

            if apuesta_nueva[1] > apuesta_actual[1] and apuesta_nueva[0] == apuesta_actual[0]:
                return True

            if apuesta_nueva[0] > apuesta_actual[0] and apuesta_nueva[1] > apuesta_actual[1]:
                return True

        # ---------- casos especiales de los ases ---------

        # -> cambio de pinta A ases
        if apuesta_actual[1] != 1 and apuesta_nueva[1] == 1:

            if self._cantidad_valida_a_ases_desde_otra_pinta(apuesta_actual[0]) == apuesta_nueva[0]:
                return True

        # -> cambio DE ases a otra pinta
        if apuesta_actual[1] == 1 and apuesta_nueva[1] != 1:

            if self._cantidad_valida_de_ases_a_otra_pinta(apuesta_actual[0]) == apuesta_nueva[0]:
                return True

        return False

    def _cantidad_valida_a_ases_desde_otra_pinta(self, cantidad_actual: int) -> int:
        if cantidad_actual % 2 == 0:
            return (cantidad_actual // 2) + 1
        return math.ceil(cantidad_actual / 2)

    def _cantidad_valida_de_ases_a_otra_pinta(self, cantidad_actual: int) -> int:
        return (cantidad_actual * 2) + 1


