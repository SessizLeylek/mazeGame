from gameManagement import *
import mainMenu
import game
import scoreboard


def initialize_main_menu():
    reset_game_variables()
    renderer.offset_x = 0
    renderer.offset_y = 0
    main_menu = mainMenu.MainMenu(renderer, keyboardInput, start_new_game)


def start_new_game():
    level = game.Game(renderer, keyboardInput, level_completed, timer_run_out)
    level_size = 1 + 10 * game_variables[0]
    level.generate_level(level_size, level_size)
    level.initialize_game(game_variables)


def level_completed():
    if game_variables[0] < 3:
        game_variables[0] += 1
        game_variables[1] += 1000

        start_new_game()
    else:
        game_variables[2] += game_variables[1]
        show_scoreboard(True)


def timer_run_out():
    show_scoreboard(False)


def show_scoreboard(player_succeed):
    _scoreboard = scoreboard.ScoreboardScreen(renderer, keyboardInput, initialize_main_menu,
                                              game_variables, player_succeed)


def reset_game_variables():
    game_variables[0] = 1
    game_variables[1] = 1250
    game_variables[2] = 0


if __name__ == "__main__":
    renderer = GameRenderer(640, 640)
    keyboardInput = KeyboardState()

    game_variables = [1, 1250, 0]  # level number, remaining time (seconds * 25), score
    initialize_main_menu()

    renderer.keep_window_open()
    # Anything under this line will not work
