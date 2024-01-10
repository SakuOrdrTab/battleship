'''Python script game for traditional "Battleship" '''
# Version 1.1

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
    ''' A Class describing a human player'''  
    def __init__(self) -> None:
        # _display is a private variable for just displaying the game
        self._display = [[SYMBOLS["sea"] for i in range(10)] for j in range(10)]
        # _boats is the private variable for holding the remaining boats. Needs to be separate from display
        self._boats = [[SYMBOLS["sea"] for i in range(10)] for j in range(10)]
        # self.get_starting_positions
        self.get_automatic_starting_positions()

    def display_map(self) -> None:
        print("   ABCDEFGHIJ")
        row_count = 0
        for row in self._display:
            row_count += 1
            print(f"{row_count:2} ", end="")
            for item in row:
                print(item, end="")
            print()

    @classmethod
    def _get_coords(cls, prompt : str) -> tuple:
        '''A helper class method to validate coordinate input'''
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
    
    def get_starting_positions(self) -> None:
        '''Get starting positions for ships'''
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

    def get_automatic_starting_positions(self) -> None:
        ''' A copy from computer players random starting positions to speed up testing process'''
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
                            break 
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

    def bomb(self, another_player : "Player") -> None:
        '''a human player bombs another player'''
        print("")
        x, y = Player._get_coords("Give coordinates for bombing (X Y): ")
        if another_player._boats[y][x] in [x+1 for x in range(4)]:
            print(f"A HIT! A {list(SYMBOLS.keys())[list(SYMBOLS.values()).index(another_player._boats[y][x])]} was hit")
            self._display[y][x] = SYMBOLS["hit"]
            another_player._boats[y][x] += 10
            another_player._display[y][x] = SYMBOLS["destroyed_target"]
            if self.is_sunk(another_player, x, y, another_player._boats[y][x]-10):
                print(f"A {list(SYMBOLS.keys())[list(SYMBOLS.values()).index(another_player._boats[y][x]-10)]} was SUNK!")
        else:
            print("A miss.")
            self._display[y][x] = SYMBOLS["miss"]
    
    def is_sunk(self, another_player : "Player", x : int, y : int, ship_type = int):
        '''Method checks whether a ship was sunk. Not completely foolproof for all ship placements!'''
        if ship_type == 1:
            return True # A submarine is of course sunk
        else:
            # a helper func
            def shrink(subject : list, to_keep : int) -> list:
                if subject == []:
                    return []
                elif len(subject) == 1:
                    return subject[0] if subject[0] in [to_keep, to_keep + 10] else []
                else:
                    if subject[0] not in [to_keep, to_keep + 10]:
                        return shrink(subject[1:], to_keep)
                    elif subject[-1] not in [to_keep, to_keep + 10]:
                        return shrink(subject[:-1], to_keep)
                    else:
                        return subject
            # test horizontal first, take corresponding row
            test_row = another_player._boats[y].copy()
            # maximum needed list to test is x +/- ship length
            max_test_list = [test_row[_y] for _y in range(x - ship_type + 1, x + ship_type) if _y >= 0 and _y < 10]
            # shrink 
            to_test = shrink(max_test_list, ship_type)
            # go through the list if size > ship_type
            if type(to_test) == list:
                max_sunk = 0
                curr_sunk = 0
                for item in to_test:
                    if type(item) == int:
                        if item == ship_type + 10:
                            curr_sunk += 1
                    else:
                        curr_sunk = 0
                    if curr_sunk > max_sunk:
                        max_sunk = curr_sunk
                if max_sunk >= ship_type:
                    return True
            # test column
            test_column = [another_player._boats[x][s] for s in range(10)] # a new list, not a ref
            to_test = shrink([test_column[_x] for _x in range(y - ship_type + 1, y + ship_type) if _x >= 0 and _x < 10], ship_type)
            if type(to_test) == list:
                max_sunk = 0
                curr_sunk = 0
                for item in to_test:
                    if type(item) == int:
                        if item == ship_type + 10:
                            curr_sunk += 1
                    else:
                        curr_sunk = 0
                    if curr_sunk > max_sunk:
                        max_sunk = curr_sunk
                if max_sunk >= ship_type:
                    return True
            return False

    def dead(self) -> bool:
        '''Return True if the player has no ships left'''
        return not any(num in [1, 2, 3, 4] for row in self._boats for num in row)

