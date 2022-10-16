import sys
from queue import PriorityQueue
from typing import List, Dict, Set
from typing import Tuple
import heapq

from src.nlp.nlp_actor import NLPActor
from src.ui.hexagons import init_hexagons, HexagonTile
from src.world import GeographicFeature, Location, Adjacency, Actor, Message


class Board:
    def __init__(
            self,
            width,
            height
    ):
        self.locations = []
        self.features = []
        self.name_to_actor = {}
        self.name_to_loc = {}
        self.coord_to_hex: Dict[Tuple[int, int], HexagonTile] = {}
        self.coord_to_feature: Dict[Tuple[int, int], GeographicFeature] = {}
        self.feature_to_coord: Dict[GeographicFeature, Tuple[int, int]] = {}
        self.hexagons = init_hexagons(self.coord_to_hex, flat_top=True)
        self.gen_hex_world(width, height)
        self.player: Actor = None
        self.actors = []
        self.gen_actors()
        self.time = 0
        self.messages: Set[Message] = set()

    def gen_actors(self):
        self.player = Actor(self.coord_to_feature[(5,5)].nexus_location, "player")
        self.actors.append(self.player)


        actor1 = NLPActor(self.coord_to_feature[(6,6)].nexus_location)
        self.actors.append(actor1)

        self.name_to_actor[actor1.name] = actor1

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

    def simulate_time_step(self):

        # if self.time == 1:
        #     print("adding message")
        #     npc = self.actors[1]
        #
        #     message = self.get_message(self.player, npc, "test message")
        #
        #     self.messages.add(message)


        # handle messages
        new_messages: Set[Message] = set()

        for message in self.messages:
            if message.arrival_time == self.time:
                # we arrive at destination
                print("Message arrives in: " + str(self.feature_to_coord[message.destination.parent_feature]))
                recipient_loc = message.destination.estimate_loc_of_actor(message.recipient)
                if recipient_loc == message.destination:
                    # message has arrived:
                    print("recipient gets message!!")
                    print(message.contents)
                    message.recipient.receive_message(message)
                else:
                    message.source = message.destination
                    dist, message.destination = self.get_first_step(message.source, recipient_loc)
                    message.arrival_time = self.time + dist
                    new_messages.add(message)
            else:
                new_messages.add(message)

        self.messages = new_messages

        # simulate actors

        for actor in self.actors:
           actor.run_actions(actor.get_actions())

        self.time += 1


    def get_first_step(self, a: Location, b: Location) -> (int, Location):
        path, dist = self.get_path(a, b)
        print(path)
        return dist[path[0]], path[0]

    def get_path(self, a: Location, b: Location):
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
                        prev[location] = current_location
                        heapq.heappush(pq, (distance, location))
            else:
                # TODO not relevant to current geometry
                print("UNIMPLEMENTED")

        print("getting path")
        path = [b]
        curr = prev[b]

        while curr is not a:
            path.append(curr)
            curr = prev[curr]

        path.reverse()
        return path, dist

    def get_hexagons(self):
        return self.hexagons

    def get_hex_from_feature(self, feature: GeographicFeature):
        return self.coord_to_hex[self.feature_to_coord[feature]]

    def get_feature_from_hex(self, hexagon: HexagonTile) -> GeographicFeature:
        return self.coord_to_feature[hexagon.game_coords]

    def get_actors(self):
        return self.actors

    def test_path_finding(self):
        loc_a = self.coord_to_feature[(5,5)].nexus_location
        loc_b = self.coord_to_feature[(5,6)].nexus_location

        _, step1 = self.get_first_step(loc_a, loc_b)

        assert step1 == loc_b

        loc_a = self.coord_to_feature[(5,5)].nexus_location
        loc_b = self.coord_to_feature[(6,6)].nexus_location

        _, step1 = self.get_first_step(loc_a, loc_b)

        print(self.feature_to_coord[step1.parent_feature])

    def get_message(self, source: Actor, recipient: Actor, contents: str, loc_map=None) -> Message:
        curr_loc = source.location
        final_dest_est = curr_loc.estimate_loc_of_actor(recipient)
        dist, first_step = self.get_first_step(curr_loc, final_dest_est)
        return Message(curr_loc, first_step, source, recipient, self.time + dist, contents, loc_map)

    def add_player_message(self, recipient: str, text: str):

        loc_map = {}
        loc_refs = 0
        print(self.name_to_loc)
        for loc_name in self.name_to_loc:
            if loc_name in text:
                print("location in player message")
                tag = "#" + str(loc_refs)
                text = text.replace(loc_name, tag)
                loc_refs += 1
                loc_map[tag] = self.name_to_loc[loc_name]


        print(recipient)
        print(self.name_to_actor)

        if recipient in self.name_to_actor:
            recipient_actor = self.name_to_actor[recipient]
        else:
            print("sending to unknown actor")
            print(recipient)

        self.messages.add(self.get_message(self.player, recipient_actor, text, loc_map))