from gameManagement import *
from random import Random


class MainMenu:
    def __init__(self, renderer, key_input, start_game_method):
        """
        Creates and deals with the main menu sprites and buttons
        :param renderer: GameRenderer object
        :param key_input: KeyboardState object
        :param start_game_method: The method that will be called when the start game button is pressed
        """
        renderer.change_bg_color("#3FB2FF")

        self.renderer = renderer
        self.key_input = key_input
        self._registered_objects = []

        # Opening transition
        SceneTransition(self.renderer).entrance_transition()

        # Creating and registering objects
        self.game_title = GameSprite(["mainmenu_title"], 0, 0, 240)
        self._registered_objects.append(self.game_title)

        self.spr_beach = GameSprite(["mainmenu_beach"], 0, 0, -240)
        self._registered_objects.append(self.spr_beach)

        self.spr_wave0 = GameSprite(["mainmenu_wave"], -3, 0, -40)
        self._registered_objects.append(self.spr_wave0)

        self.spr_wave1 = GameSprite(["mainmenu_wave"], -2, 0, -80)
        self._registered_objects.append(self.spr_wave1)

        self.spr_wave2 = GameSprite(["mainmenu_wave"], -1, 0, -140)
        self._registered_objects.append(self.spr_wave2)

        self.spr_cloud0 = GameSprite(["mainmenu_cloud_0", "mainmenu_cloud_1", "mainmenu_cloud_2"], -4, -180, 240)
        self.spr_cloud0.alwaysDraw = True
        self._registered_objects.append(self.spr_cloud0)

        self.spr_cloud1 = GameSprite(["mainmenu_cloud_0", "mainmenu_cloud_1", "mainmenu_cloud_2"], -5, 180, 180)
        self.spr_cloud1.alwaysDraw = True
        self._registered_objects.append(self.spr_cloud1)

        sb = Scoreboard()
        scores = sb.get_scores()
        self._scoreboard_texts = []
        press_enter_text = UiText("Press Enter to Return", "black", "Times New Roman", 24, "italic", "center", 0, -150)
        self._scoreboard_texts.append(press_enter_text)
        self._registered_objects.append(press_enter_text)
        press_enter_text.hidden = True
        sb_title = UiText("Scoreboard", "black", "Times New Roman", 24, "bold", "center", 0, 120)
        self._scoreboard_texts.append(sb_title)
        self._registered_objects.append(sb_title)
        sb_title.hidden = True
        for score in scores:
            scr_text = UiText(f"{score[0]} : {score[1]}", "black", "Times New Roman",
                              24, "normal", "center", 0, 150 - len(self._scoreboard_texts) * 30)
            self._scoreboard_texts.append(scr_text)
            self._registered_objects.append(scr_text)
            scr_text.hidden = True

        self._credits0 = UiText("Credits", "black", "Times New Roman", 24, "bold", "center", 0, 120)
        self._credits1 = UiText("Programming", "black", "Times New Roman", 24, "normal", "center", 0, 60)
        self._credits2 = UiText("Kursat \"SessizLeylek\" Kuyumcu", "black", "Times New Roman", 24, "normal", "center", 0, 30)
        self._credits3 = UiText("Art", "black", "Times New Roman", 24, "normal", "center", 0, -30)
        self._credits4 = UiText("Kursat \"SessizLeylek\" Kuyumcu", "black", "Times New Roman", 24, "normal", "center", 0, -60)
        self._credits5 = UiText("Press Enter to Return", "black", "Times New Roman", 24, "italic", "center", 0, -150)
        self._registered_objects.append(self._credits0)
        self._registered_objects.append(self._credits1)
        self._registered_objects.append(self._credits2)
        self._registered_objects.append(self._credits3)
        self._registered_objects.append(self._credits4)
        self._registered_objects.append(self._credits5)
        self._credits0.hidden = True
        self._credits1.hidden = True
        self._credits2.hidden = True
        self._credits3.hidden = True
        self._credits4.hidden = True
        self._credits5.hidden = True

        self._selected_button = 0
        self._ui_interactable = True
        self._buttons_interactable = True
        self._button_play = UiText("< Start the Game >", "red", "Times New Roman", 32, "bold", "center", 0, 60)
        self._button_scores = UiText("Show the Scoreboard", "black", "Times New Roman", 32, "normal", "center", 0, 0)
        self._button_credits = UiText("Credits", "black", "Times New Roman", 32, "normal", "center", 0, -60)
        self._registered_objects.append(self._button_play)
        self._registered_objects.append(self._button_scores)
        self._registered_objects.append(self._button_credits)

        for o in self._registered_objects:
            renderer.register_object(o)
        renderer.sort_sprites_by_layer()

        # Registering methods
        renderer.register_method(self._background_animation)
        renderer.register_method(self._menu_loop)
        self._start_game_method = start_game_method

    def _menu_loop(self, loop_number):
        if self._ui_interactable:
            if self.key_input.pressed_up and self._buttons_interactable:
                self._selected_button += -1 if self._selected_button > 0 else 2
                self._highlight_selected_button(self._selected_button)

            if self.key_input.pressed_down and self._buttons_interactable:
                self._selected_button += 1 if self._selected_button < 2 else -2
                self._highlight_selected_button(self._selected_button)

            game_started = False
            # When user presses the start game button
            if self.key_input.pressed_enter and self._selected_button == 0 and self._buttons_interactable:
                self._ui_interactable = False
                game_started = True

            buttons_shown = False
            # Hide scoreboard and credits to show buttons
            if not self._buttons_interactable and self.key_input.pressed_enter:
                # Show buttons
                self._buttons_interactable = True
                self._button_play.hidden = False
                self._button_scores.hidden = False
                self._button_credits.hidden = False

                buttons_shown = True

                # Hide scoreboard and credits
                for scoreboard in self._scoreboard_texts:
                    scoreboard.hidden = True
                self._credits0.hidden = True
                self._credits1.hidden = True
                self._credits2.hidden = True
                self._credits3.hidden = True
                self._credits4.hidden = True
                self._credits5.hidden = True

            # When user presses the scoreboard button
            if self.key_input.pressed_enter and self._selected_button == 1 and self._buttons_interactable and not buttons_shown:
                # Buttons are hidden
                self._buttons_interactable = False
                self._button_play.hidden = True
                self._button_scores.hidden = True
                self._button_credits.hidden = True

                # Scoreboard is shown
                for scoreboard in self._scoreboard_texts:
                    scoreboard.hidden = False

            # When user presses the credits button
            if self.key_input.pressed_enter and self._selected_button == 2 and self._buttons_interactable and not buttons_shown:
                # Buttons are hidden
                self._buttons_interactable = False
                self._button_play.hidden = True
                self._button_scores.hidden = True
                self._button_credits.hidden = True

                # Scoreboard is shown
                self._credits0.hidden = False
                self._credits1.hidden = False
                self._credits2.hidden = False
                self._credits3.hidden = False
                self._credits4.hidden = False
                self._credits5.hidden = False

            if game_started:
                SceneTransition(self.renderer).exit_transition(self._terminate_main_menu)

    def _terminate_main_menu(self):
        # All objects and methods are unregistered
        for o in self._registered_objects:
            self.renderer.unregister_object(o)

        self.renderer.unregister_method(self._menu_loop)
        self.renderer.unregister_method(self._background_animation)

        self._start_game_method()

    def _highlight_selected_button(self, selected_button):
        # Highlights the selected buttons and removes highlights of the others

        if selected_button == 0:
            self._button_play.content = "< Start Game >"
            self._button_play.color = "#FF001A"
            self._button_play.style = "bold"
        else:
            self._button_play.content = "Start Game"
            self._button_play.color = "black"
            self._button_play.style = "normal"

        if selected_button == 1:
            self._button_scores.content = "< Show the Scoreboard >"
            self._button_scores.color = "#FF001A"
            self._button_scores.style = "bold"
        else:
            self._button_scores.content = "Show the Scoreboard"
            self._button_scores.color = "black"
            self._button_scores.style = "normal"

        if selected_button == 2:
            self._button_credits.content = "< Credits >"
            self._button_credits.color = "#FF001A"
            self._button_credits.style = "bold"
        else:
            self._button_credits.content = "Credits"
            self._button_credits.color = "black"
            self._button_credits.style = "normal"

    def _background_animation(self, loop_number):
        # Makes waves and clouds move
        self.spr_wave0.pos_x = (loop_number % 100) * 1.6 - 80
        self.spr_wave1.pos_x = (loop_number % 80) * -2 + 80
        self.spr_wave2.pos_x = (loop_number % 64) * 2.5 - 80

        self.spr_cloud0.pos_x += self.spr_cloud0.pos_y / 280 + 1
        self.spr_cloud1.pos_x += self.spr_cloud1.pos_y / 280 + 1

        rnd = Random()
        if self.spr_cloud0.pos_x > 440:
            self.spr_cloud0.pos_x = -440
            self.spr_cloud0.pos_y = rnd.random() * 280
            self.spr_cloud0.frame = rnd.randint(0, 2)
        if self.spr_cloud1.pos_x > 440:
            self.spr_cloud1.pos_x = -440
            self.spr_cloud1.pos_y = rnd.random() * 280
            self.spr_cloud1.frame = rnd.randint(0, 2)
