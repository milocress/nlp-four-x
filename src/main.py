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
from src.world import GeographicFeature, Location, Adjacency

def renderActors(board, game_surface):
    actors = board.actors
    for actor in actors:
        if isinstance(actor, NLPActor):
            color = pygame.Color('red')
        else:
            color = pygame.Color('blue')

        location = actor.location
        feature = location.parent_feature
        hex = board.get_hex_from_feature(feature)

        pygame.draw.circle(game_surface, color, (hex.centre[0], hex.centre[1]), 5)  # DRAW CIRCLE


def renderGameSurface(hexagons, tile_text):
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


def get_actor_list(actors):
    text = ""
    for actor in actors:
        text += str(actor) + ", <br>"
    return text

def actor_name_list(actors):
    return [actor.name for actor in actors]

def main():

    # setup game board
    board = Board(10, 10)

    board.test_path_finding()


    hexagons = board.get_hexagons()

    # setup ui state
    tile_text = "test"

    # ui setup
    pygame.freetype.init()

    pygame.display.set_caption('Quick Start')
    screen = pygame.display.set_mode((1000, 800))

    background = pygame.Surface((1000, 800))
    background.fill(pygame.Color('lightskyblue3'))

    manager = pygame_gui.UIManager((1000, 800))

    advance_day_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((825, 20), (150, 50)),
                                                text='Advance Day',
                                                manager=manager)

    tile_text_box = pygame_gui.elements.ui_text_box.UITextBox(tile_text, relative_rect=pygame.Rect((825, 80), (150, 200)),
                                                                        manager=manager)


    command_entry = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect((825, 300), (150, 200)),
                                                                            manager=manager)

    recipient_select = pygame_gui.elements.ui_selection_list.UISelectionList(pygame.Rect((825, 520), (150, 50)),
                                                                             actor_name_list(board.actors),
                                                                             manager=manager)

    send_message = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((825, 590), (150, 50)),
                                                text='Send Message',
                                                manager=manager)


    # setup pygame loop
    pygame.init()
    clock = pygame.time.Clock()

    print("reaches ui")
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
                    feature = board.get_feature_from_hex(hexagon)
                    tile_text = "name: " + feature.name + ", population: " + str(feature.population) + "<br>actors: " + get_actor_list(feature.nexus_location.actors)

                    tile_text_box.set_text(tile_text)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == advance_day_button:
                    print('Advancing Day')
                    board.simulate_time_step()
                if event.ui_element == send_message:
                    print("Send Message")

                    board.add_player_message(recipient_select.get_single_selection(), command_entry.text)

            manager.process_events(event)

        manager.update(time_delta)

        for hexagon in hexagons:
            hexagon.update()

        game_surface = renderGameSurface(hexagons, tile_text)

        renderActors(board, game_surface)

        screen.blit(background, (0, 0))
        screen.blit(game_surface, (0, 0))

        manager.draw_ui(screen)
        pygame.display.flip()

        clock.tick(50)

    pygame.display.quit()


if __name__ == "__main__":
    main()
