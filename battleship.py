# Laivanupotus 10 * 10 kartalla
# Sääntöinä LLLL, 2 * LLL, 3 * LL, 4 * L
from random import randint

SYMBOLS = {
            "sea" : ".",
            "hit" : "X",
            "miss" : "O",
            "destroyed_target" : "~",
            "target" : "L",
            "carrier" : 4,
            "cruiser" : 3,
            "destroyer" : 2,
            "submarine" : 1
            }

class Player():
    def __init__(self):
        # _display is a private variable for just displaying the game
        self._display = [[SYMBOLS["sea"] for i in range(10)] for j in range(10)]
        # _boats is the private variable for holding the remaining boats. Needs to be separate from display
        self._boats = [[SYMBOLS["sea"] for i in range(10)] for j in range(10)]
        self.get_starting_positions()


    def display_map(self):
        print("   ABCDEFGHIJ")
        rowcount = 0
        for row in self._display:
            rowcount += 1
            print(f"{rowcount:2} ", end="")
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
                print("Invalid coordinates!")
                continue
            break
        return x, y


    def get_starting_positions(self):
        ship_names = { 4 : "Carrier", 3 : "Cruiser", 2 : "Destroyer", 1 : "Submarine" }
        print()
        print("The starting coordinates for ships. Give coordinates to the upper, or left margin of the ship.")
        for ship_size in range(5,0, -1):
            for ship_number in range(5-ship_size, 0, -1):
                print()
                self.display_map()
                while True:
                    x, y = Player._get_coords(f"Give coordinates ({6-ship_size-ship_number}. {ship_names[ship_size]}) (x y): ")
                    if ship_size > 1:
                        go_horizontal = input("Place ship horizontally? (Y/N): ").upper() == "Y"
                    else:
                        go_horizontal = True
                    if go_horizontal:
                        if x < 0 or x + ship_size > 10 or y < 0 or y > 9:
                            print("Invalid coordinates!")
                            continue
                        else:
                            cur_map_space = []
                            for i in range(ship_size):
                                cur_map_space.append(self._boats[y][x+i])
                            if any(num + 1 not in cur_map_space for num in range(4)):
                                for i in range(ship_size):
                                    self._boats[y][x+i] = ship_size
                                    self._display[y][x+i] = SYMBOLS['target']
                            else:
                                print("Invalid coordinates!")
                                continue
                    else:
                        if x < 0 or x > 9 or y < 0 or y + ship_size > 10:
                            print("Invalid coordinates!")
                            continue
                        else:
                            cur_map_space = []
                            for i in range(ship_size):
                                cur_map_space.append(self._boats[y+i][x])
                            if any(num + 1 not in cur_map_space for num in range(4)):
                                print(SYMBOLS['target'], " not in ", cur_map_space)
                                for i in range(ship_size):
                                    self._boats[y+i][x] = ship_size
                                    self._display[y+i][x] = SYMBOLS['target']
                            else:
                                print("Invalid coordinates!")
                                continue
                    break

    def bomb(self, another_player : "Player"):
        print("")
        x, y = Player._get_coords("Give coordinates for bombing (X Y): ")
        if another_player._boats[y][x] in range(4)+1:
            print("A HIT! ", another_player._boats[y][x], " was hit")
            self._display[y][x] = another_player._boats[y][x] = SYMBOLS["hit"]
            another_player._display[y][x] = SYMBOLS["destroyed_target"]
        else:
            print("A miss.")
            self._display[y][x] = SYMBOLS["miss"]
    
    def dead(self):
        return not any(num in [1, 2, 3, 4] for row in self._boats for num in row)


class ComputerPlayer(Player):
    def __init__(self):
        super().__init__()
        self._hits = [] # tuple (y, x)

    def bomb(self, another_player : Player):
        print()
        print("Computer is bombing")
        # Check if there are hits to bomb more
        
        while True:
            x, y = randint(0, 9), randint(0, 9)
            if self._display[y][x] in [SYMBOLS["miss"], SYMBOLS["hit"]]:
                continue
            else:
                if another_player._boats[y][x] in [x+1 for x in range(4)]:
                    print("Computer HITS! target: ", another_player._boats[y][x])
                    self._display[y][x] = another_player._boats[y][x] = SYMBOLS["hit"]
                    another_player._display[y][x] = SYMBOLS["destroyed_target"]
                    self._hits.append((y, x))
                else:
                    print("Computer missed.")
                    self._display[y][x] = SYMBOLS["miss"]
                break

    def get_starting_positions(self):
        for ship_size in range(1, 5):
            for n in range(5 - ship_size, 0, -1):
                while True:
                    go_horizontal = bool(randint(0, 1))
                    if go_horizontal:
                        starting_x = randint(0, 9 - ship_size)
                        starting_y = randint(0, 9)
                    else:
                        starting_x = randint(0, 9)
                        starting_y = randint(0, 9 - ship_size)
                    if go_horizontal:
                        cur_map_space = []
                        for i in range(ship_size):
                            cur_map_space.append(self._boats[starting_y][starting_x + i])
                        if all(num + 1 not in cur_map_space for num in range(4)):
                            for i in range(ship_size):
                                self._boats[starting_y][starting_x + i] = ship_size
                                self._display[starting_y][starting_x + i] = SYMBOLS['target']
                            break  # Exit the while loop when ship placement is successful
                        else:
                            continue
                    else:
                        cur_map_space = []
                        for i in range(ship_size):
                            cur_map_space.append(self._boats[starting_y + i][starting_x])
                        if all(num + 1 not in cur_map_space for num in range(4)):
                            for i in range(ship_size):
                                self._boats[starting_y + i][starting_x] = ship_size
                                self._display[starting_y + i][starting_x] = SYMBOLS['target']
                            break
                        else:
                            continue
       


cp1 = ComputerPlayer()
cp2 = ComputerPlayer()
round = 1
while cp1.dead() == False and cp2.dead() == False:
    print(f"round {round}:")
    if round % 10 == 0:
        cp1.display_map()
    cp1.bomb(cp2)
    cp2.bomb(cp1)
    round += 1
    

if cp1.dead():
    print("computer 1 won")
else:
    print("computer 2 won")