class ComputerPlayer(Player):
    '''a class for computer players, inherits player class'''
    def __init__(self):
        super().__init__()
        self._hits = [] # tuple (y, x)

    def _check_bombing(self, another_player : Player, x : int, y : int) -> None:
        if another_player._boats[y][x] in [x+1 for x in range(4)]:
            print(f"Computer HITS a target! A {list(SYMBOLS.keys())[list(SYMBOLS.values()).index(another_player._boats[y][x])]} was hit")
            if another_player._boats[y][x] in [x+2 for x in range(3)]: # if not submarine, add to hits
                self._hits.append((y, x))
            self._display[y][x] = SYMBOLS["hit"]
            another_player._boats[y][x] += 10
            another_player._display[y][x] = SYMBOLS["destroyed_target"]
            if self.is_sunk(another_player, x, y, another_player._boats[y][x]-10):
                print(f"A {list(SYMBOLS.keys())[list(SYMBOLS.values()).index(another_player._boats[y][x]-10)]} was SUNK!")
        else:
            print("Computer missed.")
            self._display[y][x] = SYMBOLS["miss"]

    def bomb(self, another_player : Player) -> None:
        '''computer player bombs another player, overrides superclass method'''
        print()
        print("Computer is bombing")
        # "Target mode", if previous hits warrant bombing adjacent coords
        for y, x in self._hits:
            for x_offset in range(-1, 2, 2):
                if x + x_offset in range(10):
                    if self._display[y][x + x_offset] not in [SYMBOLS["miss"], SYMBOLS["hit"]]:
                        self._check_bombing(another_player, x + x_offset, y)
                        return
            for y_offset in range(-1, 2, 2):
                if y + y_offset in range(10):
                    if self._display[y + y_offset][x] not in [SYMBOLS["miss"], SYMBOLS["hit"]]:
                        self._check_bombing(another_player, x, y + y_offset)
                        return     
        # Hunting mode, just random bombing
        while True:
            x, y = randint(0, 9), randint(0, 9)
            if self._display[y][x] in [SYMBOLS["miss"], SYMBOLS["hit"]]:
                continue
            else:
                self._check_bombing(another_player, x, y)
                return 

    def get_starting_positions(self) -> None:
        '''computer player gets random starting positions, overrides superclass method'''
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
                            break 
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


def test_computer_players(number : int) -> None:
    '''Runs a <number> amount of computer vs computer games and prints some info'''
    round_list = []
    cp1_won = cp2_won = 0
    for i in range(number):
        cp1 = ComputerPlayer()
        cp2 = ComputerPlayer()
        round = 1
        while cp1.dead() == False and cp2.dead() == False:
            cp1.bomb(cp2)
            cp2.bomb(cp1)
            round += 1
        round_list.append(round)
        if cp1.dead():
            cp1_won += 1
        elif cp2.dead():
            cp2_won += 1
    print(f"The number of test games {number}, in which computer_player_1 won {cp1_won} and computer_player_2 {cp2_won}.")
    print(f"The average number of rounds was {sum(round_list)/number}")
    print(f"the maximum number of rounds was {max(round_list)} and minimum {min(round_list)}.")


if __name__ == "__main__":
    print("Welcome to classic Battleship game!")
    print()
    
    # test_computer_players(100)
    
    human_player = Player()
    computer_player = ComputerPlayer()
    while True:
        human_player.display_map()
        human_player.bomb(computer_player)
        computer_player.bomb(human_player)
        print()
        if human_player.dead():
            print("Human player LOST and computer won.")
            break
        elif computer_player.dead():
            print("Human player WON and computer lost. Congratulations!")
            break
    print()
    print("Thank you for playing.")