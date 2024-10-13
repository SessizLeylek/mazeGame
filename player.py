import particles
from gameManagement import *


class Player:
    def __init__(self, renderer, key_input, movement_call):
        """
        Player is controllable by user via keyboard inputs, main actor of gameplay
        :param renderer: GameRenderer object
        :param key_input: KeyboardState object
        :param movement_call: The method that will be called when the player moved
        """
        self._renderer = renderer
        self._key_input = key_input
        self._movement_call = movement_call

        self.level_data = []

        self.sprite = GameSprite(["turtle_right_0", "turtle_right_1", "turtle_down_0", "turtle_down_1", "turtle_left_0", "turtle_left_1", "turtle_up_0", "turtle_up_1"], 10, -256, -256)
        self._renderer.register_object(self.sprite)
        self._movement_route = []   # Route of the character, saved for interpolation of sprite

        self.pos_x = 0
        self.pos_y = 0

    def update(self, _loop_number):
        """
        The update is called every frame
        """
        if self._key_input.pressed_right:
            self._move_player(1, 0)
            self.sprite.frame = 1 - self.sprite.frame % 2

        if self._key_input.pressed_left:
            self._move_player(-1, 0)
            self.sprite.frame = 5 - self.sprite.frame % 2

        if self._key_input.pressed_up:
            self._move_player(0, 1)
            self.sprite.frame = 7 - self.sprite.frame % 2

        if self._key_input.pressed_down:
            self._move_player(0, -1)
            self.sprite.frame = 3 - self.sprite.frame % 2

        self._update_sprite_pos()
        self._renderer.offset_x = -max(min(self.sprite.pos_x, (len(self.level_data) - 11) * 64), 0)
        self._renderer.offset_y = -max(min(self.sprite.pos_y, (len(self.level_data[0]) - 11) * 64), 0)

    def _move_player(self, dx, dy):
        if self.level_data[self.pos_x + dx][self.pos_y + dy] != 1:
            self.pos_x += dx
            self.pos_y += dy
            self._movement_route.append([self.pos_x * 64 - 320, self.pos_y * 64 - 320, dx * 16, dy * 16, 4])

            if self._movement_call:
                self._movement_call()

    def _update_sprite_pos(self):
        # Interpolating the sprite position
        if self._movement_route:
            particles.DustParticles(self._renderer, self.sprite.pos_x + random.randint(-16, 16),
                                    self.sprite.pos_y + random.randint(-16, 16))

            step = 1 if len(self._movement_route) < 3 else 2
            self._movement_route[0][4] -= step
            self.sprite.pos_x = self._movement_route[0][0] - self._movement_route[0][2] * self._movement_route[0][4] * step
            self.sprite.pos_y = self._movement_route[0][1] - self._movement_route[0][3] * self._movement_route[0][4] * step

            if self._movement_route[0][4] < 1:
                self._movement_route.pop(0)
