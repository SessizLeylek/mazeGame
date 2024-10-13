from gameManagement import *


class BaseParticle:
    def __init__(self, renderer, pos_x, pos_y, layer, vfx_sprites):
        self._renderer = renderer
        self.speed = 1

        self._sprite = GameSprite(vfx_sprites, layer, pos_x, pos_y)
        self._renderer.register_object(self._sprite)
        self._renderer.register_method(self._particle_update)
        self._renderer.sort_sprites_by_layer()

    def _particle_update(self, _loop_number):
        if _loop_number % self.speed == 0:
            if self._sprite.frame < len(self._sprite.sprites) - 1:
                self._sprite.frame += 1
            else:
                self._renderer.unregister_object(self._sprite)
                self._renderer.unregister_method(self._particle_update)


class ShrimpParticles(BaseParticle):
    def __init__(self, renderer, pos_x, pos_y):
        super().__init__(renderer, pos_x, pos_y, 11, ["vfx_bell_0", "vfx_bell_1", "vfx_bell_2",
                                                      "vfx_bell_3", "vfx_bell_4", "vfx_bell_5"])
        self.speed = 2


class DustParticles(BaseParticle):
    def __init__(self, renderer, pos_x, pos_y):
        super().__init__(renderer, pos_x, pos_y, 9, ["vfx_dust_0", "vfx_dust_1", "vfx_dust_2", "vfx_dust_3"])
        self.speed = 3


class StarParticles(BaseParticle):
    def __init__(self, renderer, pos_x, pos_y):
        super().__init__(renderer, pos_x, pos_y, 9, ["vfx_star_0", "vfx_star_1", "vfx_star_2",
                                                     "vfx_star_3", "vfx_star_4"])
        self.speed = 3
