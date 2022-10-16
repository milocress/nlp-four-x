from typing import List, Optional
from transformers import pipeline

from src.world import Actor, Message, Action, Location


class NLPActor(Actor):
    def get_actions(self, messages: [Message]) -> List[Action]:
        pass

    def __init__(self, location: Location, name: str):
        super().__init__(location, name)
        self.generator = pipeline(task="text-generation")
        self.birth_location = location
        self.bio: Optional[str] = None

    def set_bio(self):
        location = self.birth_location
        name = self.name
        township = location.parent_feature.name
        population = location.parent_feature.population

        bio_prompt = f"""{name} is a general of the armies of {township} tasked with defending his homeland of {township}, which has a population of {population}.
Write a story about {name}. 
-----------------------------
"""

        bio_prompt_len = len(bio_prompt)

        bio_prompt += f"""{name} was born"""

        self.bio = self.generator(
            bio_prompt,
            max_length=150,
            early_stopping=True,
            # num_beams=5,
            do_sample=True,
            top_k=0,
        )[0]['generated_text'][bio_prompt_len:]

    def respond_to_order(self, message: Message) -> Message:
        order_prompt = f"""{self.bio}
-----------------------------
Later that year, {message.sender.name} wrote to {message.recipient.name}. The letter is transcribed below:
-----------------------------
{message.contents}
-----------------------------
{message.recipient.name} responded to the letter immediately: 
-----------------------------
"""
        order_prompt_len = len(order_prompt)
        order_prompt += f"""Dear {message.sender.name},"""

        return_contents = self.generator(
            order_prompt,
            max_length=250,
            early_stopping=True,
            # num_beams=5,
            do_sample=True,
            top_k=0,
        )[0]['generated_text'][order_prompt_len:]

        return Message(source=self.location, destination=message.source, sender=self, recipient=message.sender,
                       contents=return_contents)
