from __future__ import annotations
from world import Location
from typing import List


class Message:
    def __init__(
            self,
            source: Location,
            destination: Location,
            sender: Actor,
            recipient: Actor,
            contents: str,
    ):
        self.source = source
        self.destination = destination
        self.sender = sender
        self.recipient = recipient
        self.contents = contents


class Action:
    pass


class Movement(Action):
    def __init__(self, destination: Location, troop_commitment: int):
        self.destination = destination
        self.troop_commitment = troop_commitment


class Dispatch(Action):
    def __init__(self, message: Message):
        self.message = message


class Actor:
    def __init__(self, location: Location, name: str):
        self.location = location
        self.name = name

    def move(self, destination: Location) -> None:
        raise NotImplementedError

    def move_with_troops(self, destination: Location, num_troops: int) -> None:
        raise NotImplementedError

    def dispatch(self, message: Message) -> None:
        raise NotImplementedError

    def get_actions(self, messages: [Message]) -> List[Action]:
        raise NotImplementedError

    def run_actions(self, actions: List[Action]):
        for action in actions:
            if isinstance(action, Dispatch):
                self.dispatch(action.message)
            elif isinstance(action, Movement):
                if action.troop_commitment != 0:
                    self.move_with_troops(action.destination, action.troop_commitment)
                else:
                    self.move(action.destination)