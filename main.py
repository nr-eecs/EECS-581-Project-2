# Program: main
# Description: This program implements the Game and Player classes from their respective files.
# This creates a 2-player battleship, letting players input coordinates to both place and sink ships.
# Inputs: # of ships, coordinates
# Outputs: game states via a 2D Array
# Author: Del Endecott, Ben Weinzirl
# Creation Date: 9/15/24

from game import Game

def main():
    game_on = True
    print("###  Welcome to Battleship!  ###")

    valid_player_count_input = False
    is_ai = False
    ai_difficulty = None

    while not valid_player_count_input:
        try:
            is_ai_int = int(input("Enter number of human players for game (1, 2): "))
            if is_ai_int not in (1,2):
                raise Exception("Invalid player count")
            valid_player_count_input = True
            if is_ai_int == 1: is_ai = True
        except ValueError:
            print("Invalid input. Please enter a valid integer (1 or 2).")
    
    if is_ai:
        valid_ai_difficulty_input = False
        while not valid_ai_difficulty_input:
            ai_difficulty = input("Enter Difficulty of AI - (E)asy, (M)edium, (H)ard: ").upper()
            if ai_difficulty in ("E", "M", "H"):
                valid_ai_difficulty_input = True
            else:
                print("Invalid AI difficulty, enter 'E' or 'M' or 'H'")
    valid_ship_count = False
    while not valid_ship_count:
        try:
            num = int(input("Enter number of ships (min = 1, max = 5): "))
            if 1 <= num <= 5:
                valid_ship_count = True
            else:
                print("You can only have 1 through 5 ships")
                
        except ValueError:
            print("Invalid input. Please enter a valid integer between 1 and 5.")
            
    
    # Initializes Game and Player classes
    G = Game(num, is_ai, ai_difficulty)
    P1 = G.get_P1()
    P2 = G.get_P2()
    
    # Establishes turn order
    order = [P1,P2]

    player = 1
    # For loop for placing ships for each player
    for p in order:
        ship_text = f"{num} ship{'s' if num > 1 else ''}"
        print(f'Player {player} must place {"all " if num > 1 else ""}{ship_text}{" starting from smallest" if num > 1 else ""}')
        print()
        player += 1
        for i in range(num):
            G.place_ship(p, i+1)
        if p.is_ai:
            print("AI has completed placing ships")
        print()

    print("🌟 ############ Game Start! ############ 🌟")
    print()
    # While loop for running the game until all of an opponents ships are sunk
    while game_on:
        player = 1
        for p in order:
            print(f"----------------------------🎯🔄 Player {player}'s turn 🔄🎯------------------------")
            p.print_board()
            G.turn(p, order[order.index(p)-1])
            if order[order.index(p)-1].is_all_sunk():
                game_on = False
                p.print_board()
                break
            player += 1

    
    print(f"🎉🏆 PLAYER {player} WINS! 🏆🎉")
    G.display_scoreboard()

main()
