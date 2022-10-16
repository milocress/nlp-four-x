from typing import List, Dict
from typing import Tuple

from src.ui.hexagons import init_hexagons, HexagonTile
from src.world import GeographicFeature, Location, Adjacency


def gen_hex_world(num_x, num_y, gameboard: Dict[int, Dict[int, HexagonTile]], feature_map: Dict[GeographicFeature, HexagonTile]):

    features: List[GeographicFeature] = []

    for i in range(num_y):
        for j in range(num_x):
            feature = GeographicFeature([], [], 10, str(i) + str(j), None)
            feature_map[feature] = gameboard[i][j]

            location = Location(feature, [])


    # create adjacencies
    for feature in features:
        hexagon = feature_map[feature]
        adjs: List[Adjacency] = []
        for hexagon in hexagon.compute_neighbours():
            i, j = hexagon.game_coords
            neighbor_feature = gameboard[i][j]
            adjs.append(Adjacency(feature, neighbor_feature, 10))
        feature.set_adjacencies(adjs)


class Board:
    def __init__(
            self,
            width,
            height
    ):
        self.gameboard: Dict[int, Dict[int, HexagonTile]] = {}
        self.feature_map: Dict[GeographicFeature, HexagonTile] = {}
        self.hexagons = init_hexagons(self.gameboard, flat_top=True)

    def get_hexagons(self):
        return self.hexagons