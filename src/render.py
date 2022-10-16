import pygame

from src.nlp.nlp_actor import NLPActor
from src.simulation import Simulation


def renderActors(simulation: Simulation, game_surface):
    actors = simulation.get_actors()
    for actor in actors:
        if isinstance(actor, NLPActor):
            color = pygame.Color('red')
        else:
            color = pygame.Color('blue')

        if actor.position.is_moving():
            pass
        else:
            location = actor.position.static_position
            feature = location.parent_feature
            hex = simulation.board.get_hex_from_feature(feature)

            pygame.draw.circle(game_surface, color, (hex.centre[0], hex.centre[1]), 5)  # DRAW CIRCLE


def renderGameSurface(hexagons):
    """Renders hexagons on the screen"""
    game_surface = pygame.Surface((800, 800))

    for hexagon in hexagons:
        hexagon.render(game_surface)

    # draw borders around colliding hexagons and neighbours
    mouse_pos = pygame.mouse.get_pos()
    colliding_hexagons = [
        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
    ]
    for hexagon in colliding_hexagons:
        # print(hexagon.game_coords)
        for neighbour in hexagon.compute_neighbours(hexagons):
            neighbour.render_highlight(game_surface, border_colour=(100, 100, 100))
        hexagon.render_highlight(game_surface, border_colour=(0, 0, 0))

    # draw_state_box(game_surface, tile_text)

    return game_surface
