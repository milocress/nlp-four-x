from __future__ import annotations
from typing import List, Optional, Dict
from src.nlp.gpt_order_parsing import is_movement_order

class Adjacency:
    def __init__(
            self,
            source: Location,
            destination: Location,
            distance: float,
    ):
        self.source = source
        self.destination = destination
        self.distance = distance


class Position:
    def __init__(
            self,
            static_position: Optional[Location],
            en_route: Optional[Adjacency],
    ):
        if static_position is None and en_route is None:
            raise ValueError("static position and en route position cannot both be none")
        elif static_position is not None and en_route is not None:
            raise ValueError("static position and en route position cannot both be specified")
        self.static_position = static_position
        self.en_route = en_route


class Location:
    def __init__(
            self,
            parent_feature: GeographicFeature,
            actors: List[Actor],
            name: str
    ):
        self.parent_feature = parent_feature
        self.actors = actors
        self.location_estimates = {}
        self.name = name

    def estimate_loc_of_actor(self, actor: Actor):
        # TODO implement for real
        return actor.location

        if actor in self.location_estimates:
            return self.location_estimates[actor]
        else:
            return None

    def update_location_estimate(self, actor: Actor, location: Location):
        self.location_estimates[actor] = location

    def is_nexus(self):
        return self.parent_feature.nexus_location == self

    def __lt__(self, other):
        # arbitrary, should not be used
        return self.parent_feature.name < other.parent_feature.name

class GeographicFeature:
    def __init__(
            self,
            adjacencies: List[Adjacency],
            children: List[GeographicFeature],
            population: int,
            name: str,
            nexus_location: Optional[Location],
    ):
        self.adjacencies = adjacencies
        self.children = children
        self.population = population
        self.name = name
        self.nexus_location = nexus_location

    def set_adjacencies(self, adjacencies):
        self.adjacencies = adjacencies

    def set_nexus_location(self, location):
        self.nexus_location = location

#actor file

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
        self.location = location
        location.actors.append(self)
        self.name = name
        self.pending_messages = []

    def __str__(self):
        return self.name

    def receive_message(self, message: Message):
        print("receiving message")
        print(self.name)
        self.pending_messages.append(message)
        print(self.pending_messages)

    def move(self, destination: Location) -> None:
        print("executing move")
        self.location.actors.remove(self)
        self.location = destination
        destination.actors.append(self)

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