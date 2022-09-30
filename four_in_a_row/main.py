# Here we will implement the assignment using python as our programming language.
from copy import deepcopy


# Constants
BOARD_WIDTH = 5
BOARD_HEIGHT = 10
IN_A_ROW = 4

# Give 1-based index or any based index in python by manipulating the base parameter
def index_notation(index, base=1):
    return index + base

class Game:
    def __init__(self, *players, size=(BOARD_WIDTH,BOARD_HEIGHT), game_n=IN_A_ROW):
        self.players = players
        self.pc = PlayerController(players, board_size=size)
        self.game_n = game_n
        self.board = Board(size, game_n=game_n)
        self.move = 0
        self.title = "Four In A Row"
        self.offset = int((self.board.w*3)/2)
        self.title_offset = self.offset - int(len(self.title)/2)
        # Starting screen
        self.start()
        # Game loop
        while True:
            if self.board.is_full():
                # Draw code
                print("It is a draw!")
                break
            if self.board.has_won():
                # Winning code
                print(f"{self.get_winner()} has won the game!")
                break
            self.next_move()

    def start(self):
        print(f"Welcome to the game!")
        print("\n")
        print(f"{self.players[0].name}: {self.players[0].symbol}")
        print(f"{self.players[1].name}: {self.players[1].symbol}")
        print("\n")
        print(self.board)
    def show_title(self):
        spaces = " "*self.title_offset
        print(spaces + self.title)
    def next_move(self):
        self.move += 1
        move_text = f"Move {self.move}:"
        move_offset = self.offset - int(len(move_text)/2)
        spaces = " "*move_offset
        succes = False
        print(f"The best choice according to the minmax algorithm would be: {Minimax(self.board, self.pc).get()}")
        while not succes:
            player, slot = self.pc.get_turn()
            succes = self.board.place(player, slot)
        self.pc.update_turn()
        # maybe center move_text in the future
        print(f"\n{spaces + move_text}\n\n")
        print(self.board)

    def get_winner(self):
        (row,col) = self.board.last_played
        symbol = self.board.board[row][col]
        for player in self.players:
            if player.symbol == symbol:
                return player.name

class Board:
    def __init__(self,size,game_n=IN_A_ROW):
        (self.w,self.h) = size
        self.game_n = game_n
        self.board = []
        self.last_played = None # (row, col) of last played symbol
        #Create board
        for row in range(self.h):
            self.board.append([])
            for col in range(self.w):
                self.board[row].append('~')

    def __str__(self):
        border = "-"*self.w*3
        title = "Four In A Row"
        title_offset = int(len(border)/2) - int(len(title)/2)
        spaces = " "*title_offset
        slots = "".join([f" {index_notation(i)} " for i in range(self.w)])

        output = spaces + title + "\n" + border
        for row in range(self.h):
            output += "\n"
            for col in range(self.w):
                output += f" {self.board[row][col]} "
        # add slot info with border
        output += "\n" + border + "\n" + slots + "\n"
        return output

    def __eq__(self, other):
        if self.h != other.h or self.w != other.w:
            return False
        else:
            for row in reversed(range(self.h)):
                for col in range(self.w):
                    if self.board[row][col] != other.board[row][col]:
                        return False
            return True


    def place(self, player, slot):

        def slot_full(slot):
            for row in range(self.h):
                if self.board[row][slot] == '~':
                    return False
            return True

        def get_row(slot):
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
        self.board[self.last_played[0]][self.last_played[1]] = "~"


    def is_full(self):
        for row in reversed(range(self.h)):
            for col in range(self.w):
                if self.board[row][col] == "~":
                    return False
        return True

    def has_won(self):
        if self.last_played == None:
            return False
        (row,col) = self.last_played

        def on_board(row=row, col=col, state='horizontal'):
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
            n = self.game_n - 1
            symbol = self.board[row][col]
            i = 1
            left = True
            while n > 0:
                if left:
                    if on_board(col=col-i, state='horizontal'):
                        if self.board[row][col - i] == symbol:
                            n -= 1
                            i += 1
                        else:
                            i = 1
                            left = False
                    else:
                        left = False
                else:
                    if on_board(col=col+i, state='horizontal'):
                        if self.board[row][col + i] == symbol:
                            n -= 1
                            i += 1
                        else:
                            return n == 0
                    else:
                        return n == 0
            return True


        def is_vertical():
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
                        top = False
                else:
                    if on_board(row=row+i, state='vertical'):
                        if self.board[row+i][col] == symbol:
                            n -= 1
                            i += 1
                        else:
                            return n == 0
                    else:
                        return n == 0
            return True

        def is_diagonal_down():
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
                        left_top = False
                else:
                    if on_board(row=row+i,col=col+i, state='diagonal'):
                        if self.board[row+i][col + i] == symbol:
                            n -= 1
                            i += 1
                        else:
                            return n == 0
                    else:
                        return n == 0
            return True
        def is_diagonal_up():
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
                        right_top = False
                else:
                    if on_board(row=row+i,col=col-i, state='diagonal'):
                        if self.board[row+i][col-i] == symbol:
                            n -= 1
                            i += 1
                        else:
                            return n == 0
                    else:
                        return n == 0
            return True

        return is_horizontal() or is_vertical() or is_diagonal_down() or is_diagonal_up()


