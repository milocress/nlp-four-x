from typing import Set, List

from src.actor import Actor, Action, Movement, Message
from src.board import Board
from src.nlp.nlp_actor import NLPActor
from src.world import Position


class Simulation:
    def __init__(self):
        print("import actors")
        self.player: Actor = None
        self.name_to_actor = {}
        self.actors = []
        self.board: Board = Board(10, 10)
        self.gen_actors()

        self.time: int = 0
        self.messages: Set[Message] = set()

    def get_message(self, source: Actor, recipient: Actor, contents: str, loc_map=None) -> Message:
        # TODO fix static position assumptions
        curr_loc = source.position.static_position
        final_dest_est = self.estimate_loc_of_actor(recipient).static_position
        first_step = self.board.get_first_step(curr_loc, final_dest_est)
        return Message(curr_loc, first_step.destination, source, recipient, self.time + first_step.distance, contents, loc_map)

    def add_player_message(self, recipient: str, text: str):

        loc_map = {}
        loc_refs = 0
        for loc_name in self.board.name_to_loc:
            if loc_name in text:
                print("location in player message")
                tag = "#" + str(loc_refs)
                text = text.replace(loc_name, tag)
                loc_refs += 1
                loc_map[tag] = self.board.name_to_loc[loc_name]

        print(recipient)
        print(self.name_to_actor)

        if recipient in self.name_to_actor:
            recipient_actor = self.name_to_actor[recipient]
        else:
            print("sending to unknown actor")
            print(recipient)

        self.messages.add(self.get_message(self.player, recipient_actor, text, loc_map))

    def gen_actors(self):
        self.player = Actor(self.board.coord_to_feature[(5, 5)].nexus_location, "player")
        self.actors.append(self.player)

        actor1 = NLPActor(self.board.coord_to_feature[(6, 6)].nexus_location)
        self.actors.append(actor1)

        self.name_to_actor[actor1.name] = actor1

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
                print("Message arrives in: " + str(self.board.feature_to_coord[message.destination.parent_feature]))
                recipient_loc = self.estimate_loc_of_actor(message.recipient)
                if recipient_loc.static_position == message.destination:
                    # message has arrived:
                    print("recipient gets message!!")
                    print(message.contents)
                    message.recipient.receive_message(message)
                else:
                    message.source = message.destination
                    adj = self.board.get_first_step(message.source, recipient_loc.static_position)
                    message.arrival_time = self.time + adj.distance
                    message.destination = adj.destination
                    new_messages.add(message)
            else:
                new_messages.add(message)

        self.messages = new_messages

        # simulate actors

        for actor in self.actors:
            self.handle_motion(actor)

        for actor in self.actors:
            self.handle_actions(actor, actor.get_actions())

        self.time += 1

    def handle_motion(self, actor):
        if actor.position.is_moving():
            if actor.position.get_arrival_time() == self.time:
                actor.position.set_static_location(actor.position.get_dest_loc())
                if len(actor.path) > 0:
                    print(len(actor.path))
                    print("starting next segment")
                    actor.move(actor.path[0], self.time + actor.path[0].distance)
                    if len(actor.path) > 1:
                        actor.set_path(actor.path[1:])
                    else:
                        actor.set_path([])
                else:
                    print("done movement")

    def handle_actions(self, actor, actions: List[Action]):
        for action in actions:
            if isinstance(action, Movement):
                path, dist = self.board.get_path(actor.position.static_position, action.destination)
                actor.set_path(path[1:])
                actor.move(path[0], self.time + path[0].distance)

    def get_actors(self):
        return self.actors

    def estimate_loc_of_actor(self, actor: Actor) -> Position:
        # TODO implement for real
        return actor.position

        if actor in self.location_estimates:
            return self.location_estimates[actor]
        else:
            return None
