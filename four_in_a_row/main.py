# Here we will implement the assignment using python as our programming language.

# this module was used to support copying multidimensional lists
from copy import deepcopy


# Constants
BOARD_WIDTH = 5
BOARD_HEIGHT = 10
IN_A_ROW = 4

# Global variables
count_complexity = 0

# Give 1-based index or any based index in python by manipulating the base parameter
def index_notation(index, base=1):
    return index + base

class GameOfN:
    def __init__(self, *players, size=(BOARD_WIDTH,BOARD_HEIGHT), game_n=IN_A_ROW, minmax=True, use_alphabeta=False):
        """
        Function: Initialize a terminal based game environment for the game Four In A Row, or N In A Row where you can choose the value of N.

        Parameters:
        *players (args list): An arguments list containing the players as Player objects
        size (tuple): A tuple containing the width and height of the board respectively
        game_n (int): An integer that indicates the number in a row that we see as winning
        minmax (bool): Boolean which determines whether or not to use the minmax heuristic
        use_alphabeta (bool): Boolean that indicates whether or not we want to use alpha-, beta pruning with the minmax heuristic algorithm

        Returns: None
        """
        self.players = players
        self.pc = PlayerController(players, board_size=size)
        self.game_n = game_n
        self.minmax = minmax
        self.use_alphabeta = use_alphabeta
        self.board = Board(size, game_n=game_n)
        self.move = 0
        n_in_a_row = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
        if self.game_n <= 10:
            self.title = f"{n_in_a_row[self.game_n-1]} In A Row"
        else:
            self.title = "N In A Row"
        self.board.title = self.title
        self.offset = int((self.board.w*3)/2)
        self.title_offset = self.offset - int(len(self.title)/2)
        # Starting screen
        self.start()
        # Game loop
        while True:
            if self.board.has_won():
                # Winning code
                print(f"{self.get_winner()} has won the game!")
                break
            if self.board.is_full():
                # Draw code
                print("It is a draw!")
                break
            self.next_move()

    def start(self):
        """
        Function: Print an introductory message before starting the gameplay
        """
        print(f"Welcome to the game!")
        print("\n")
        print(f"{self.players[0].name}: {self.players[0].symbol}")
        print(f"{self.players[1].name}: {self.players[1].symbol}")
        print("\n")
        print(self.board)

    def next_move(self):
        """
        Function: Start a new move where another player gets to move after which the resulting board is shown
        """
        self.move += 1
        move_text = f"Move {self.move}:"
        move_offset = self.offset - int(len(move_text)/2)
        spaces = " "*move_offset
        succes = False
        if self.minmax:
            minmax_obj = Minimax(self.board, self.pc, use_alphabeta=self.use_alphabeta)
            if self.use_alphabeta:
                print(f"The best choice according to the alpha beta pruning algorithm would be: {minmax_obj.get()}")
            else:
                print(f"The best choice according to the minimax algorithm would be: {minmax_obj.get()}")
        while not succes:
            player, slot = self.pc.get_turn()
            succes = self.board.place(player, slot)
        self.pc.update_turn()
        # maybe center move_text in the future
        print(f"\n{spaces + move_text}\n\n")
        print(self.board)

    def get_winner(self):
        """
        Function: Get the player that has won based on the last move
        """
        (row,col) = self.board.last_played
        symbol = self.board.board[row][col]
        for player in self.players:
            if player.symbol == symbol:
                return player.name

