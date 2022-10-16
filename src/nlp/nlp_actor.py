from typing import List, Union
from transformers import pipeline
from diffusers import StableDiffusionPipeline
import torch

from src.world import Actor, Message, Action, Location


class NLPActor(Actor):
    def get_actions(self, messages: [Message]) -> List[Action]:
        pass

    def __init__(self, location: Location):
        self.generator = pipeline(task="text-generation", model="gpt2")
        self.birth_location = location
        name = self.create_name()
        super().__init__(location, name)
        self.pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_type=torch.float16,
                                                            revision="fp16")
        prompt = "a photo of an astronaut riding a horse on mars"
        image = self.pipe(prompt).images[0]
        self.descriptors = self.get_descriptors()
        self.character_profile = self.get_character_profile()

    def ask_generator(self, prompt: str, length: int, hint: str = "", n: int = 1) -> Union[str, List[str]]:
        outs = self.generator(
            prompt + hint,
            max_length=length,
            early_stopping=False,
            do_sample=True,
            top_k=0,
            num_return_sequences=n,
        )

        rets = [out['generated_text'][len(prompt):] for out in outs]
        if n == 1:
            return rets[0]
        else:
            return rets

    def summarize_character(self, text: str, length: int, hint: str = "") -> str:
        return self.ask_generator(
            prompt=f"Here is text and its summary:\n#Text:{text}\n#Summary:",
            length=length,
            hint=hint
        ).split("\n")[0]

    def create_name(self) -> str:
        output = self.ask_generator(
            prompt=f"The name of the warrior general from {self.birth_location.parent_feature.name} was \"",
            length=20)
        output = output.replace(".", "\"")
        output = output.replace(",", "\"")
        output = output.replace(":", "\"")
        return output.split("\"")[0]

    def get_descriptors(self) -> List[str]:
        output = self.ask_generator(
            prompt=f"The three best words that describe {self.name} the warrior chief are wise, brave, and",
            length=25,
            n=15)
        adjectives = []
        for rest in output:
            candidate = rest.split(" ")[1]\
                .strip().strip("\"").strip(".").strip(",").strip(";").strip("…").strip("—").strip(":")
            if candidate:
                if candidate in adjectives:
                    continue
                adjectives.append(candidate)

        return sorted(adjectives, key=lambda x: len(x))[2:-2]

    def get_character_profile(self):
        repetitive_character_profile = f"{self.name} is "
        for adjective in self.descriptors[:-1]:
            repetitive_character_profile += f"{adjective}, "
        repetitive_character_profile += f" and {self.descriptors[-1]}."
        return self.summarize_character(repetitive_character_profile, 100, hint=f"Warrior General {self.name}.")
