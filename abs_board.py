"""
Author: Jose L Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Headers for functions in abstract board for simple tic-tac-toe-like games, 2021.
Intended for Grau en Intel-ligencia Artificial, Programacio i Algorismes 1.
I would prefer to do everything in terms of object-oriented programming though.
"""

# Import: 
# color GRAY; PLAYER_COLOR, NO_PLAYER
# board dimension BSIZ
from constants import PLAYER_COLOR, BSIZ, NO_PLAYER, GRAY

# Data structure for stones
from collections import namedtuple

# Tupla para saber la piedra seleccionada o movida por el jugador según sus coordenadas "x", "y" y su "color"
Stone = namedtuple('Stone', ('x', 'y', 'color'))


def set_board_up(stones_per_player = 7):
    'Init stones and board, prepare functions to provide, act as their closure'

    # init board and game data here

    # Inicializamos la tabla BSIZxBSIZ con las casillas vacías
    board = [[" "]*BSIZ for _ in range(BSIZ)]

    # Lista para guardar las piedras jugadas
    played_stones = []

    # Para saber a qué jugador le toca // 0 --> Jugador 1 y 1 --> Jugador 2 
    # También tenemos pensado que la ficha 'X' correspondrá para el jugador 1 y la ficha 'O' para el jugador 2
    curr_player = 0

    # Para saber si se ha seleccionado una piedra o no después de que los dos jugadores hayan movido todas sus piedras disponibles
    stone_selected = True

    # El número total de piedras disponibles entre los dos jugadores 
    total_stones = stones_per_player * 2

    # Coordenadas de la piedra seleccionada. De momento no hay ninguna piedra seleccionada.
    stone_itself = (None, None)
    
    
    def stones():
        "return iterable with the stones already played"
        return played_stones


    # Llamamos esta función una vez que todas las piedras sean jugadas. Seleccionamos
    # la piedra que queremos mover y retornamos True si el jugador ha colocado la piedra
    # en una casilla vacía
    def select_st(i, j):

        '''
        Select stone that current player intends to move. 
        Player must select a stone of his own.
        To be called only after all stones played.
        Report success by returning a boolean;
        '''
        
        # Hacemos que las variables curr_player, total_stones, stone_itself, stone_selected sean 
        # non_local para que las podamos utilizar en esta función
        nonlocal curr_player, total_stones, stone_itself, stone_selected

        # Miramos si se trata del jugador 0 que tiene que seleccionar la piedra y nos aseguramos también
        # de que las coordenadas "i" y "j" estén dentro del rango del tablero
        if curr_player == 0 and 0 <= i < BSIZ and 0 <= j < BSIZ: 

            # Nos aseguramos de que la casilla seleccionada por el jugador sea una de sus piedras
            if board[i][j] == 'X': 

                # Guardamos las coordenadas de la casilla seleccionada y guardamos las coordenadas
                # "x" y "y" en la variable stone_itself
                stone_itself = (i, j)

                # Incrementamos +1 al número total de piedras disponibles porque ahora el jugador 1 
                # ya puede mover una de sus piedras  
                total_stones += 1

                # Hacemos que la variable stone_selected sea True para indicar que ya se ha seleccionado
                # una piedra 
                stone_selected = True

                # Retornamos True para reportar éxito
                return True
            
            # Retornamos False si la piedra seleccionada por el jugador no es una de sus piedras
            return False

        # Hacemos lo mismo que con el jugador 2 
        elif curr_player == 1 and 0 <= i < BSIZ and 0 <= j < BSIZ: 
            if board[i][j] == 'O':
                stone_itself = (i, j)
                total_stones += 1
                stone_selected = True
                return True
        
            return False


    # Función para comprobar si los jugadores han hecho 3 en raya horizontalmente, verticalmente o diagonalmente
    def end():
        'Test whether there are 3 aligned stones'

        # Comprobar por filas
        for i in range(BSIZ):

            # Comprobamos si la primera piedra de la fila 'i' ([board[i][0]]) es igual que los otros elementos que 
            # también están en la misma fila (board[i][j]). Además, nos aseguramos que las casillas que estamos
            # comprobando no sea vacía (board[i][j] != " ").
            if all(board[i][j] == board[i][0] and board[i][j] != " " for j in range(BSIZ)):

                # Retornamos True si alguna de las filas cumple lo anteriormente dicho
                return True

        # Comprobar por columnas
        for j in range(BSIZ):

            # Comprobamos si la primera piedra de la columna 'j' ([board[0][j]]) es igual que los otros elementos que 
            # también están en la misma columna (board[i][j]). 
            if all(board[i][j] == board[0][j] and board[i][j] != " " for i in range(BSIZ)):

                # Retornamos True si alguna de las columnas cumple lo anteriormente dicho
                return True

        # Comprobar por la diagonal principal:
        # Comprobamos si la piedra que se encuentra en la primera fila y columna (board[0][0]) es igual que los demás
        # piedras que se encuentran en la diagonal principal (board[i][i])
        if all(board[i][i] == board[0][0] and board[i][i] != " " for i in range(BSIZ)):

            # Retornamos True si la diagonal principal cumple lo anteriormente dicho
            return True
        
        # Comprobar por la diagonal secundaria
        # Comprobamos si la piedra que se encuentra en la primera fila y última columna (board[0][BSIZ-1]) es igual 
        # que los demás piedras que se encuentran en la diagonal secundaria (board[i][BSIZ - 1 - i])
        if all(board[i][BSIZ - 1 - i] == board[0][BSIZ - 1] and board[i][BSIZ - 1 - i] != " " for i in range(BSIZ)):

            # Retornamos True si la diagonal secundaria cumple lo anteriormente dicho
            return True
        
        # Si ninguna de las condiciones anteriores fueron ciertas, quiere decir que el juego aún no ha acabado
        return False


    # Función para mover las piedras dado unas coordenadas "i" y "j"
    def move_st(i, j):

        '''If valid square, move there selected stone and unselect it,
        then check for end of game, then select new stone for next
        player unless all stones already played; if square not valid, 
        do nothing and keep selected stone.
        
        Return 3 values: bool indicating whether a stone is
        already selected, current player, and boolean indicating
        the end of the game.
        '''

        # Hacemos que las variables curr_player, stone_selected, total_stones y stone_itself sean nonlocal
        nonlocal curr_player, stone_selected, total_stones, stone_itself

        # Obtenemos las coordenadas "x" e "y" de la piedra seleccionada. Esto solo tendrá sentido una vez 
        # después de llamar a la función select_st(). Si no se ha llamado select_st(), "x" e "y" son "None"
        x, y = stone_itself

        # Nos aseguramos que las coordenadas seleccionadas por el jugador estén dentro del rango del tablero
        if not(0 <= i < BSIZ and 0 <= j < BSIZ): 
            print("Las coordenadas que has introducido están mal.")
            return True, curr_player, end()
        
        # Nos aseguramos que la casilla escogida esté vacía
        if board[i][j] != " ": 
            print("Ya hay una ficha en esas coordenadas")
            return True, curr_player, end()

        # Si ninguna de las anteriores condiciones fueron ciertas, entonces, movemos la piedra del jugador 
        # actual a las coordenadas "i" y "j" que haya introducido
        if stone_selected:  

            # Esto solo tiene sentido después de haber llamado a select_st()
            # Vemos si ha seleccionado alguna piedra o no en la función select_st()
            if x != None and y != None: 

                # Eliminamos la piedra seleccionada por el jugador de la lista played_stones
                played_stones.remove(Stone(x, y, PLAYER_COLOR[curr_player]))

                # Hacemos que la casilla donde estaba la piedra seleccionada por el jugador esté vacía otra vez 
                board[x][y] = " "  

            # Vemos si es el turno del jugador 1
            if curr_player == 0: 

                # Imprimos una 'X' en la casilla donde quiere mover la piedra el jugador 1
                board[i][j] = 'X'

            # Vemos si es el turno del jugador 2
            elif curr_player == 1: 

                # Imprimos una 'O' en la casilla donde quiere mover la piedra el jugador 2
                board[i][j] = 'O'

            # Añadimos la piedra jugada por el jugador actual en la lista played_stones
            played_stones.append(Stone(i, j, PLAYER_COLOR[curr_player]))

            # Cambiamos de jugador actual
            curr_player = 1 - curr_player

            # Restamos -1 a la variable 'total_stones' para saber las piedras que aun están disponibles
            total_stones -= 1

            # Miramos el total de piedras aun disponibles, si es cero...
            if total_stones == 0: 

                # ...entonces stone_selected = False porque ya no hay más piedras que mover por parte de los 
                # dos jugadores. De esta manera, entraríamos al bucle while donde el jugador actual tendría 
                # que seleccionar una de sus piedras y moverla
                stone_selected = False

        # Return 3 values: bool indicating whether a stone is already selected, current player, and boolean indicating the end of the game. 
        return stone_selected, curr_player, end()
    

    # Función para imprimir el tablero
    def draw_txt(end = False):

        '''
        Use ASCII characters to draw the board.
        '''

        # Recorre cada fila del tablero
        for row in range(BSIZ): 

            # Recorre cada columna de la fila actual
            for col in range(BSIZ): 

                # Si no es la última columna, imprime el contenido de la celda seguido de una barra vertical "|"
                if col < BSIZ - 1: 
                    print("", board[row][col], "|", end="")
                    
                # Si es la última columna, solo imprime el contenido de la celda
                else: 
                    print("", board[row][col], end="")

            # Termina la fila actual y pasa a una nueva línea
            print()

            # Si no es la última fila, imprime una línea divisoria con guiones para separar las filas
            if row < BSIZ - 1: 
                print("-" * (BSIZ * 4 - 1))


    # return these 4 functions to make them available to the main program
    return stones, select_st, move_st, draw_txt