class Board:
    def __init__(self,size=(BOARD_WIDTH, BOARD_HEIGHT),game_n=IN_A_ROW):
        """
        Function: Generate a board for the GameOfN object to play on

        Parameters:
        size (tuple): A tuple containing the width and height of the board respectively
        game_n (int): An integer that indicates the number in a row that we see as winning

        Returns: None
        """
        (self.w,self.h) = size
        self.game_n = game_n
        self.board = []
        self.title = "Four In A Row"
        self.last_played = None # (row, col) of last played symbol
        #Create board
        for row in range(self.h):
            self.board.append([])
            for col in range(self.w):
                self.board[row].append('~')

    def __str__(self):
        """
        Function: Give a string representation of the object for when it is printed
        """
        border = "-"*self.w*3
        title_offset = int(len(border)/2) - int(len(self.title)/2)
        spaces = " "*title_offset
        slots = "".join([f" {index_notation(i)} " for i in range(self.w)])

        output = spaces + self.title + "\n" + border
        for row in range(self.h):
            output += "\n"
            for col in range(self.w):
                output += f" {self.board[row][col]} "
        # add slot info with border
        output += "\n" + border + "\n" + slots + "\n"
        return output

    def __eq__(self, other):
        """
        Function: Determine whether two board objects are the same

        Parameters:
        self: The current object
        other: The object we are comparing with

        Returns (bool): True if the Board objects are equal according to this function
        """
        if self.h != other.h or self.w != other.w:
            return False
        else:
            for row in reversed(range(self.h)):
                for col in range(self.w):
                    if self.board[row][col] != other.board[row][col]:
                        return False
            return True


    def place(self, player, slot):
        """
        Function: Correctly place a symbol on the board when the player and the slot it wants are given

        Parameters:
        player (Player): Player object that has requested a slot
        slot (int): The slot that the player has requested

        Returns (bool): True if it has correctly placed the symbol of the player on the board
        """
        def slot_full(slot):
            """
            Function: Check if a slot of the board is completely full

            Parameters:
            slot (int): The slot that needs checking

            Returns (bool): True if the slot is found full
            """
            for row in range(self.h):
                if self.board[row][slot] == '~':
                    return False
            return True

        def get_row(slot):
            """
            Function: Get the first free row inside a slot of the board (looking from the bottom to the top of the slot)

            Parameters:
            slot (int): The slot that needs to be reviewed

            Returns (int): value of the row that is free
            """
            for row in reversed(range(self.h)):
                if self.board[row][slot] == '~':
                    return row

        if not slot_full(slot):
            row = get_row(slot)
            self.board[row][slot] = player.symbol
            self.last_played = (row, slot)
            return True
        else:
            #print("That slot is full please try another")
            return False

    def undo(self):
        """
        Function: Undo the last played move on the board
        """
        self.board[self.last_played[0]][self.last_played[1]] = "~"


    def is_full(self):
        """
        Function: Check if the board is full

        Returns (bool): True if the board is full
        """
        for row in reversed(range(self.h)):
            for col in range(self.w):
                if self.board[row][col] == "~":
                    return False
        return True

    def has_won(self):
        """
        Function: Check if the board is in a win state

        Returns (bool): True if the board is in a win state
        """
        if self.last_played == None:
            return False
        (row,col) = self.last_played

        def on_board(row=row, col=col, state='horizontal'):
            """
            Function: Check if a row and column are within the space of the board

            Parameters:
            row (int): value of the row
            col (int): value of the column
            state (str): specific state that needs checking ('horizontal', 'vertical', 'diagonal')

            Returns (bool): True if the row and col are a valid location on the board
            """
            horizontal = col >= 0 and col < self.w
            #print(f"on board: {horizontal}")
            vertical = row >= 0 and row < self.h
            if state == 'horizontal':
                return horizontal
            elif state == 'vertical':
                return vertical
            elif state == 'diagonal':
                return horizontal and vertical
            else:
                print("please give a valid state: (horizontal, vertical, diagonal)")


        def is_horizontal():
            """
            Function: Check if a horizontal win state is present

            Returns: True if a horizontal win state has been found
            """
            n = self.game_n - 1
            symbol = self.board[row][col]
            i = 1
            left = True
            while n > 0:
                if left:
                    if on_board(col=col-i, state='horizontal'):
                        #print(f"Check: {row} :: {col-i}")
                        #print(f"Symbol: {symbol}")
                        if self.board[row][col - i] == symbol:
                            n -= 1
                            i += 1
                        else:
                            i = 1
                            left = False
                    else:
                        i = 1
                        left = False
                else:
                    if on_board(col=col+i, state='horizontal'):
                        if self.board[row][col + i] == symbol:
                            #print(f"Check: {row} :: {col+i}")
                            #print(f"Symbol: {symbol}")
                            n -= 1
                            i += 1
                        else:
                            return n <= 0
                    else:
                        return n <= 0
            return True


        def is_vertical():
            """
            Function: Check if a vertical win state is present

            Returns: True if a vertical win state has been found
            """
            n = self.game_n - 1
            symbol = self.board[row][col]
            i = 1
            top = True
            while n > 0:
                if top:
                    if on_board(row=row-i, state='vertical'):
                        if self.board[row-i][col] == symbol:
                            n -= 1
                            i += 1
                        else:
                            i = 1
                            top = False
                    else:
                        i = 1
                        top = False
                else:
                    if on_board(row=row+i, state='vertical'):
                        if self.board[row+i][col] == symbol:
                            n -= 1
                            i += 1
                        else:
                            return n <= 0
                    else:
                        return n <= 0
            return True

        def is_diagonal_down():
            """
            Function: Check if a downwards diagonal win state is present

            Returns: True if a downwards diagonal win state has been found
            """
            n = self.game_n - 1
            symbol = self.board[row][col]
            i = 1
            left_top = True
            while n > 0:
                if left_top:
                    if on_board(row=row-i,col=col-i, state='diagonal'):
                        if self.board[row-i][col - i] == symbol:
                            n -= 1
                            i += 1
                        else:
                            i = 1
                            left_top = False
                    else:
                        i = 1
                        left_top = False
                else:
                    if on_board(row=row+i,col=col+i, state='diagonal'):
                        if self.board[row+i][col + i] == symbol:
                            n -= 1
                            i += 1
                        else:
                            return n <= 0
                    else:
                        return n <= 0
            return True
        def is_diagonal_up():
            """
            Function: Check if a upwards diagonal win state is present

            Returns: True if a upwards diagonal win state has been found
            """
            n = self.game_n - 1
            symbol = self.board[row][col]
            i = 1
            right_top = True
            while n > 0:
                if right_top:
                    if on_board(row=row-i,col=col+i, state='diagonal'):
                        if self.board[row-i][col+i] == symbol:
                            n -= 1
                            i += 1
                        else:
                            i = 1
                            right_top = False
                    else:
                        i = 1
                        right_top = False
                else:
                    if on_board(row=row+i,col=col-i, state='diagonal'):
                        if self.board[row+i][col-i] == symbol:
                            n -= 1
                            i += 1
                        else:
                            return n <= 0
                    else:
                        return n <= 0
            return True

        return is_horizontal() or is_vertical() or is_diagonal_down() or is_diagonal_up()


