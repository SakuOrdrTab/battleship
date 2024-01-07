# Laivanupotus 10 * 10 kartalla
# Sääntöinä LLLL, 2 * LLL, 3 * LL, 4 * L
from random import randint

SYMBOLS = {
            "sea" : ".",
            "target" : "L",
            "hit" : "X",
            "miss" : "O",
            "destroyed_target" : "~"
            }

class Player():
    def __init__(self):
        # _display is a private variable for just displaying the game
        self._display = [[SYMBOLS["sea"] for i in range(10)] for j in range(10)]
        # _boats is the private variable for holding the remaining boats. Needs to be separate from display
        self._boats = [[SYMBOLS["sea"] for i in range(10)] for j in range(10)]
        self.get_starting_positions()


    def display_map(self):
        print("  ABCDEFGHIJ")
        rowcount = 0
        for row in self._display:
            rowcount += 1
            print(f"{rowcount:2}", end="")
            for item in row:
                print(item, end="")
            print()

    @classmethod
    def _get_coords(cls, prompt):
        while True:
            coords = input(prompt)
            try:
                items = coords.split(" ")
                x = items[0]
                coord_alphabet = "ABCDEFGHIJabcdefghij"
                if x in coord_alphabet:
                    x = coord_alphabet.find(x.upper())
                else:
                    x = int(x) - 1
                y = int(items[1]) - 1
            except Exception:
                print("Invalidit koordinaatit!")
                continue
            break
        return x, y


    def get_starting_positions(self):
        ship_names = { 4 : "Lentotukialus", 3 : "Risteilijä", 2 : "Hävittäjä", 1 : "Sukellusvene" }
        print()
        print("Laivojen aloituskoordinaatit. Anna koordinaateiksi laivan vasen- tai ylänurkka.")
        for ship_size in range(5,0, -1):
            for ship_number in range(5-ship_size, 0, -1):
                print()
                self.display_map()
                while True:
                    x, y = Player._get_coords(f"Anna koordinaatit ({6-ship_size-ship_number}. {ship_names[ship_size]}) (x y): ")
                    if ship_size > 1:
                        go_horizontal = input("Laitetaanko laiva poikittain? (K/E): ").upper() == "K"
                    else:
                        go_horizontal = True
                    if go_horizontal:
                        if x < 0 or x + ship_size > 10 or y < 0 or y > 9:
                            print("Invalidit koordinaatit!")
                            continue
                        else:
                            cur_map_space = []
                            for i in range(ship_size):
                                cur_map_space.append(self._boats[y][x+i])
                            if SYMBOLS['target'] not in cur_map_space:
                                for i in range(ship_size):
                                    self._boats[y][x+i] = SYMBOLS['target']
                                    self._display[y][x+i] = SYMBOLS['target']
                            else:
                                print("Invalidit koordinaatit!")
                                continue
                    else:
                        if x < 0 or x > 9 or y < 0 or y + ship_size > 10:
                            print("Invalidit koordinaatit!")
                            continue
                        else:
                            cur_map_space = []
                            for i in range(ship_size):
                                cur_map_space.append(self._boats[y+i][x])
                            if SYMBOLS['target'] not in cur_map_space:
                                print(SYMBOLS['target'], " not in ", cur_map_space)
                                for i in range(ship_size):
                                    self._boats[y+i][x] = SYMBOLS['target']
                                    self._display[y+i][x] = SYMBOLS['target']
                            else:
                                print("Invalidit koordinaatit!")
                                continue
                    break

    def bomb(self, another_player : "Player"):
        print("")
        x, y = Player._get_coords("Anna pommituksen koordinaatit: ")
        if another_player._boats[y][x] == SYMBOLS["target"]:
            print("OSUI!")
            self._display[y][x] = another_player._boats[y][x] = SYMBOLS["hit"]
            another_player._display[y][x] = SYMBOLS["destroyed_target"]
        else:
            print("ei osunut")
            self._display[y][x] = SYMBOLS["miss"]
    
    def dead(self):
        if any(SYMBOLS['target'] in row for row in self._boats):
            return False
        else:
            return True


class ComputerPlayer(Player):
    def __init__(self):
        super().__init__()

    def bomb(self, another_player : Player):
        print()
        print("Tietokone pommittaa...")
        while True:
            x, y = randint(0, 9), randint(0, 9)
            if self._display[y][x] in [SYMBOLS["miss"], SYMBOLS["hit"]]:
                continue
            else:
                if another_player._boats[y][x] == SYMBOLS["target"]:
                    print("Tietokone OSUI!")
                    self._display[y][x] = another_player._boats[y][x] = SYMBOLS["hit"]
                    another_player._display[y][x] = SYMBOLS["destroyed_target"]
                else:
                    print("Tietokone ei osunut.")
                    self._display[y][x] = SYMBOLS["miss"]
                break

    def get_starting_positions(self):
        # Carrier
        x, y = randint(0, 4), randint(0,9)
        for i in range(4):
            self._boats[y][x+i] = self._display[y][x+i] = SYMBOLS["target"]
        

        


cp1 = ComputerPlayer()
cp2 = ComputerPlayer()
round = 1
while cp1.dead() == False and cp2.dead() == False:
    print(f"round {round}:")
    cp1.bomb(cp2)
    cp2.bomb(cp1)
    round += 1
    

if cp1.dead():
    print("computer 1 won")
else:
    print("computer 2 won")
