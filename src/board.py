import sys
from typing import List, Dict, Set
from typing import Tuple
import heapq

from src.shapes.hexagons import init_hexagons, HexagonTile
from src.world import GeographicFeature, Location, Adjacency

class Board:
    def __init__(
            self,
            width,
            height
    ):
        self.locations = []
        self.features = []
        self.name_to_loc = {}
        self.coord_to_hex: Dict[Tuple[int, int], HexagonTile] = {}
        self.coord_to_feature: Dict[Tuple[int, int], GeographicFeature] = {}
        self.feature_to_coord: Dict[GeographicFeature, Tuple[int, int]] = {}
        self.hexagons = init_hexagons(self.coord_to_hex, flat_top=True)
        self.gen_hex_world(width, height)

    def gen_hex_world(self, num_x, num_y):

        for i in range(num_y):
            for j in range(num_x):
                feature = GeographicFeature([], [], 10, str(i) + str(j), None)

                self.coord_to_feature[(i, j)] = feature
                self.feature_to_coord[feature] = (i, j)
                self.features.append(feature)

                loc_name = str(i) + str(j) + "l"
                location = Location(feature, [], loc_name)
                self.name_to_loc[loc_name] = location

                self.locations.append(location)

                feature.set_nexus_location(location)

        # create adjacencies
        for feature in self.features:
            hexagon = self.get_hex_from_feature(feature)
            adjs: List[Adjacency] = []
            # TODO STUPIDLY INEFFICIENT NEIGHBORS
            for hexagon in hexagon.compute_neighbours(self.hexagons):
                if hexagon.game_coords is not None:
                    i, j = hexagon.game_coords
                    neighbor_feature = self.coord_to_feature[(i,j)]
                    adjs.append(Adjacency(feature.nexus_location, neighbor_feature.nexus_location, 1))
            feature.set_adjacencies(adjs)

    def get_first_step(self, a: Location, b: Location) -> Adjacency:
        path, dist = self.get_path(a, b)
        return path[0]

    def get_path(self, a: Location, b: Location) -> Tuple[List[Adjacency], int]:
        prev = {}
        dist: Dict[Location, int] = {}

        for location in self.locations:
            dist[location] = sys.maxsize

        dist[a] = 0

        pq = [(0.0, a)]
        while len(pq) > 0:
            current_distance, current_location = heapq.heappop(pq)
            # print(current_location)

            if current_distance > dist[current_location]:
                continue

            if current_location.is_nexus():
                feature = current_location.parent_feature
                # print(feature.adjacencies)
                for adjacency in feature.adjacencies:
                    distance = current_distance + adjacency.distance
                    location = adjacency.destination

                    # print(location)
                    if distance < dist[location]:
                        dist[location] = distance
                        prev[location] = adjacency
                        heapq.heappush(pq, (distance, location))
            else:
                # TODO not relevant to current geometry
                print("UNIMPLEMENTED")

        print("getting path")
        path = []
        curr = prev[b]

        while True:
            path.append(curr)
            if curr.source not in prev:
                break
            curr = prev[curr.source]

        path.reverse()
        return path, dist

    def get_hexagons(self):
        return self.hexagons

    def get_hex_from_feature(self, feature: GeographicFeature):
        return self.coord_to_hex[self.feature_to_coord[feature]]

    def get_feature_from_hex(self, hexagon: HexagonTile) -> GeographicFeature:
        return self.coord_to_feature[hexagon.game_coords]

    def test_path_finding(self):
        loc_a = self.coord_to_feature[(5,5)].nexus_location
        loc_b = self.coord_to_feature[(5,6)].nexus_location

        _, step1 = self.get_first_step(loc_a, loc_b)

        assert step1 == loc_b

        loc_a = self.coord_to_feature[(5,5)].nexus_location
        loc_b = self.coord_to_feature[(6,6)].nexus_location

        _, step1 = self.get_first_step(loc_a, loc_b)

        print(self.feature_to_coord[step1.parent_feature])