class Player:
    def __init__(self, symbol, name):
        """
        Function: Initialize the player object for playing a GameOfN

        Parameters:
        symbol (str): Symbol we want to associate with the player
        name (str): Actual name of the player

        Returns: None
        """

        self.name = name
        self.symbol = symbol

    def ask(self, limit=0):
        """
        Function: Ask the player to choose a slot on the board of the GameOfN

        Parameters:
        limit (int): upper bound of the slots we can choose from (this should be equal to the width of the board of the GameOfN)

        Returns (int): The slot chosen by the player
        """
        slot = None
        while slot == None or (slot > BOARD_WIDTH or slot < 0):
            try:
                slot = int(input(f"What slot do you want to select {self.name}? (ex. 1, 2): ")) - 1
                if slot > limit or slot < 0:
                    slot = None
                    print(f"That is not on the board please choose a number between 1 and {BOARD_WIDTH}!")
            except:
                print("That is not a number, please try again ")
        return slot

# This player controller is designed for 2 players, there is no support currently for more (and that is also not necessary).
class PlayerController:
    def __init__(self, players, board_size=(BOARD_WIDTH, BOARD_HEIGHT)):
        """
        Function: Initialize the PlayerController

        Parameters:
        players (list): list of Player objects available to the PlayerController for alternating between them
        board_size (tuple): A tuple containing the width and height of the board respectively

        Returns: None
        """
        self.turn_index = 0
        self.board_size = board_size
        self.players = players

    def get_player(self):
        """
        Function: Get the current activated/moving player

        Returns (Player): Player object that is to move next on the board
        """
        return self.players[self.turn_index]

    def get_turn(self):
        """
        Function: Ask current player for a move

        Returns (Player, int): A player and it's chosen move/slot
        """
        turn = self.turn_index
        player = self.get_player()
        slot = player.ask(self.board_size[0])

        return player, slot

    def update_turn(self):
        """
        Function: Alternate to another player

        Returns: None
        """
        self.turn_index = 1 if self.turn_index == 0 else 0



