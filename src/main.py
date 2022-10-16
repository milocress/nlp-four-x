# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 13:50:07 2022

@author: richa
"""
import random
from typing import List
from typing import Tuple
import pygame
import pygame_gui

from src.board import Board


# pylint: disable=no-member
from src.nlp.nlp_actor import NLPActor
from src.render import renderGameSurface, renderActors
from src.simulation import Simulation
from src.ui import UI
from src.world import GeographicFeature, Location, Adjacency

def get_actor_list(actors):
    text = ""
    for actor in actors:
        text += str(actor) + ", <br>"
    return text


def main():

    # setup game board
    simulation = Simulation()

    hexagons = simulation.board.get_hexagons()

    # setup shapes state
    tile_text = "test"

    # shapes setup
    pygame.freetype.init()

    pygame.display.set_caption('Quick Start')
    screen = pygame.display.set_mode((1000, 800))

    background = pygame.Surface((1000, 800))
    background.fill(pygame.Color('lightskyblue3'))

    manager = pygame_gui.UIManager((1000, 800))
    ui = UI(manager)
    ui.set_actor_name_list(simulation.get_actors())

    # setup pygame loop
    pygame.init()
    clock = pygame.time.Clock()

    print("reaches shapes")
    terminated = False
    while not terminated:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                colliding_hexagons = [
                    hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
                ]
                for hexagon in colliding_hexagons:
                    print(hexagon.game_coords)
                    feature = simulation.board.get_feature_from_hex(hexagon)
                    tile_text = "name: " + feature.name + ", population: " + str(feature.population) + "<br>actors: " + get_actor_list(feature.nexus_location.actors)

                    ui.tile_text_box.set_text(tile_text)

            ui.handleUIEvent(event, simulation)
            manager.process_events(event)

        manager.update(time_delta)

        for hexagon in hexagons:
            hexagon.update()

        game_surface = renderGameSurface(hexagons)

        renderActors(simulation, game_surface)

        screen.blit(background, (0, 0))
        screen.blit(game_surface, (0, 0))

        manager.draw_ui(screen)
        pygame.display.flip()

        clock.tick(50)

    pygame.display.quit()


if __name__ == "__main__":
    main()
