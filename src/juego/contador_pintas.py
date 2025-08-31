class ContadorPintas:

    def __init__(self):
        pass

    def contar_apariciones(self, valores: list[int], num_pinta: int, ases_comodines: bool = True) -> int:
        total_apariciones = 0

        for valor in valores:
            if valor == num_pinta or (valor == 1 and ases_comodines):
                total_apariciones += 1

        return total_apariciones
