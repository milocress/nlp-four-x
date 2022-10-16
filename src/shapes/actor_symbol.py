import math
from typing import Tuple

import pygame

from src.actor import Actor


class ActorSymbol:
    def __init__(self, surface, actor: Actor, radius: float, friendly: bool, simulation):
        self.radius = radius
        self.friendly = friendly
        self.actor = actor
        self.color = pygame.Color('blue')
        self.surface = surface

        hex = simulation.board.get_hex_from_feature(self.actor.position.static_position.parent_feature)

        self.center = (hex.centre[0], hex.centre[1])

    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        return math.dist(point, self.center) < self.radius

    def render(self, simulation):
        if self.actor.position.static_position:
            hex = simulation.board.get_hex_from_feature(self.actor.position.static_position.parent_feature)
            pygame.draw.circle(self.surface, self.color, (hex.centre[0], hex.centre[1]), 10)  # DRAW CIRCLE

    def get_actor(self):
        return self.actor
