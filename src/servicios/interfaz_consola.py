import os
from src.juego.cacho import Cacho

class InterfazConsola:

    # NOTE: ESTA CLASE NO SE ESTÁ TESTEANDO, SON PUROS PRINTS 
    # ASI QUE NO ESTOY SEGURO DE SI SE DEBERIA TESTEAR
    # PERO EL PROBLEMA ES QUE SI NO SE TESTEA BAJA EL PORCENTAJE
    # DE COVERAGE DE LOS TESTS
    # O CAPAZ NO AFECTAN AL COVERAGE PORQUE TODAS ESTAS FUNCIONES ESTÁN SIENDO
    # USADAS EN GESTOR_PARTIDA?
    def __init__(self):
        pass

    def imprimir_banner(self) -> None:
        banner = """
            DDDDDDDDDDDDD       UUUUUUUU     UUUUUUUUDDDDDDDDDDDDD             OOOOOOOOO     
            D::::::::::::DDD    U::::::U     U::::::UD::::::::::::DDD        OO:::::::::OO   
            D:::::::::::::::DD  U::::::U     U::::::UD:::::::::::::::DD    OO:::::::::::::OO 
            DDD:::::DDDDD:::::D UU:::::U     U:::::UUDDD:::::DDDDD:::::D  O:::::::OOO:::::::O
              D:::::D    D:::::D U:::::U     U:::::U   D:::::D    D:::::D O::::::O   O::::::O
              D:::::D     D:::::DU:::::D     D:::::U   D:::::D     D:::::DO:::::O     O:::::O
              D:::::D     D:::::DU:::::D     D:::::U   D:::::D     D:::::DO:::::O     O:::::O
              D:::::D     D:::::DU:::::D     D:::::U   D:::::D     D:::::DO:::::O     O:::::O
              D:::::D     D:::::DU:::::D     D:::::U   D:::::D     D:::::DO:::::O     O:::::O
              D:::::D     D:::::DU:::::D     D:::::U   D:::::D     D:::::DO:::::O     O:::::O
              D:::::D     D:::::DU:::::D     D:::::U   D:::::D     D:::::DO:::::O     O:::::O
              D:::::D    D:::::D U::::::U   U::::::U   D:::::D    D:::::D O::::::O   O::::::O
            DDD:::::DDDDD:::::D  U:::::::UUU:::::::U DDD:::::DDDDD:::::D  O:::::::OOO:::::::O
            D:::::::::::::::DD    UU:::::::::::::UU  D:::::::::::::::DD    OO:::::::::::::OO 
            D::::::::::::DDD        UU:::::::::UU    D::::::::::::DDD        OO:::::::::OO   
            DDDDDDDDDDDDD             UUUUUUUUU      DDDDDDDDDDDDD             OOOOOOOOO     
        """
        print(banner)

    def imprimir_cierre(self) -> None:
        cierre = """
                        AAA               DDDDDDDDDDDDD      IIIIIIIIII     OOOOOOOOO        SSSSSSSSSSSSSSS 
                       A:::A              D::::::::::::DDD   I::::::::I   OO:::::::::OO    SS:::::::::::::::S
                      A:::::A             D:::::::::::::::DD I::::::::I OO:::::::::::::OO S:::::SSSSSS::::::S
                     A:::::::A            DDD:::::DDDDD:::::DII::::::IIO:::::::OOO:::::::OS:::::S     SSSSSSS
                    A:::::::::A             D:::::D    D:::::D I::::I  O::::::O   O::::::OS:::::S            
                   A:::::A:::::A            D:::::D     D:::::DI::::I  O:::::O     O:::::OS:::::S            
                  A:::::A A:::::A           D:::::D     D:::::DI::::I  O:::::O     O:::::O S::::SSSS         
                 A:::::A   A:::::A          D:::::D     D:::::DI::::I  O:::::O     O:::::O  SS::::::SSSSS    
                A:::::A     A:::::A         D:::::D     D:::::DI::::I  O:::::O     O:::::O    SSS::::::::SS  
               A:::::AAAAAAAAA:::::A        D:::::D     D:::::DI::::I  O:::::O     O:::::O       SSSSSS::::S 
              A:::::::::::::::::::::A       D:::::D     D:::::DI::::I  O:::::O     O:::::O            S:::::S
             A:::::AAAAAAAAAAAAA:::::A      D:::::D    D:::::D I::::I  O::::::O   O::::::O            S:::::S
            A:::::A             A:::::A   DDD:::::DDDDD:::::DII::::::IIO:::::::OOO:::::::OSSSSSSS     S:::::S
           A:::::A               A:::::A  D:::::::::::::::DD I::::::::I OO:::::::::::::OO S::::::SSSSSS:::::S
          A:::::A                 A:::::A D::::::::::::DDD   I::::::::I   OO:::::::::OO   S:::::::::::::::SS 
         AAAAAAA                   AAAAAAADDDDDDDDDDDDD      IIIIIIIIII     OOOOOOOOO      SSSSSSSSSSSSSSS   
        """
        print(cierre)

    def pedir_direccion_de_turnos(self, jugador_idx: int) -> str:
        print(f"\nJugador {jugador_idx + 1}, debes elegir dirección de turnos:")
        print("Opciones: [H]orario | [A]ntihorario")
        eleccion = input("¿Qué eliges?: ").strip().lower()

        while eleccion not in ["h", "a"]:
            print("Opción inválida, vuelve a ingresar")
            eleccion = input("¿Qué eliges?: ").strip().lower()

        if eleccion == "h":
            eleccion = "horario"
        elif eleccion == "a":
            eleccion = "antihorario"

        return eleccion

    def imprimir_estado(self, lista_cachos: list[Cacho], jugador_actual: Cacho, apuesta: tuple[int, int], num_ronda: int) -> None:
        print(f"\nRONDA {num_ronda}")
        print("\n Estado de los jugadores:")
        print(f"Apuesta: {apuesta if apuesta != (0, 0) else 'Ninguna'}")

        # NOTE: imprimir valores de dados aca? no se cómo manejar lo de ocultar/mostrar en interfaz
        for cacho in lista_cachos:
            print(f"Jugador {lista_cachos.index(cacho) + 1}: {cacho.get_valores()}")

        print("\n")

    def imprimir_valores(self, lista_cachos: list[Cacho], apuesta: tuple[int, int]) -> None:
        print(f"\nLa apuesta especulada era: {apuesta}")
        print("\nLos valores de los dados eran: ")
        for cacho in lista_cachos:
            print(f"Jugador {lista_cachos.index(cacho) + 1}: {cacho.get_valores()}")

    def pedir_accion(self, jugador_idx: int) -> str:
        print(f"\nTurno del Jugador {jugador_idx + 1}")
        print("Opciones: [A]postar | [D]udar | [C]alzar | [P]asar")

        accion = input("¿Qué eliges?: ").strip().lower()
        return accion

    def limpiar_terminal(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def pedir_tipo_ronda_especial(self, jugador_idx: int) -> str:
        print(f"\nJugador {jugador_idx + 1}, debes elegir de qué forma jugar la siguiente ronda")
        print("Opciones: [A]bierto | [C]errado")

        while True: # -> hasta que haya eleccón válida
            eleccion = input("¿Qué eliges?: ").strip().lower()
            if eleccion in ["a", "abierto"]:
                return "abierto"
            if eleccion in ["c", "cerrado"]:
                return "cerrado"

            print("Opción inválida, vuelve a ingresar")

    def pedir_apuesta(self, jugador_idx: int, apuesta_actual: tuple[int, int]) -> tuple[int, int]:
        print(f"\nJugador {jugador_idx + 1}, elige una nueva apuesta:")
        print(f"Apuesta actual: {apuesta_actual if apuesta_actual != (0, 0) else 'Ninguna'}")

        while True:
            try:
                cantidad = int(input("Cantidad de dados: ").strip())
                break
            except ValueError:
                print("Por favor, ingresa un número válido para la cantidad de dados.")

        while True:
            try:
                valor = int(input("Valor de la pinta: ").strip())
                break
            except ValueError:
                print("Por favor, ingresa un número válido para el valor de la pinta.")

        return (cantidad, valor)





