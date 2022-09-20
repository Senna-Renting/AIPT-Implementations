# Here we will implement the assignment using python as our programming language.

# Constants
BOARD_WIDTH = 5
BOARD_HEIGHT = 10
IN_A_ROW = 4

# Give 1-based index or any based index in python by manipulating the base parameter
def index_notation(index, base=1):
    return index + base

class Game:
    def __init__(self, *players, size=(BOARD_WIDTH,BOARD_HEIGHT), gameN=IN_A_ROW):
        self.players = players
        self.pc = PlayerController(players, board_size=size)
        self.gameN = gameN
        self.board = Board(size, gameN=gameN)
        self.move = 0
        self.title = "Four In A Row"
        self.offset = int((self.board.w*3)/2)
        self.title_offset = self.offset - int(len(self.title)/2)
        # Starting screen
        self.start()
        # Game loop
        while not self.board.has_won():
            self.next_move()
        # Winning code
        print(f"{self.get_winner()} has won the game!")

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
    def __init__(self,size,gameN=IN_A_ROW):
        (self.w,self.h) = size
        self.gameN = gameN
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

    def place(self, player, slot):

        def get_row(slot):
            for row in reversed(range(self.h)):
                if self.board[row][slot] == '~':
                    return row

        def slot_full(slot):
            for row in range(self.h):
                if self.board[row][slot] == '~':
                    return False
            return True

        if not slot_full(slot):
            row = get_row(slot)
            self.board[row][slot] = player.symbol
            self.last_played = (row, slot)
            return True
        else:
            print("That slot is full please try another")
            return False

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
            n = self.gameN - 1
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
            n = self.gameN - 1
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
            n = self.gameN - 1
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
            n = self.gameN - 1
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
    pass

# maybe seperate minimax and alphabeta pruning into different classes

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
    player1 = Player("X", "Player 1")
    player2 = Player("O", "Player 2")
    game = Game(player1,player2, size=(5,5))
