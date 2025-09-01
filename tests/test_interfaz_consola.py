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
    def test_pedir_accion_devuelve_accion(self, mock_input):
        """
        se verifica que al pedir accion a jugador se devuelve la
        accion esperada
        """ 
        interfaz = InterfazConsola()
        accion = interfaz.pedir_accion(0)
        assert accion == "a"

    # NOTE: agregar otros tests para las otras acciones posibles?
    
    @patch("builtins.input", side_effect=["a"])
    def test_pedir_tipo_ronda_especial_abierto(self, mock_input):
        """
        se verifica que al pedir tipo de ronda especial abierto,
        se devuelve string: "abierto"
        """
        interfaz = InterfazConsola()
        eleccion = interfaz.pedir_tipo_ronda_especial(0)
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
    
    @patch("builtins.input", side_effect=["4", "5"])
    def test_pedir_apuesta_devuelve_tupla(self, mock_input):
        """
        se veriifica que al pedir apuesta se devuelve una tupla
        con la cantidad y valor de la apuesta := (cantidad, valor)
        """
        interfaz = InterfazConsola()
        apuesta = interfaz.pedir_apuesta(0, (0, 0))
        assert apuesta == (4, 5)

    def test_imprimir_estado_sin_apuesta(self, capsys):
        """
        verificar que al imprimir el estado sin apuesta se muestre "Ninguna" como apuesta
        """
        interfaz = InterfazConsola()
        cacho = Cacho()
        interfaz.imprimir_estado([cacho], cacho, (0, 0), "normal", 1)
        salida = capsys.readouterr()
        assert "Apuesta: Ninguna" in salida.out
        assert "Jugador 1:" in salida.out

    def test_limpiar_terminal_verificar_ejecucion(self):
        """
        verificar que limpiar_terminal realmente ejecute el comando
        """
        interfaz = InterfazConsola()
        with patch("src.servicios.interfaz_consola.os.system") as mock_system:
            interfaz.limpiar_terminal()
            assert mock_system.called

    @patch("builtins.input", side_effect=["invalid", "cerrado"])
    def test_ronda_especial_entrada_invalida_cerrado(self, mock_input):
        """
        verificar manejo de input invalido y luego "cerrado" en regla especial
        """
        interfaz = InterfazConsola()
        eleccion = interfaz.pedir_tipo_ronda_especial(0)
        assert eleccion == "cerrado"

    @patch("builtins.input", side_effect=["invalid", "a"])
    def test_pedir_direccion_de_turnos_entrada_invalida_luego_antihorario(self, mock_input):
        """
        verificar que al pedir direccion de turnos con input invalido
        y "antihorario" se maneje correctamente
        """
        interfaz = InterfazConsola()
        eleccion = interfaz.pedir_direccion_de_turnos(0)
        assert eleccion == "antihorario"