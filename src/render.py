from typing import List

import pygame

from src.nlp.nlp_actor import NLPActor
from src.shapes.actor_symbol import ActorSymbol
from src.simulation import Simulation



class Renderer:
    def __init__(self, simulation):
        self.game_surface = pygame.Surface((800, 800))
        self.simulation = simulation
        self.hexagons = simulation.board.get_hexagons()

        self.actor_symbols: List[ActorSymbol] = None
        self.GetActorSymbols()

    def GetActorSymbols(self):
        actors = self.simulation.get_actors()

        actor_symbols = []
        for actor in actors:
            actor_symbols.append(ActorSymbol(self.game_surface, actor, 8, True, self.simulation))

        self.actor_symbols = actor_symbols


    def Render(self):
        self.renderGameSurface()
        self.renderActors()

    def renderActors(self):
        for actor_symbol in self.actor_symbols:
            actor_symbol.render(self.simulation)

    def renderGameSurface(self):
        """Renders hexagons on the screen"""

        for hexagon in self.hexagons:
            hexagon.render(self.game_surface)

        # draw borders around colliding hexagons and neighbours
        mouse_pos = pygame.mouse.get_pos()
        colliding_hexagons = [
            hexagon for hexagon in self.hexagons if hexagon.collide_with_point(mouse_pos)
        ]

        for hexagon in colliding_hexagons:
            for neighbour in hexagon.compute_neighbours(self.hexagons):
                neighbour.render_highlight(self.game_surface, border_colour=(100, 100, 100))
            hexagon.render_highlight(self.game_surface, border_colour=(0, 0, 0))
