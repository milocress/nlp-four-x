from typing import List, Optional, Union
from transformers import pipeline

from src.actor import Actor
from src.world import Location


class NLPActor(Actor):

    def __init__(self, location: Location):
        self.generator = pipeline(task="text-generation")
        self.birth_location = location
        name = self.create_name()
        super().__init__(location, name)
        self.descriptors = self.get_descriptors()
        self.character_profile = self.get_character_profile()

    def ask_generator(self, prompt: str, length: int, hint: str = "", n: int = 1) -> Union[str, List[str]]:
        outs = self.generator(
            prompt + hint,
            max_length=length,
            early_stopping=True,
            do_sample=True,
            top_k=0,
            num_return_sequences=n,
        )

        rets = [out['generated_text'][len(prompt):] for out in outs]
        if n == 1:
            return rets[0]
        else:
            return rets

    def generate_summary(self, text: str, length: int, hint : str = "") -> str:
        return self.ask_generator(
            prompt=f"Here is a text and a short summary.\n#Text:{text}\n#Short Summary:",
            length=length,
            hint=hint
        ).split("\n")[0]

    def create_name(self) -> str:
        output = self.ask_generator(
            prompt=f"The name of the warrior general from {self.birth_location.parent_feature.name} was \"",
            length=20)
        return output.split("\"")[0]

    def get_descriptors(self) -> List[str]:
        output = self.ask_generator(
            prompt=f"The three best words that describe the warrior general {self.name} are wise, brave, and",
            length=30,
            n=10)
        adjectives = []
        for rest in output:
            rest = rest.replace("!", ".")
            rest = rest.replace(";", ".")
            rest = rest.replace(",", ".")
            rest = rest.replace(":", ".")
            rest = rest.replace("--", ".")
            rest = rest.replace("\n", ".")
            rest = rest.replace("?", ".")
            rest = rest.replace("—", ".")
            adjectives.append(rest.split(".")[0].strip().strip("_"))

        return adjectives

    def get_character_profile(self):
        repetitive_character_profile = f"{self.name} is "
        for adjective in self.descriptors:
            repetitive_character_profile += f"{adjective}, "
        return self.generate_summary(repetitive_character_profile, 200, hint=self.name)
