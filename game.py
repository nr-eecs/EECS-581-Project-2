# Program: game
# Description: This program utilizes the Player class, and the functions from validifier.
# It brings everything together in order to run a game of Battleship.
# The Game class manages player turns, ship placement, and shot processing.
# It handles input validation through validifier.
# Inputs: num, player, ship_size, row, col, ships, orientation, target, y, x, letter
# Outputs: player, num, game states via 2D Array, messages pertaining to the changes in game states
# Author: Del Endecott, Sam Harrison, Mick Torres
# Creation Date: 9/11/24
from typing import Literal, List

from player import Player
import random
import validifier as v

class Game:
    def __init__(self, num: int, is_ai: bool, ai_difficulty: str):
        self.P1 = Player(num)
        self.P2 = Player(num, is_ai, ai_difficulty)
        self.plies = 0
        # if is_ai:
        #     self.P2 = AIPlayer(num)
        # else:
        #     self.P2 = Player(num)
        
    def get_P1(self):
        return self.P1
    
    def get_P2(self):
        return self.P2
    
    def place_ship(self, player, ship_size: int):

        def letter_to_index(letter: str) -> int:
            return ord(letter.upper()) - ord('A')

        is_valid_placement = False
        if player.is_ai:
            while not is_valid_placement:
                orientation = random.choice(('H', 'V'))
                row = random.randint(0, 9) if orientation == 'H' else random.randint(0, 10 - ship_size)
                col = random.randint(0, 9) if orientation == 'V' else random.randint(0, 10 - ship_size)     
                is_valid_placement = v.is_valid_ship_placement(row, col, player.ships, ship_size, orientation)
            # debugging
            print(f"Placed ship on {row, col}")

        while not is_valid_placement:       
            position = input("Input the ship's top-leftmost position (e.g., A6): ").strip()
            try:
                row = letter_to_index(position[0])  # converts characters to numbers
                col = int(position[1:]) - 1         # subtracts 1 due to 0-indexed
            except:
                print("Invalid coordinate format. Please try again")
                continue
            
            orientation = input("Input the orientation of the ship (H or V): ").strip().upper()
            if orientation not in ("H", "V"):
                print("Orientation is invalid, must be H or V")
                continue
            
            try:
                is_valid_placement = v.is_valid_ship_placement(row, col, player.ships, ship_size, orientation)
            except:
                print("That format is invalid, please try again")
                continue
            if not is_valid_placement:
                print("Invalid ship placement, please try again")
        
        # the temp_board has the ships' sizes as identifiers of where they are placed
        if orientation == 'H':
        # places ship horizontally by changing line of cells
        # increases column index for length of ship
            for i in range(ship_size):
                player.ships[row][col + i] = ship_size 

        elif orientation == 'V':
            # places ship vertically by changing line of cells
            # increases row index for length of ship
            for i in range(ship_size):
                player.ships[row + i][col] = ship_size
        
        print(player.ships)

        
    def shot(self, player, target, y, x): # player = player being shot AT (x and y are swapped due to 2D array)
    # Checks if the square is valid, else it raises IndexError
        if v.is_valid_shot(x, y):
            # Saves the data of the square
            square = target.ships[x][y]
            # If the square is empty, it is a miss
            if square == 0:
                player.shots[x][y] = "M"
                return "missed!"
            # If the square has been hit before, raise IndexError
            elif player.shots[x][y] == 'X' or player.shots[x][y] == 'M' or player.shots[x][y] == "S":
                raise IndexError("Index picked before")
            # Otherwise, it is a hit
            else:
                # Checks if the ship is sunk
                if target.is_sunk(square):
                    target.num_ships -= 1
                    # Checks if all ships are sunk
                    if target.is_all_sunk():
                        player.shots[x][y] = "S"
                        return "Sunk all your opponent's ships!"
                    else:
                        player.shots[x][y] = "S"
                        return "You sunk a ship!"
                else:
                    player.shots[x][y] = "X"
                    target.ships[x][y] = "X"
                    return "You hit a ship!"
        else:
            raise IndexError("Index is not on the board")
        
    def display_scoreboard(self):
        s1, d1, h1 = self.P1.get_stats()
        s2, d2, h2 = self.P2.get_stats()

        p1_turns = self.plies // 2 + self.plies % 2
        p2_turns = self.plies // 2

        columns = ["Successful Shots", "Misses", "Ships Destroyed", "Accuracy", "Hit-To-Miss Ratio"]
        column_length = 20

        accuracy1 = "N/A" if p1_turns == 0 else str(round(s1 / p1_turns, 2))
        accuracy2 = "N/A" if p2_turns == 0 else str(round(s2 / p2_turns, 2))
        misses1 = str(p1_turns - s1)
        misses2 = str(p2_turns - s2)
        ratio1 = "N/A" if h1 == 0 else str(round(s1 / h1, 2))
        ratio2 = "N/A" if h2 == 0 else  str(round(s2 / h2, 2))
        destroyed1 = str(d1)
        destroyed2 = str(d2)
        success1 = str(s1)
        success2 = str(s2)

        player1_stats = (success1, misses1, destroyed1, accuracy1, ratio1)
        player2_stats = (success2, misses2, destroyed2, accuracy2, ratio2)

        print()
        print("=" * 49 + "SCOREBOARD" + "=" * 49)

        print(" " * 10, end="")
        for col in columns:
            spaces = (column_length - len(col)) // 2
            col = " " * spaces + col + " " * (column_length - len(col) - spaces)
            print(col, end="")
        print()

        print("Player 1  ", end="")
        for stat in player1_stats:
            spaces = (column_length - len(stat)) // 2
            stat = " " * spaces + stat + " " * (column_length - len(stat) - spaces)
            print(stat, end="")
        print()
        
        print("Player 2  ", end="")
        for stat in player2_stats:
            spaces = (column_length - len(stat)) // 2
            stat = " " * spaces + stat + " " * (column_length - len(stat) - spaces)
            print(stat, end="")
        print()
        print("=" * 108)

        if s1 > s2:
            print("Leading player: Player 1")
        elif s1 == s2:
            print("Leading Player: Tied")
        else:
            print("Leading Player: Player 2")
        print()
    
    def turn(self,player,target):

        valid_turn = False
        while not valid_turn:
            try:
                turn_input = player.get_shot_placement(target)
                if turn_input == "P":
                    player.view_stats()
                    continue
                elif turn_input == "S":
                    self.display_scoreboard()
                    continue
                else:
                    x, y = turn_input
            except Exception as e:
                print(e)
                continue
            
            #shot() method can raise an error with invalid input
            try:
                shot = self.shot(player, target, x, y)
                player.update_strategy(shot, x, y)
                print(shot)
            # Gives another chance to input proper coords if an error is raised
            except:
                print("Invalid shot, try again")
                continue
            valid_turn = True
            self.plies += 1