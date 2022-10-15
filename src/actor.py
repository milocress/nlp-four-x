from __future__ import annotations
from world import Location


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


class Actor:
    def __init__(self, location: Location, name: str):
        self.location = location
        self.name = name

    def move(self, destination: Location):
        raise NotImplementedError

    def move_with_troops(self, destination: Location):
        raise NotImplementedError

    def dispatch(self, message: Message):
        raise NotImplementedError