class Minimax:
    def __init__(self, board, pc, use_alphabeta=False): # state = the current state of the board of the game
        """
        Function: Initialize minimax object

        Parameters:
        board (two-d list): current board state from where we want to search
        pc (PlayerController): switcher between two players that have been assigned to it.
        (Optional) use_alphabeta (bool): Determines whether or not we want to use alphabeta pruning with the minimax algorithm

        Returns: None
        """
        self.board = board
        self.pc = pc
        self.use_alphabeta = use_alphabeta

    # we still need to implement the alpha beta pruning part of the algorithm
    def dfs_for_score(self, board, pc, layer=0, is_max=True, alpha=None, beta=None, use_alphabeta=False):
        """
        Computes the best choice for the player given a current board state.

        Parameters:
        board (two-d list): current board state from where we want to search
        pc (PlayerController): switcher between two players that have been assigned to it.
        layer (int): keeps track of the depth the function is currently at recursively
        is_max (bool): Determines if we are in a maximizing node or in a minimizing one according to the minimax algorithm and the recursively iterated game state tree
        (Optional) alpha (int): Alpha value when alphabeta pruning method is used
        (Optional) beta (int): Beta value when alphabeta pruning method is used
        (Optional) use_alphabeta (bool): Determines whether or not we want to use alphabeta pruning with the minimax algorithm

        Returns: (int, int) First int is the best score you can get, second one is the best slot you can currently choose
        """
        global count_complexity
        count_complexity += 1
        # self.board.w gives the slots you can play
        options = list(range(self.board.w))
        scores = list()
        slots = list()
        for i,option in enumerate(options):
            #print(board)
            succes = board.place(pc.get_player(), option)
            # base case for if the player makes a winning move
            if board.has_won():
                slots.append(option)
                score = self.give_score(is_max)
                scores.append(score)
            elif board.is_full():
                slots.append(option)
                score = self.give_score(is_max, board_full=True)
                scores.append(score)
            # if a move is valid (no full slot or some other constraint)
            elif succes:
                pc.update_turn()
                slots.append(option)
                # handle alphabeta pruning choice for score generation
                if use_alphabeta:
                    score = self.dfs_for_score(deepcopy(board), deepcopy(pc), layer+1, not is_max, alpha, beta, use_alphabeta=True)
                else:
                    score = self.dfs_for_score(deepcopy(board), deepcopy(pc), layer+1, not is_max)
                scores.append(score)
                pc.update_turn()
                board.undo()
            # the alpha beta pruning part of the code
            if use_alphabeta:
                alpha, beta, prune = self.update_alphabeta(scores, alpha, beta, is_max)
                if prune:
                    return self.prune(scores, is_max)
        # either minimize or maximize depending on the player that is allowed to move
        if layer == 0:
            print(f"Number of searches needed for minimax algorithm: {count_complexity}")
            count_complexity = 0
        return self.get_best_move(scores, slots, is_max, layer)

    def prune(self, scores, is_max):
        """
        Function: Prune the search tree by returning the result based on alphabeta checks

        Parameters:
        scores (list): list with the possible scores you can get from that node.
        is_max (bool): Determines if we are in a maximizing node or in a minimizing one according to the minimax algorithm and the recursively iterated game state tree

        Returns (int): The termination score we get after pruning
        """
        if is_max:
            return max(scores)
        else:
            return min(scores)

    def update_alphabeta(self, scores, alpha, beta, is_max):
        """
        Function: Update alpha and beta values correctly given the node type and it's best score together with current alpha and beta values.

        Parameters:
        scores (list): list with the possible scores you can get from that node.
        alpha (int): current alpha value
        beta (int): current beta value
        is_max (bool): Determines if we are in a maximizing node or in a minimizing one according to the minimax algorithm and the recursively iterated game state tree

        Returns (int, int, bool): (updated alpha value, updated beta value, condition whether to prune or not)
        """
        prune = False
        if len(scores) == 0:
            return alpha, beta, prune
        else:

            if is_max:
                max_score = max(scores)
                # updating alpha value for max node
                if alpha == None:
                    alpha = max_score
                elif max_score > alpha:
                    alpha = max_score
                # check for pruning
                if beta != None:
                    if max_score >= beta:
                        prune = True
            else:
                min_score = min(scores)
                # updating beta value for min node
                if beta == None:
                    beta = min_score
                elif min_score < beta:
                        beta = min_score
                # check for pruning
                if alpha != None:
                    if min_score <= alpha:
                        prune = True
        return alpha, beta, prune


    def give_score(self, is_max, board_full=False):
        """
        Function: Computes the score based on the player that is to move.

        Parameters:
        is_max (bool): Says whether or not we are in a maximizing state
        (Optional) board_full (bool): tells the function if the game is in a draw or not

        Returns (int/(int,int)): Either gives the best score ( int ), or it gives the best score together with the move to make ( (int,int ) )

        """
        if board_full:
            return 0
        elif is_max:
            return 1
        else:
            return -1

    def get_best_move(self, scores, slots, is_max, layer):
        """
        Function: Computes the best move to make along with it's best score when it searches through the game tree

        Parameters:
        scores (list): list with the possible scores you can get from that node.
        is_max (bool): state that gives you information about whether your in a maximizing or a minimizing state.
        layer (int): int that gives you your current depth in the game search tree.

        Returns (int/(int,int)): Either gives the best score ( int ), or it gives the best score together with the move to make ( (int,int ) )
        """
        if is_max:
            # len(score) == 0 case has now been removed
            maxim = max(scores)
            if layer == 0:
                #print(scores)
                return (maxim, index_notation(slots[scores.index(maxim)]))
            else:
                return maxim
        else:
            # len(score) == 0 case has now been removed
            minim = min(scores)
            if layer == 0:
                #print(scores)
                return (minim, index_notation(slots[scores.index(minim)]))
            else:
                return minim

    def get(self):
        """
        Function: Get the current best move according to the minimax algorithm

        Returns (int): The best move according to the minimax algorithm
        """
        score = self.dfs_for_score(deepcopy(self.board), deepcopy(self.pc), use_alphabeta=self.use_alphabeta)
        return score[1]






# maybe split minimax and alphabeta pruning into different classes

# class Alphabeta:
#   pass

if __name__ == "__main__":
    # Board testing

    #board = Board((10,3))
    #board.show_title()

    # PlayerController testing

    #pc = PlayerController(Player("O"), Player("X"))
    #for i in range(5):
    #    pc.ask_player()

    # Game testing
    #player1 = Player("X", "Player 1")
    #player2 = Player("O", "Player 2")
    #game = Game(player1,player2, size=(5,5))

    # Minimax debugging
    #board = Board(size=(3,3), game_n=3)
    #p1 = Player("X", "Player1")
    #p2 = Player("O", "Player2")
    #pc = PlayerController((p1,p2))
    #minmax = Minimax(board, pc)
    #print(minmax.update_alphabeta([1,10,11,-3], None, 3, True))

    # General testing
    game = GameOfN(Player("X", "Player2"), Player("O", "Player1"), size=(3,3), game_n=3, use_alphabeta=True)
