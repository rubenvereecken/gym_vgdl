from vgdl.state import StateObserver, KeyValueObservation
import math


class AvatarOrientedObserver(StateObserver):

    def _get_distance(self, s1, s2):
        return math.hypot(s1.rect.x - s2.rect.x, s1.rect.y - s2.rect.y)


    def get_observation(self):
        avatars = self._game.getAvatars()
        assert avatars
        avatar = avatars[0]

        avatar_pos = self._rect_to_pos(avatar.rect)
        resources = [avatar.resources[r] for r in self._game.notable_resources]

        sprite_distances = []
        for key in self._game.sprite_registry.sprite_keys:
            dist = 100
            for s in self._game.getSprites(key):
                dist = min(self._get_distance(avatar, s)/self._game.block_size, dist)
            sprite_distances.append(dist)

        obs = KeyValueObservation(
            position=avatar_pos, speed=avatar.speed, resources=resources,
            distances=sprite_distances
        )
        return obs
