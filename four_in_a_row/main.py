# Here we will implement the assignment using python as our programming language.
class Game:
    def __init__(self, *players, size=(10,5)):
        self.players = players
        self.pc = PlayerController(players)
        self.title = "Four In A Row"
        self.title_offset = int((self.board.w*3)/2) - int(len(self.title)/2)
        self.board = Board(size)
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
        player, slot = self.pc.get_turn()
        self.board.place(player, slot)

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
        output = spaces + title + "\n" + border
        for row in range(self.h):
            output += "\n"
            for col in range(self.w):
                output += f" {self.board[row][col]} "
        return output + "\n" + border
    def place(self, player, slot):
        pass
    def has_won(self):
        return False


class Player:
    def __init__(self, symbol):
        self.symbol = symbol
    def ask(self):
        slot = input("What slot do you want to select? (ex. 1, 2)")
        return int(slot)

# This player controller is designed for 2 players, there is no support currently for more.
class PlayerController:
    def __init__(self, players):
        self.turn_index = 0
        self.players = players
    def get_turn(self):
        turn = self.turn_index
        player = self.players[turn]
        slot = player.ask()
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
    player1 = Player("X")
    player2 = Player("O")
    game = Game(player1,player2, size=(5,5))
    game.start()
    game.next_move()
