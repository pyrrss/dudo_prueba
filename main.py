from src.juego.gestor_partida import GestorPartida

if __name__ == "__main__":
    num_jugadores = int(input("Número de jugadores: "))
    gestor_partida = GestorPartida(num_jugadores)
    gestor_partida.jugar()

