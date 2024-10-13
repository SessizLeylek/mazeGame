import math
from player import Player
from gameManagement import *
import collectable
import particles
import random


class Game:
    def __init__(self, renderer, keyboard_input, win_method, lose_method):
        """
        Creates a game that contains elements of gameplay like player and level
        :param renderer: GameRenderer object
        :param keyboard_input: KeyboardInput object
        :param win_method: The method that will be called if the player manages to collect all shrimps
        :param lose_method: The method that will be called if the player runs out of time
        """
        self._level = []
        self._game_variables = []
        self._renderer = renderer
        self._win_method = win_method
        self._lose_method = lose_method

        self._player = Player(renderer, keyboard_input, self._player_moved)
        self._player.sprite.hidden = True

        self._tiles = []

        self._frames_since_collection = 0
        self._shrimp_creation_range = 0
        self.shrimp = None

        self._transition_in_progress = False
        SceneTransition(self._renderer).entrance_transition()

    def initialize_game(self, variables):

        self._player.pos_x = variables[0] * 6 - 1
        self._player.pos_y = variables[0] * 6 - 1
        self._player.sprite.pos_x = variables[0] * 384 - 384
        self._player.sprite.pos_y = variables[0] * 384 - 384
        self._player.sprite.hidden = False
        self._renderer.register_method(self._player.update)
        self._renderer.sort_sprites_by_layer()

        self._game_variables = variables

        self._create_ui()
        self._renderer.register_method(self._update_ui_texts)

        self._shrimp_creation_range = (2 + variables[0]) * 30
        self._create_shrimp()

    def _create_ui(self):
        self._ui_level = UiText(f"Level {self._game_variables[0]}/3", "#000000", "Times New Roman",
                                24, "normal", "left", -310, 280)
        self._ui_time = UiText(f"{self._game_variables[1]}", "#000000", "Times New Roman", 24, "normal", "center", 0, 280)
        self._ui_score = UiText(f"Score: {self._game_variables[2]}", "#000000", "Times New Roman", 24, "normal", "right", 310, 280)

        self._renderer.register_object(self._ui_level)
        self._renderer.register_object(self._ui_time)
        self._renderer.register_object(self._ui_score)

    def _update_ui_texts(self, _loop_number):
        terminate_the_level = False
        if self._game_variables[1] > 0:
            self._game_variables[1] -= 1
        else:
            terminate_the_level = True

        self._ui_time.content = f"{str(self._game_variables[1] // 25)}.{self._game_variables[1] % 25 * 4}"
        self._ui_score.content = f"Score: {self._game_variables[2]}/{60 * (self._game_variables[0] + 5) * self._game_variables[0]}"

        # When time is running out, the text flashes red and black
        if self._game_variables[1] < 500:
            self._ui_time.color = "#FF001A" if _loop_number % 20 < 10 else "#000000"

        # The text becomes yellow for a moment when a shrimp is collected
        if self._frames_since_collection > 0:
            self._ui_score.color = "#" + str(hex(236 * self._frames_since_collection // 20 + 19)).split("x")[1] \
                                   + str(hex(210 * self._frames_since_collection // 20 + 19)).split("x")[1] + "00"
            self._frames_since_collection -= 1
        else:
            self._ui_score.color = "#000000"

        if terminate_the_level and not self._transition_in_progress:
            self._transition_in_progress = True
            self._renderer.unregister_method(self._update_ui_texts)
            SceneTransition(self._renderer).exit_transition(self._terminate_level, self._lose_method)

    def generate_level(self, level_width, level_height):
        """
        Generates a randomly generated level
        :param level_width: Number of units in width
        :param level_height: Number of units in height
        """
        # Creating a grill shape
        for x in range(level_width):
            level_column = []
            for y in range(level_height):
                tile_index = 1 if (y % 2 == 0 or x % 2 == 0) else 3  # 1: wall 0: accessible empty 3: inaccessible empty
                if x == 1 and y == 1:
                    tile_index = 0
                level_column.append(tile_index)
            self._level.append(level_column)

        # Editing the level until the every corner of the level is accessible
        number_of_inaccessible = 99
        while number_of_inaccessible > 0:
            # Saving the coordinates of the walls that are between an accessible and inaccessible tile
            walls_to_be_destroyed = []
            for tx in range(1, level_width):
                for ty in range(1, level_height):
                    if (tx + ty) % 2 == 1:
                        if self._return_tile_at(tx + 1, ty) + self._return_tile_at(tx - 1, ty) == 3 \
                                or self._return_tile_at(tx, ty + 1) + self._return_tile_at(tx, ty - 1) == 3:
                            walls_to_be_destroyed.append((tx, ty))

            # Deleting a random wall that is between an accessible and inaccessible tile
            if len(walls_to_be_destroyed) > 0:
                random_wall_pos = walls_to_be_destroyed[random.randint(0, len(walls_to_be_destroyed) - 1)]
                self._level[random_wall_pos[0]][random_wall_pos[1]] = 0
                if random_wall_pos[0] % 2 == 0:
                    self._level[random_wall_pos[0] + 1][random_wall_pos[1]] = 0
                    self._level[random_wall_pos[0] - 1][random_wall_pos[1]] = 0
                else:
                    self._level[random_wall_pos[0]][random_wall_pos[1] + 1] = 0
                    self._level[random_wall_pos[0]][random_wall_pos[1] - 1] = 0

            # Counting the inaccessible tiles, the loop continues if the count is not zero
            number_of_inaccessible = 0
            for tx in range(level_width):
                for ty in range(level_height):
                    number_of_inaccessible += 1 if self._level[tx][ty] == 3 else 0

        # Creating wall sprites
        for x in range(level_width):
            sprite_column = []
            for y in range(level_height):
                # Creating the sprite
                if self._level[x][y] == 1:
                    sprite_name = "tile_wall_" + str(self._return_tile_at(x, y + 1) + self._return_tile_at(x - 1, y)
                                                     * 2 + self._return_tile_at(x + 1, y)
                                                     * 8 + self._return_tile_at(x, y - 1) * 4)
                else:
                    sprite_name = "tile_water_" + str(random.randint(0, 1))

                sprite_column.append(GameSprite([sprite_name], -1, x * 64 - 320, y * 64 - 320))
                self._renderer.register_object(sprite_column[y])
            self._tiles.append(sprite_column)
        self._player.level_data = self._level

    def _create_shrimp(self):
        # Selecting a random but fair position for shrimp to spawn at
        shrimp_creation_map = list(map(lambda col: list(map(lambda x: -x, col)), self._level))
        latest_discoveries = [(self._player.pos_x, self._player.pos_y)]
        shrimp_creation_map[self._player.pos_x][self._player.pos_y] = 1
        highest_distance = 1
        while len(latest_discoveries) > 0:
            bx = latest_discoveries[0][0]
            by = latest_discoveries[0][1]
            if shrimp_creation_map[bx + 1][by] == 0:
                latest_discoveries.append((bx + 1, by))
                shrimp_creation_map[bx + 1][by] = shrimp_creation_map[bx][by] + 1
                if shrimp_creation_map[bx][by] + 1 > highest_distance:
                    highest_distance = shrimp_creation_map[bx][by] + 1
            if shrimp_creation_map[bx - 1][by] == 0:
                latest_discoveries.append((bx - 1, by))
                shrimp_creation_map[bx - 1][by] = shrimp_creation_map[bx][by] + 1
                if shrimp_creation_map[bx][by] + 1 > highest_distance:
                    highest_distance = shrimp_creation_map[bx][by] + 1
            if shrimp_creation_map[bx][by + 1] == 0:
                latest_discoveries.append((bx, by + 1))
                shrimp_creation_map[bx][by + 1] = shrimp_creation_map[bx][by] + 1
                if shrimp_creation_map[bx][by] + 1 > highest_distance:
                    highest_distance = shrimp_creation_map[bx][by] + 1
            if shrimp_creation_map[bx][by - 1] == 0:
                latest_discoveries.append((bx, by - 1))
                shrimp_creation_map[bx][by - 1] = shrimp_creation_map[bx][by] + 1
                if shrimp_creation_map[bx][by] + 1 > highest_distance:
                    highest_distance = shrimp_creation_map[bx][by] + 1
            latest_discoveries.pop(0)

        max_dist = min(highest_distance, self._shrimp_creation_range + 1)
        if max(2, max_dist // 2) < max_dist:
            desired_shrimp_distance = random.randint(max(2, max_dist // 2), max_dist)
        else:
            desired_shrimp_distance = 2
        for _x in range(len(shrimp_creation_map)):
            for _y in range(len(shrimp_creation_map)):
                if shrimp_creation_map[_x][_y] == desired_shrimp_distance:
                    self._shrimp_pos_x = _x
                    self._shrimp_pos_y = _y

        # Creating the collectable shrimp object
        self.shrimp = collectable.Shrimp(self._renderer, self._shrimp_pos_x, self._shrimp_pos_y)
        self.shrimp.score_value = (desired_shrimp_distance - 1) * 4

        self._shrimp_creation_range -= desired_shrimp_distance - 1

        # Creating particles
        particles_length = int(math.sqrt((self._shrimp_pos_x - self._player.pos_x) ** 2
                                         + (self._shrimp_pos_y - self._player.pos_y) ** 2) * 2)
        for t in range(particles_length):
            pos_x = random.randint(-16, 16) + (self._player.pos_x + (self._shrimp_pos_x - self._player.pos_x)
                                               * (t / particles_length)) * 64 - 320
            pos_y = random.randint(-16, 16) + (self._player.pos_y + (self._shrimp_pos_y - self._player.pos_y)
                                               * (t / particles_length)) * 64 - 320
            particles.StarParticles(self._renderer, pos_x, pos_y).speed = random.randint(3, 8)

    def _player_moved(self):
        if self._player.pos_x == self._shrimp_pos_x and self._player.pos_y == self._shrimp_pos_y:
            self._frames_since_collection = 20
            self._game_variables[2] += self.shrimp.score_value

            self.shrimp.destroy_yourself()
            self.shrimp = None

            particles.ShrimpParticles(self._renderer, self._shrimp_pos_x * 64 - 320, self._shrimp_pos_y * 64 - 320)

            if self._shrimp_creation_range > 0:
                self._create_shrimp()
            else:
                self._shrimp_pos_x = -1
                self._shrimp_pos_y = -1

                # Collecting all shrimps ends the level
                if not self._transition_in_progress:
                    self._transition_in_progress = True
                    self._renderer.unregister_method(self._update_ui_texts)
                    SceneTransition(self._renderer).exit_transition(self._terminate_level, self._win_method)

    def _return_tile_at(self, x, y):
        # Returns the tile number at x, y; if there is no tile returns 1
        if -1 < x < len(self._level) and -1 < y < len(self._level):
            return self._level[x][y]
        else:
            return 1

    def _terminate_level(self):
        # Unregistering objects and methods
        self._renderer.unregister_method(self._player.update)

        self._renderer.unregister_object(self._player.sprite)
        self._renderer.unregister_object(self._ui_level)
        self._renderer.unregister_object(self._ui_score)
        self._renderer.unregister_object(self._ui_time)
        for tiles_col in self._tiles:
            for t in tiles_col:
                self._renderer.unregister_object(t)

        if self.shrimp:
            self.shrimp.destroy_yourself()
