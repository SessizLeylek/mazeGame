import math
import turtle
import random


class GameSprite:
    def __init__(self, sprites, sorting_layer, pos_x, pos_y):
        """
        A 2D texture that is going to be rendered on the screen
        :param sprites: List of names of sprites
        :param sorting_layer: Determines its sorting relative to the other sprites, higher the closer
        :param pos_x: X position of sprite
        :param pos_y: Y position of sprite
        """
        self.sprites = sprites
        self.frame = 0
        self.layer = sorting_layer
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.hidden = False
        self.alwaysDraw = False

        existing_shapes = turtle.getshapes()
        for i in range(len(sprites)):
            sprites[i] = "data/" + sprites[i] + ".gif"
            if sprites[i] not in existing_shapes:
                turtle.register_shape(sprites[i])


class UiText:
    def __init__(self, text_content, text_color, text_font, text_size, text_style, text_align, pos_x, pos_y):
        """
        Text object that is going to be rendered on the screen
        :param text_content: Content of text
        :param text_color: Color of text
        :param text_font: Font of text
        :param text_size: Size of font
        :param text_style: Style of font: normal, bold, italic or bold italic
        :param text_align: Alignment of text: left, right or center
        :param pos_x: X position of text
        :param pos_y: Y position of text
        """
        self.content = text_content
        self.color = text_color
        self.font = text_font
        self.size = text_size
        self.style = text_style
        self.align = text_align
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.hidden = False


