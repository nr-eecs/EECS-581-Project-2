# Program: player
# Description: This program is utilized by the game file in order to run Battleship.
# It focused on creating a lot of needed values for the game file, like the boards of ships and shots.
# It also checks the state of the game, with is_sunk, and is_all_sunk, as well as printing the board.
# Inputs: num_ships, ship_size, num 
# Outputs: board of ships, board of shots, Booleans determining status of sunk states, printed board, returned board
# Author: Del Endecott, Mick Torres
# Creation Date: 9/11/24

from typing import Literal, List
import random
import validifier as v

class Player:
    def __init__(self, num_ships: int, is_ai:bool = False, ai_difficulty:str = None):
        self.num_ships = num_ships
        self.is_ai = is_ai
        self.ai_difficulty = ai_difficulty

        # Medium AI difficulty logic: randomly fire shots, until a hit is reached. After this, fire shots (if legal) in a clockwise
        # manner starting from the top, advancing its reach by 1 with each round.
        # Special state variables for medium AI difficulty:
        self.ai_ship_found = False # has medium AI hit a ship
        self.ai_ship_found_square = (None, None) # square of hit
        self.orthogonal_direction = 0 # 0 -> Up, 1 -> Right, 2 -> Down, 3 -> Left
        self.advancement = 1
        
        # generate boards 
        self.ships = [[0 for _ in range(10)] for _ in range(10)]
        self.shots = [[0 for _ in range(10)] for _ in range(10)]
    
    def is_sunk(self, ship_size: int):
        x = 0
        for line in self.ships:
            x += line.count(ship_size)
        if x == 1:
            return True
        else:
            return False
        
    def is_all_sunk(self):
        if self.num_ships > 0:
            return False
        else:
            return True
    
    def return_board(self, num): # send board to game class
        if int(num) == 1: 
            return self.ships
        else:
            return self.shots 
        
    def print_board(self):

        output_str_list = []
        string_limit = 40

        coords = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        num_string = '    1  2  3  4  5  6  7  8  9  10'
        
        output_str_list.append(("         YOUR SHIPS", "        YOUR SHOTS"))
        output_str_list.append((num_string, num_string))

        for i, row in enumerate(self.ships):
            ships_str = coords[i] +  '   ' + '  '.join(map(str, row))
            shots_str = coords[i] +  '   ' + '  '.join(map(str, self.shots[i]))
            output_str_list.append((ships_str, shots_str))
        
       # print("\n".join(["   |   ".join(k) for k in output_str_list]))
        for str1, str2 in output_str_list:
            str1 += " " * (string_limit - len(str1))
            print(str1 + "|   " + str2)

        print('\n-----------------------------------------------------------------------------\n')
    
    '''
    General update strategy function for AI opponents after each turn based on the feedback of the shot
    In reality, this is only used for the medium AI difficulty
    If a random shot by the medium difficulty was a hit, we need to start hitting orthogonally adjacent tiles
    '''
    def update_strategy(self, shot, x, y):
        if self.ai_difficulty == "M":
            if not self.ai_ship_found and shot == "You hit a ship!":
                self.ai_ship_found = True
                self.ai_ship_found_square = (x,y)
            if self.ai_ship_found and shot == "You sunk a ship!":
                self.ai_ship_found = False
                self.ai_ship_found_square = (None, None)
                self.advancement = 1
                self.orthogonal_direction = 0
    
    '''
    Handles deriving the next shot placement for AI difficulties, as well as the next shot placement or stats-related commands for
    human players. This includes the "P" command to view individual player stats, as well as the "S" command to display the scoreboard
    for both players
    '''
    def get_shot_placement(self, target=None):

        if self.is_ai:
            if self.ai_difficulty == "E":
                '''
                Easy difficulty algorithm:
                Simply choose a random row and column (if it has been hit before, outer game logic will rerun this function)
                '''
                x = random.randint(0,9)
                y = random.randint(0,9)
            elif self.ai_difficulty == "M":
                '''
                Medium difficulty algorithm:
                If we haven't gotten a hit, continue firing randomly
                Otherwise, move clockwise around the hit square, starting from the top and spiralling outward with each shot.
                We check for tile legality (within range and not hit before) before deciding on the next shot in this case
                '''
                if not self.ai_ship_found:
                    x = random.randint(0,9)
                    y = random.randint(0,9)
                    
                    # for debugging medium difficulty, let it find a ship tile with certainty
                    # found_ship = False
                    # x,y = (None, None)
                    # for i, row in enumerate(target.ships):
                    #     for j, col in enumerate(row):
                    #         if type(col) == int and col > 0:
                    #             x, y = i, j
                    #             found_ship = True
                    #             break
                    #     if found_ship:
                    #         break
                else:
                    found_legal_square = False
                    
                    while not found_legal_square:
                        x, y = self.ai_ship_found_square
                        if self.orthogonal_direction == 0: 
                            x -= self.advancement
                        elif self.orthogonal_direction == 1:
                            y += self.advancement
                        elif self.orthogonal_direction == 2:
                            x += self.advancement
                        elif self.orthogonal_direction == 3:
                            y -= self.advancement
                        if v.is_valid_shot(x, y) and self.shots[x][y] not in ("X", "M", "S"):
                            found_legal_square = True
                        else:
                            if self.orthogonal_direction == 3:
                                self.advancement += 1
                            self.orthogonal_direction = (self.orthogonal_direction + 1) % 4
            elif self.ai_difficulty == "H":
                '''
                Hard difficulty algorithm:
                Find first non-hit ship tile and target it
                '''
                found_ship = False
                x,y = (None, None)
                for i, row in enumerate(target.ships):
                    for j, col in enumerate(row):
                        if type(col) == int and col > 0:
                            x, y = i, j
                            found_ship = True
                            break
                    if found_ship:
                        break
        else:
            turn_input = input("Input the square you want to shoot (e.g., A6), or (P)layer Stats, or (S)coreboard: ")
            

            if turn_input in ("P", "S"):
                return turn_input

            try:
                x = ord(turn_input[0].upper()) - ord('A')  # converts characters to numbers
                y = int(turn_input[1:]) - 1         # subtracts 1 due to 0-indexed
            except:
                raise Exception("Please pay attention to coordinate input formatting")

        return (x, y)
    
    def get_stats(self):
        '''
        Stats calculation function used by both view_stats and display_scoreboard
        Gets total successful shots FROM the player, total ships destroyed BY the player,
        and total hits taken RECEIVED by the player
        '''

        success_shots = 0
        total_ships_destroyed = 0
        total_hits_taken = 0

        for row in self.shots:
            for col in row:
                if col in ("S", "X"):
                    success_shots += 1
                if col == "S":
                    total_ships_destroyed += 1

        for row in self.ships:
            for col in row:
                if col in ("S", "X"):
                    total_hits_taken += 1
        
        return success_shots, total_ships_destroyed, total_hits_taken

    
    def view_stats(self):
        '''
        Uses get_stats to print player stats correspondingly
        '''

        success_shots, total_ships_destroyed, total_hits_taken = self.get_stats()

        print()
        print("Total Successful Shots:", success_shots)
        print("Total Opponent's Ships Destroyed:", total_ships_destroyed)
        print("Total Hits Taken:", total_hits_taken)
        print()
        
    