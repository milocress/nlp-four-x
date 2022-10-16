from typing import List
from transformers import pipeline

from src.actor import Actor, Message, Action
from src.world import Location


class NLPActor(Actor):
    def get_actions(self, messages: [Message]) -> List[Action]:
        pass

    def __init__(self, location: Location, name: str):
        super().__init__(location, name)
        self.generator = pipeline(task="text-generation")

    def speak_with_actor(self, text):
        return self.generator(text)
