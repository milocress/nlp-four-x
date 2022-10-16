from __future__ import annotations
from typing import List, Optional, Dict, Tuple

class Adjacency:
    def __init__(
            self,
            source: Location,
            destination: Location,
            distance: int,
    ):
        self.source = source
        self.destination = destination
        self.distance = distance


class Position:
    def __init__(
            self,
            static_position: Optional[Location],
            en_route: Optional[Tuple[Adjacency, int]],
    ):
        if static_position is None and en_route is None:
            raise ValueError("static position and en route position cannot both be none")
        elif static_position is not None and en_route is not None:
            raise ValueError("static position and en route position cannot both be specified")
        self.static_position = static_position
        self.en_route = en_route

    def set_en_route(self, en_route: Tuple[Adjacency, int]):
        self.en_route = en_route
        self.static_position = None

    def get_arrival_time(self) -> int:
        return self.en_route[1]

    def get_dest_loc(self) -> Location:
        return self.en_route[0].destination

    def set_static_location(self, loc: Location):
        if not isinstance(loc, Location):
            raise Exception("bad args to set loc")
        self.en_route = None
        self.static_position = loc

    def is_moving(self) -> bool:
        return self.en_route is not None

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
