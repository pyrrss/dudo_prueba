import builtins
from unittest.mock import patch
import pytest
from src.servicios.interfaz_consola import InterfazConsola
from src.juego.cacho import Cacho
from src.juego.dado import Dado

from src.servicios.interfaz_consola import InterfazConsola


class TestInterfazConsola:
    
    # NOTE: este servicio usa principalmente prints e inputs
    # asi que se testea si salidas son las esperadas y se mockean
    # los inputs

    def test_imprimir_banner_correctamente(self, capsys):
        """
        se verifica que el banner se imprima correctamente
        """
        interfaz = InterfazConsola()
        interfaz.imprimir_banner()
        salida = capsys.readouterr()

        assert "DDDDDDDDDDDDD" in salida.out

    def test_imprimir_cierre_correctamente(self, capsys):
        """
        se verifica que el cierre se imprima correctamente
        """
        interfaz = InterfazConsola()
        interfaz.imprimir_cierre()
        salida = capsys.readouterr()
        
        assert "A:::::AAAAAAAAA:::::A" in salida.out
    
    @patch("builtins.input", side_effect=["h"])
    def test_pedir_direccion_de_turnos_horario(self, mock_input):
        """
        se verifica que al pedir dirrecion de turnos horario
        se devuelva el string esperado: "horario"
        """
        interfaz = InterfazConsola()
        eleccion = interfaz.pedir_direccion_de_turnos(0)
        assert eleccion == "horario"

    @patch("builtins.input", side_effect=["a"])
    def test_pedir_direccion_de_turnos_antihorario(self, mock_input):
        """
        se verifica que al pedir dirrecion de turnos antihorario
        se devuelva el string esperado: "antihorario"
        """
        interfaz = InterfazConsola()
        eleccion = interfaz.pedir_direccion_de_turnos(0)
        assert eleccion == "antihorario"
 
    @patch("builtins.input", side_effect=["x", "h"])
    def test_pedir_direccion_de_turnos_invalido_y_luego_valido(self, mock_input, capsys):
        """
        se verifica que al pedir direccion de turnos y recibir un input
        invalido, se muestra un mensaje de error
        """
        interfaz = InterfazConsola()
        eleccion = interfaz.pedir_direccion_de_turnos(0)
        salida = capsys.readouterr() 
        assert "Opción inválida" in salida.out
        assert eleccion == "horario"

    def test_imprimir_estado_muestra_valores_correctamente(self, capsys):
        """
        se verifica que al imprimir el estado se muestre una salida
        esperada
        """
        interfaz = InterfazConsola()
        cacho = Cacho()
        interfaz.imprimir_estado([cacho], cacho, (2, 3), "abierto", 1)
        salida = capsys.readouterr()
        assert "RONDA 1" in salida.out
        assert "TIPO DE RONDA: abierto" in salida.out
        assert "Estado de los jugadores:" in salida.out
        assert "Apuesta: 2 trenes" in salida.out

    def test_imprimir_estado_sin_apuesta(self, capsys):
        """
        se verifica que al imprimir estado sin apuesta se muestra
        "Apuesta: Ninguna"
        """
        interfaz = InterfazConsola()
        cacho = Cacho()
        interfaz.imprimir_estado([cacho], cacho, (0, 0), "cerrado", 1)
        salida = capsys.readouterr()
        assert "Apuesta: Ninguna" in salida.out
    
    def test_imprimir_revelacion_muestra_valores_correctamente(self, capsys):
        """
        se verifica que al revelar los valores de los dados al terminar una ronda
        estos se muestran de forma esperada
        """
        interfaz = InterfazConsola()
        cacho = Cacho()
        cacho.set_valores_dados([1, 2, 3, 4, 5])
        interfaz.imprimir_revelacion([cacho], (2, 3))
        salida = capsys.readouterr()
        assert "La apuesta especulada era: (2, 3)" in salida.out
        assert "Los valores de los dados eran: " in salida.out
        assert "Jugador 1: [1, 2, 3, 4, 5]" in salida.out
    
    @patch("builtins.input", side_effect=["a"])
    def test_pedir_accion_devuelve_accion_apostar(self, mock_input):
        """
        se verifica que al pedir accion a jugador se devuelve la
        accion esperada (apostar)
        """ 
        interfaz = InterfazConsola()
        accion = interfaz.pedir_accion(0)
        assert accion == "a"
    
    @patch("builtins.input", side_effect=["d"])
    def test_pedir_accion_dudar(self, mock_input):
        """
        se verifica que al pedir accion a jugador se devuelve
        la accion esperada (dudar)
        """
        interfaz = InterfazConsola()
        assert interfaz.pedir_accion(0) == "d"

    @patch("builtins.input", side_effect=["c"])
    def test_pedir_accion_devuelve_accion_calzar(self, mock_input):
        """
        se verifica que al pedir accion a jugador se devuelve la
        accion esperada (calzar)
        """ 
        interfaz = InterfazConsola()
        accion = interfaz.pedir_accion(0)
        assert accion == "c"
    
    @patch("builtins.input", side_effect=["p"])
    def test_pedir_accion_devuelve_accion_pasar(self, mock_input):
        """
        se verifica que al pedir accion a jugador se devuelve la
        accion esperada (pasar)
        """ 
        interfaz = InterfazConsola()
        accion = interfaz.pedir_accion(0)
        assert accion == "p"

    @patch("os.system")
    def test_limpiar_terminal(self, mock_system):
        """
        se verifica que al limpiar termianl se llama al metodo
        de os.system
        """
        interfaz = InterfazConsola()
        interfaz.limpiar_terminal()
        mock_system.assert_called_once()

    @patch("builtins.input", side_effect=["a"])
    def test_pedir_tipo_ronda_especial_abierto(self, mock_input):
        """
        se verifica que al pedir tipo de ronda especial abierto,
        se devuelve string: "abierto"
        """
        interfaz = InterfazConsola()
        eleccion = interfaz.pedir_tipo_ronda_especial(0)
        assert eleccion == "abierto"

    @patch("builtins.input", side_effect=["x", "a"])
    def test_pedir_tipo_ronda_especial_invalido_luego_abierto(self, mock_input, capsys):
        """
        se verifica que al pedir tipo de ronda especial y recibir
        entrada invalido, se muestra mensaje de error, luego se pide
        otra entrada y si se ingresa correctamente, se devuelve tipo 
        de ronda esperado (abierto)
        """

        interfaz = InterfazConsola()
        eleccion = interfaz.pedir_tipo_ronda_especial(0)
        salida = capsys.readouterr()
        assert "Opción inválida" in salida.out
        assert eleccion == "abierto"

    @patch("builtins.input", side_effect=["c"])
    def test_pedir_tipo_ronda_especial_cerrado(self, mock_input):
        """
        se verifica que al pedir tipo de ronda especial cerrado,
        se devuelve string: "cerrado"
        """
        interfaz = InterfazConsola()
        eleccion = interfaz.pedir_tipo_ronda_especial(0)
        assert eleccion == "cerrado"

    @patch("builtins.input", side_effect=["x", "c"])
    def test_pedir_tipo_ronda_especial_invalido_luego_cerrado(self, mock_input, capsys):
        """
        se verifica que al pedir tipo de ronda especial y recibir
        entrada invalido, se muestra mensaje de error, luego se pide
        otra entrada y si se ingresa correctamente, se devuelve tipo 
        de ronda esperado (cerrado)
        """
        interfaz = InterfazConsola()
        eleccion = interfaz.pedir_tipo_ronda_especial(0)
        salida = capsys.readouterr()
        assert "Opción inválida" in salida.out
        assert eleccion == "cerrado"
    
    @patch("builtins.input", side_effect=["4", "5"])
    def test_pedir_apuesta_devuelve_tupla(self, mock_input):
        """
        se veriifica que al pedir apuesta se devuelve una tupla
        con la cantidad y valor de la apuesta := (cantidad, valor)
        """
        interfaz = InterfazConsola()
        apuesta = interfaz.pedir_apuesta(0, (2, 3))
        assert apuesta == (4, 5)

    @patch("builtins.input", side_effect=["x", "3", "y", "6"])
    def test_pedir_apuesta_con_valores_invalidos(self, mock_input, capsys):
        interfaz = InterfazConsola()
        apuesta = interfaz.pedir_apuesta(0, (0, 0))
        salida = capsys.readouterr()
        assert "Por favor, ingresa un número válido" in salida.out
        assert apuesta == (3, 6)

