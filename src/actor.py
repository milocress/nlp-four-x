from __future__ import annotations
from typing import List, Dict
from src.nlp.gpt_order_parsing import is_movement_order
from src.world import Location, Position, Adjacency


class Message:
    def __init__(
            self,
            source: Location,
            destination: Location,
            sender: Actor,
            recipient: Actor,
            arrival_time: int,
            contents: str,
            loc_map: Dict[str, Location] = None
    ):
        self.source = source
        self.destination = destination
        self.sender = sender
        self.recipient = recipient
        self.contents = contents
        self.arrival_time = arrival_time
        self.loc_map = loc_map

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
        self.position = Position(location, None)
        location.actors.append(self)
        self.name = name
        self.pending_messages = []
        self.path: List[Adjacency] = []

    def __str__(self):
        return self.name

    def receive_message(self, message: Message):
        print("receiving message")
        print(self.name)
        self.pending_messages.append(message)
        print(self.pending_messages)

    def set_path(self, path: List[Adjacency]):
        self.path = path

    def move(self, adjacency: Adjacency, arrivalTime: int) -> None:
        print("executing move")
        if self.position.is_moving():
            print("only stationary units can start to move!")

        self.position.set_en_route((adjacency, arrivalTime))

    def move_with_troops(self, destination: Location, num_troops: int) -> None:
        raise NotImplementedError

    def dispatch(self, message: Message) -> None:
        raise NotImplementedError

    def get_actions(self) -> List[Action]:
        print("actions from messages:")
        print(self.pending_messages)
        actions = []
        for message in self.pending_messages:
            is_motion_order = is_movement_order(message.contents)
            if is_motion_order:
                print("ordered to move!")
                actions.append(Movement(message.loc_map["#0"], 0))
            else:
                print("not ordered to move")
        self.pending_messages = []
        return actions

    def run_actions(self, actions: List[Action]):
        for action in actions:
            if isinstance(action, Dispatch):
                self.dispatch(action.message)
            elif isinstance(action, Movement):
                if action.troop_commitment != 0:
                    self.move_with_troops(action.destination, action.troop_commitment)
                else:
                    self.move(action.destination)