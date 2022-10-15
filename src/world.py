from __future__ import annotations
from typing import List, Any, Self, Optional
from actor import Actor


class Adjacency:
    def __init__(
            self,
            source: Location,
            destination: Location,
            distance: float,
            progress: Optional[float],
    ):
        self.source = source
        self.destination = destination
        self.distance = distance
        self.progress = progress


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
    def __int__(
            self,
            parent_feature: GeographicFeature,
            actors: List[Actor]
    ):
        self.parent_feature = parent_feature
        self.actors = actors


class GeographicFeature:
    def __init__(
            self,
            adjacencies: List[Adjacency],
            children: List[GeographicFeature],
            population: int,
            name: str,
            nexus_location: Location,
    ):
        self.adjacencies = adjacencies
        self.children = children
        self.population = population
        self.name = name
        self.nexus_location = nexus_location