class GameRenderer:
    def __init__(self, screen_width, screen_height):
        """
        Renders the game with 50 fps
        :param screen_width: Width of the screen
        :param screen_height: Height of the screen
        """
        # Setting up the screen
        self._screen = turtle.Screen()
        self._screen.setup(640, 640, None, None)
        self._screen.title("Caretta the Labyrinth Explorer")
        self._screen._root.resizable(False, False)
        self._screen._root.iconbitmap("data/game_icon.ico")

        # Setting up the turtle
        self._turtleObject = turtle.Turtle()
        self._turtleObject.hideturtle()
        self._turtleObject.penup()
        self._screen.tracer(0, 0)

        # Defining lists
        self._gameSprites = []
        self._uiTexts = []
        self._loopMethods = []

        self._loop_number = 0

        self.offset_x = 0
        self.offset_y = 0
        self.show_transition = True
        self.transition_radius = 0

        self._render_loop()

    def _render_loop(self):
        # Clears the screen before the drawing
        self._turtleObject.clear()

        # Calls every loop methods
        for m in self._loopMethods:
            m(self._loop_number)

        # Draws all the sprites in the list
        for sprite in self._gameSprites:
            sprite_visible = sprite.alwaysDraw or \
                             (abs(sprite.pos_x + self.offset_x) < 360 and abs(sprite.pos_y + self.offset_y) < 360)
            if not sprite.hidden and sprite_visible:
                self._turtleObject.shape(sprite.sprites[sprite.frame])
                self._turtleObject.setposition(sprite.pos_x + self.offset_x, sprite.pos_y + self.offset_y)
                self._turtleObject.stamp()

        # Writes all the sprites in the list
        for text in self._uiTexts:
            if not text.hidden:
                self._turtleObject.pencolor(text.color)
                self._turtleObject.setposition(text.pos_x, text.pos_y)
                self._turtleObject.write(text.content, False, text.align, (text.font, text.size, text.style))

        # Draws a black screen with a circular hole in it for transitions
        if self.show_transition:
            self._turtleObject.pensize(64)
            self._turtleObject.pencolor("black")
            for lyr in range((self.transition_radius + 32) // 15, 61):
                self._turtleObject.setposition(64 * lyr, 0)
                self._turtleObject.pendown()
                for t in range(21):
                    self._turtleObject.setposition(math.cos(math.pi * t / 10) * 15 * lyr,
                                                   math.sin(math.pi * t / 10) * 15 * lyr)
                self._turtleObject.penup()

        self._loop_number += 1

        # This function is called again after 20 ms
        self._screen.ontimer(self._render_loop, 20)

    def keep_window_open(self):
        """
        Prevents screen from closing. Put this at the end of the script
        """
        self._screen.mainloop()

    def register_method(self, method):
        """
        Adds a method to list so every frame it wil be called before rendering
        :param method: Method to be registered
        """
        self._loopMethods.append(method)

    def unregister_method(self, method):
        """
        Deletes the method from the list
        :param method: Method that will no longer be called
        """
        if method in self._loopMethods:
            self._loopMethods.remove(method)

    def register_object(self, obj):
        """
        Adds object to the rendering list
        :param obj: GameSprite or UiText
        """
        if isinstance(obj, GameSprite):
            self._gameSprites.append(obj)
        elif isinstance(obj, UiText):
            self._uiTexts.append(obj)
        else:
            raise ValueError(f"Registered object is {obj} must be a GameSprite or UiText")

    def unregister_object(self, obj):
        """
        Removes object from the rendering list
        :param obj: GameSprite or UiText
        """
        if obj in self._gameSprites:
            self._gameSprites.remove(obj)
        elif obj in self._uiTexts:
            self._uiTexts.remove(obj)

    def sort_sprites_by_layer(self):
        """
        Sorts sprites by their sorting layer. As the layer value increases, sprite comes forward
        """
        self._gameSprites = sorted(self._gameSprites, key=lambda x: x.layer)

    def change_bg_color(self, new_color):
        """
        Changes background color
        :param new_color: New color to be applied on background
        """
        self._screen.bgcolor(new_color)

    def get_text_input(self, title, text):
        return self._screen.textinput(title, text)


class SceneTransition:
    def __init__(self, renderer):
        self._renderer = renderer
        self._exit_methods = []

    def _increase_transition_rad(self):
        self._renderer.transition_radius += self._renderer.transition_radius // 20 + 15
        if self._renderer.transition_radius >= 906:
            self._renderer.show_transition = False
        else:
            turtle.ontimer(self._increase_transition_rad, 20)

    def _decrease_transition_rad(self):
        self._renderer.transition_radius -= self._renderer.transition_radius // 20 + 15
        if self._renderer.transition_radius <= 0:
            self._renderer.show_transition = False
            for m in self._exit_methods:
                m()
        else:
            turtle.ontimer(self._decrease_transition_rad, 20)

    def entrance_transition(self):
        self._renderer.transition_radius = 0
        self._renderer.show_transition = True
        self._increase_transition_rad()

    def exit_transition(self, *methods):
        self._renderer.transition_radius = 906
        self._renderer.show_transition = True
        self._decrease_transition_rad()
        for m in methods:
            self._exit_methods.append(m)


class KeyboardState:
    def __init__(self):
        """
        Allows you to get buttons pressed in the last frame
        """
        self.pressed_up = False
        self.pressed_down = False
        self.pressed_right = False
        self.pressed_left = False
        self.pressed_enter = False

        turtle.onkey(self._up_pressed, "Up")
        turtle.onkey(self._down_pressed, "Down")
        turtle.onkey(self._right_pressed, "Right")
        turtle.onkey(self._left_pressed, "Left")
        turtle.onkey(self._enter_pressed, "Return")

        turtle.listen()

    def _up_pressed(self, *args):
        self.pressed_up = True
        turtle.ontimer(self._reset_pressed_keys, 20)

    def _down_pressed(self, *args):
        self.pressed_down = True
        turtle.ontimer(self._reset_pressed_keys, 20)

    def _right_pressed(self, *args):
        self.pressed_right = True
        turtle.ontimer(self._reset_pressed_keys, 20)

    def _left_pressed(self, *args):
        self.pressed_left = True
        turtle.ontimer(self._reset_pressed_keys, 20)

    def _enter_pressed(self, *args):
        self.pressed_enter = True
        turtle.ontimer(self._reset_pressed_keys, 20)

    def _reset_pressed_keys(self):
        self.pressed_up = False
        self.pressed_down = False
        self.pressed_right = False
        self.pressed_left = False
        self.pressed_enter = False


class Scoreboard:
    def __init__(self):
        """
        Scoreboard saves and show the high scores in (name, score) format
        """
        data_readable = open("data/scoredata", "r")

        read_data = data_readable.read().split("\n")
        names = list(map(lambda x: x, read_data[0::2]))
        scores = list(map(lambda x: int(x), read_data[1::2]))
        bool_list = [False for i in range(len(scores))]
        self._scoreboard = list(zip(names, scores, bool_list))

    def get_scores(self):
        return self._scoreboard

    def add_score(self, name, score):
        name = "".join(filter(lambda x: ord(x) > 31, name))  # Removing unreadable characters from the name
        self._scoreboard.append((name, score, True))  # 3rd bool indicates that this element is added recently
        self._scoreboard.sort(key=lambda x: x[1], reverse=True)

    def update_score_data(self):
        while len(self._scoreboard) > 7:
            self._scoreboard.pop(-1)

        names = list(map(lambda x: x[0], self._scoreboard))
        scores = list(map(lambda x: x[1], self._scoreboard))
        final_text = "\n".join(map(lambda x: f"{x[0]}\n{x[1]}", zip(names, scores)))

        data_writable = open("data/scoredata", "w", encoding="utf-8")
        data_writable.write(final_text)
