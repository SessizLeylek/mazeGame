from gameManagement import *


class Shrimp:
    def __init__(self, renderer, pos_x, pos_y):
        """
        Bell is a collectable that increases the score when collected
        :param renderer: GameRenderer object
        :param pos_x: X position of the bell
        :param pos_y: Y position of the bell
        """
        self._renderer = renderer

        self._sprite = GameSprite(["shrimp_0", "shrimp_1", "shrimp_2", "shrimp_3", "shrimp_4",
                                   "shrimp_5", "shrimp_6", "shrimp_7", "shrimp_8", "shrimp_9",
                                   "shrimp_10", "shrimp_11"], 9, pos_x * 64 - 320, pos_y * 64 - 320)
        self._renderer.register_object(self._sprite)
        self._renderer.sort_sprites_by_layer()

        self._renderer.register_method(self._animation_update)

        self.score_value = 0

    def _animation_update(self, _loop_number):
        # Changes the animation frame every 5th frame
        if _loop_number % 5 == 0:
            if self._sprite.frame < 11:
                self._sprite.frame += 1
            else:
                self._sprite.frame = 0

    def destroy_yourself(self):
        self._renderer.unregister_method(self._animation_update)
        self._renderer.unregister_object(self._sprite)
