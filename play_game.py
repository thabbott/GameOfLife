from GameOfLife import *

output_frames = True

fname1 = "Messi"
fname2 = "Mothership"

import sys
ARGS = sys.argv[1:]
if len(ARGS) > 0:
    if len(ARGS) == 2:
        fname1 = ARGS[0]
        fname2 = ARGS[1]
    else:
        print("Requires exactly two entry filenames as arguments or zero, in which case it defaults to hard-coded values.")
        sys.exit()

game = GameOfLife(100, 100, 1000)

try:
    game.read_state_from_file(f"entries/{fname1}", red = True)
    game.read_state_from_file(f"entries/{fname2}", red = False)
except:
    print(f"Input files {fname1} and/or {fname2} not found.")    
game.update_display()
input("Press enter to continue")

while True:
    for _ in range(3):
        game.evolve()
        if game.red_has_won():
            game.update_display()
            game.display_result("red")
            input("Press enter to continue")
            exit()
        if game.black_has_won():
            game.update_display()
            game.display_result("black")
            input("Press enter to continue")
            exit()
        if game.tiebreaker_needed():
            game.update_display()
            game.display_result("tie")
            input("Press enter to continue")
            break
    game.update_display()
    if output_frames:
        game.save_display()


game.t = game.T
while True:
    game.seed_random_cells()
    game.evolve()
    game.update_display()
    if game.red_has_won():
        game.display_result("red")
        input("Press enter to continue")
        exit()
    if game.black_has_won():
        game.display_result("black")
        input("Press enter to continue")
        exit()
