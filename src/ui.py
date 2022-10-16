from typing import List

import pygame
import pygame_gui

from src.events import RECV_MESSAGE_EVENT
from src.simulation import Simulation


class Actors(object):
    pass

class UI:
    def __init__(self, manager):
        self.advance_day_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((825, 20), (150, 50)),
                                                               text='Advance Day',
                                                               manager=manager)

        self.tile_text_box = pygame_gui.elements.ui_text_box.UITextBox("",
                                                                       relative_rect=pygame.Rect((825, 80), (150, 200)),
                                                                       manager=manager)

        self.command_entry = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect((825, 300), (150, 200)),
            manager=manager)

        self.recipient_select = pygame_gui.elements.ui_selection_list.UISelectionList(
            pygame.Rect((825, 520), (150, 50)),
            [],
            manager=manager)

        self.send_message = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((825, 590), (150, 50)),
                                                         text='Send Message',
                                                         manager=manager)

        self.inbox = pygame_gui.elements.ui_text_box.UITextBox("",
                                                                       relative_rect=pygame.Rect((50, 810), (800, 80)),
                                                                       manager=manager)


    def handleUIEvent(self, event, simulation: Simulation):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.advance_day_button:
                print('Advancing Day')
                simulation.simulate_time_step()
            if event.ui_element == self.send_message:
                print("Send Message")

                simulation.add_player_message(self.recipient_select.get_single_selection(), self.command_entry.text)

        if event.type == RECV_MESSAGE_EVENT:
            print("inner")
            print(event)
            if event.inbox:
                print("recv message event")
                self.inbox.set_text(simulation.inbox)

    def get_actor_list(actors):
        text = ""
        for actor in actors:
            text += str(actor) + ", <br>"
        return text

    def actor_name_list(self, actors):
        return [actor.name for actor in actors]

    def set_actor_name_list(self, actors: List[Actors]):
        self.recipient_select.set_item_list(self.actor_name_list(actors))
