from GameOfLife import *

game = GameOfLife(100, 100, 1000)
game.read_state_from_file("Ronaldo", red = True)
game.read_state_from_file("Messi", red = False)
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
