from gameManagement import *


class ScoreboardScreen:
    def __init__(self, renderer, key_input, return_method, game_variables, player_succeed):
        self._renderer = renderer
        self._key_input = key_input
        self._return_method = return_method

        self._renderer.offset_x = 0
        self._renderer.offset_y = 0

        self._scoreboard_texts = []
        heading = UiText("You Win!" if player_succeed else "Time's Up!", "black", "Times New Roman", 32, "bold", "center", 0, 210)
        self._scoreboard_texts.append(heading)
        self._renderer.register_object(heading)
        heading = UiText(f"Your Score is {game_variables[2]}", "black", "Times New Roman", 24, "normal", "center", 0, 180)
        self._scoreboard_texts.append(heading)
        self._renderer.register_object(heading)

        self._wave = GameSprite(["mainmenu_wave"], 0, 0, 80)
        self._renderer.register_object(self._wave)
        self._background = GameSprite(["scoreboard_bg_0", "scoreboard_bg_1"], 0, 0, -160)
        self._renderer.register_object(self._background)

        SceneTransition(self._renderer).entrance_transition()

        sb = Scoreboard()

        ask_for_name = False
        if len(sb.get_scores()) < 7:
            ask_for_name = True
        elif game_variables[2] > sb.get_scores()[-1][1]:
            ask_for_name = True
        if ask_for_name:
            name = renderer.get_text_input("You Win!" if player_succeed else "Time's Up!", "Please Enter Your Name:")
            if name:
                sb.add_score(name, game_variables[2])
                sb.update_score_data()
        turtle.listen()

        scores = sb.get_scores()
        press_enter_text = UiText("Press Enter to Return", "black", "Times New Roman", 24, "italic", "center", 0, -210)
        press_enter_text.hidden = True
        self._scoreboard_texts.append(press_enter_text)
        self._renderer.register_object(press_enter_text)
        sb_title = UiText("Scoreboard", "black", "Times New Roman", 24, "bold", "center", 0, 90)
        self._scoreboard_texts.append(sb_title)
        self._renderer.register_object(sb_title)
        for score in scores:
            scr_text = UiText(f"{score[0]} : {score[1]}", "#FFE500" if score[2] else "black", "Times New Roman",
                              24, "normal", "center", 0, 180 - len(self._scoreboard_texts) * 30)
            self._scoreboard_texts.append(scr_text)
            self._renderer.register_object(scr_text)

        self._renderer.register_method(self._scoreboard_update)

        self._can_return = False
        turtle.ontimer(self._enable_returning, 500)

    def _scoreboard_update(self, _loop_number):
        self._wave.pos_x = (_loop_number % 64) * 2.5 - 80
        if _loop_number % 10 == 0:
            self._background.frame = 1 - self._background.frame

        if self._key_input.pressed_enter and self._can_return:
            self._key_input.pressed_enter = False
            self._can_return = False
            SceneTransition(self._renderer).exit_transition(self._terminate_scoreboard)

    def _enable_returning(self):
        self._can_return = True
        self._scoreboard_texts[2].hidden = False

    def _terminate_scoreboard(self):
        self._renderer.unregister_object(self._wave)
        self._renderer.unregister_object(self._background)
        self._renderer.unregister_method(self._scoreboard_update)

        for obj in self._scoreboard_texts:
            self._renderer.unregister_object(obj)

        self._return_method()
