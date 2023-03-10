from field import *
#from GUI import *

gameField = GameField()
gameField.add_piece()

try:
    gameField.load_game()
except Exception as e:
    print("Unable to load saved game: " + str(e))

while True:
    print(gameField.status)
    if gameField.status == Status.LOSED:
        print("You lose! Try again.")
        break
    elif gameField.status == Status.WINNED:
        print("You winned!")
        break

    for x in range(4):
        for y in range(4):
            if gameField.field[x][y] is None:
                print("0\t", end="")
                continue
            print(str(gameField.field[x][y]) + "\t", end="")
        print()

    print(gameField.status)

    move = input("Write ur move (UP, DOWN, LEFT, RIGHT): ")
    move = move.upper()

    if move not in Directions.DIRECTIONS_DICT:
        print("You can not move like that!")
        continue

    is_changed = gameField.make_move(Directions.DIRECTIONS_DICT[move])
    if not is_changed:
        print("Never changes. Try again.")
    else:
        gameField.add_piece()
    
    print("Score is: " + str(gameField.get_score()))
    print("Best score is: " + str(gameField.get_best_score()))
    gameField.save_game()
