# Here we will implement the assignment using python as our programming language.

# Give 1-based index or any based index in python by manipulating the base parameter
def index_notation(index, base=1):
    return index + base

class Game:
    def __init__(self, *players, size=(10,5)):
        self.players = players
        self.pc = PlayerController(players)
        self.board = Board(size)
        self.move = 0
        self.title = "Four In A Row"
        self.title_offset = int((self.board.w*3)/2) - int(len(self.title)/2)

    def start(self):
        self.show_title()
        print("\n")
        print(f"Player 1: {self.players[0].symbol}")
        print(f"Player 2: {self.players[1].symbol}")
        print("\n")
        print(self.board)
    def show_title(self):
        spaces = " "*self.title_offset
        print(spaces + self.title)
    def next_move(self):
        self.move += 1
        move_text = f"Move {self.move}:"
        player, slot = self.pc.get_turn()
        self.board.place(player, slot)
        # maybe center move_text in the future
        print(f"{move_text}\n\n")
        print(self.board)

class Board:
    def __init__(self,size):
        (self.w,self.h) = size
        print(self.w,self.h)
        self.board = []
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
        output += "\n" + border + "\n" + slots
        return output
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
            self.board[get_row(slot)][slot] = player.symbol

    def has_won(self):
        return False


class Player:
    def __init__(self, symbol):
        self.symbol = symbol
    def ask(self, index=1):
        slot = None
        while slot == None:
            try:
                slot = int(input(f"What slot do you want to select player {index}? (ex. 1, 2)")) - 1
            except:
                print("That is not a number, please try again ")
        return slot

# This player controller is designed for 2 players, there is no support currently for more.
class PlayerController:
    def __init__(self, players):
        self.turn_index = 0
        self.players = players
    def get_turn(self):
        turn = self.turn_index
        player = self.players[turn]
        slot = player.ask(index_notation(self.turn_index))
        self.turn_index = 1 if self.turn_index == 0 else 0

        return player, slot



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
    player1 = Player("P")
    player2 = Player("O")
    game = Game(player1,player2, size=(5,5))
    game.start()
    game.next_move()