class Player:
    def __init__(self, symbol, name):
        self.name = name
        self.symbol = symbol
    def ask(self, limit=0):
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
        self.turn_index = 0
        self.board_size = board_size
        self.players = players
    def get_player(self):
        return self.players[self.turn_index]

    def get_turn(self):
        turn = self.turn_index
        player = self.get_player()
        slot = player.ask(self.board_size[0])

        return player, slot
    def update_turn(self):
        self.turn_index = 1 if self.turn_index == 0 else 0



class Minimax:
    def __init__(self, board, pc): # state = the current state of the board of the game
        self.board = board
        self.pc = pc

    def dfs_for_score(self, board, pc, layer, is_max):
        """
        Computes the best choice for the player given a current board state.

        Parameters:
        board (two-d list): current board state from where we want to search
        pc (PlayerController): switches between two players that have been assigned to it.
        layer (int): keeps track of the depth the function is currently at recursively

        Returns: (int, int) First int is the best score you can get, second one is the best slot you can currently choose
        """
        # self.board.w gives the slots you can play
        options = list(range(self.board.w))
        scores = list()
        for i,option in enumerate(options):
            succes = board.place(pc.get_player(), option)
            #print(board)
            # base case for if the player makes a winning move
            if board.has_won():
                return self.give_score(layer, option, is_max)
            elif board.is_full():
                return self.give_score(layer, option, is_max, board_full=True)
            # if a move is valid (no full slot or some other constraint)
            elif succes:
                pc.update_turn()
                scores.append(self.dfs_for_score(deepcopy(board), deepcopy(pc), layer+1, not is_max))
                pc.update_turn()
                board.undo()
        # either minimize or maximize depending on the player that is allowed to move
        return self.get_best_move(scores, is_max, layer)

    def give_score(self, layer, option, is_max, board_full=False):
        """
        Computes the score based on the player that is to move, and also has a base case for if an ending state is immediately reached.

        Parameters:
        layer (int): The depth we are currently looking at in the game tree
        option (int): The option under consideration (the move we would want to possibly make as a player)
        is_max (bool): Says whether or not we are in a maximizing state
        (Optional) board_full (bool): tells the function if the game is in a draw or not

        Returns (int/(int,int)): Either gives the best score ( int ), or it gives the best score together with the move to make ( (int,int ) )

        """
        if board_full:
            if layer == 0:
                return (0,index_notation(option))
            else:
                return 0
        elif is_max:
            if layer == 0:
                return (1,index_notation(option))
            else:
                return 1
        else:
            if layer == 0:
                return (-1,index_notation(option))
            else:
                return -1

    def get_best_move(self, scores, is_max, layer):
        """
        Computes the best move to make along with it's best score when it searches through the game tree

        Parameters:
        scores (list): list with the possible scores you can get from that node.
        is_max (bool): state that gives you information about whether your in a maximizing or a minimizing state.
        layer (int): int that gives you your current depth in the game search tree.

        Returns (int/(int,int)): Either gives the best score ( int ), or it gives the best score together with the move to make ( (int,int ) )
        """
        if is_max:
            if len(scores) == 0:
                return 0
            else:
                maxim = max(scores)
                if layer == 0:
                    return (maxim, scores.index(maxim))
                else:
                    return maxim
        else:
            if len(scores) == 0:
                return 0
            else:
                minim = min(scores)
                if layer == 0:
                    return (minim, scores.index(minim))
                else:
                    return minim

    def get(self):
        score = self.dfs_for_score(deepcopy(self.board), deepcopy(self.pc), 0, True)
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
    #Minimax(board, pc)

    # General testing
    game = Game(Player("X", "Player2"), Player("O", "Player1"), size=(3,3), game_n=3)
