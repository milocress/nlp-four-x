from typing import List, Union
from transformers import pipeline
from diffusers import StableDiffusionPipeline
import torch

from src.actor import Actor, Message, Action, Movement, Occupy, Dispatch
from src.nlp.gpt_order_parsing import is_movement_order, is_occupation_order
from src.world import Location

class NLPActor(Actor):

    def __init__(self, location: Location):
        self.generator = pipeline(task="text-generation", model="gpt2")
        self.birth_location = location
        name = self.create_name()
        super().__init__(location, name)
        self.descriptors = self.get_descriptors()
        self.character_profile = self.get_character_profile()

    def ask_generator(self, prompt: str, length: int, hint: str = "", n: int = 1) -> Union[str, List[str]]:
        outs = self.generator(
            prompt + hint,
            max_new_tokens=length,
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

    def summarize_character(self, text: str, length: int, hint: str = "") -> str:
        def make_prompt(input, output=""):
            return f"\n#Text:{input}\n#Summary:{output}"
        prompt = "Here is text and its summary\n"
        prompt += make_prompt("Valinor is smart, kind, reckless, and thoughtful.", "Valinor. The wisest of us, he led us through the hardest perils in our kingdom with only his wit and bravado.")
        prompt += make_prompt("Bjork is ruthless, evil, cunning, and brash.", "Bjorn. A dangerous foe, he destroys anything that displeases him, leaving his enemies only the dust for company.")
        prompt += make_prompt("Arnos is courageous, clumsy, loyal, and gruff.", "Arnos. When his friends are in danger, nothing stands in his way. Though he appears rough on the outside, he bravely opens up to his friends.")
        prompt += make_prompt(input=text)
        return sorted(self.ask_generator(
            prompt=prompt,
            length=length,
            hint=hint,
            n=5
        ), key=len)[-2].split("\n")[0]

    def reply_to_message(self, message: Message, obey: bool) -> str:
        def make_prompt(input, output="", should_obey=True):
            return f"\n#Message:{input}\n#Response type:{'obey' if should_obey else 'disobey'}\n#Response from {self.name}:{output}"
        prompt = f"Context: {self.character_profile}"
        prompt += "Here are messages and their respective responses\n"
        prompt += make_prompt("Go attack #1", f"Dear General {message.sender.name}, it would be my honor to aid your forces. I will obey your order with duty and honor.", should_obey=True)
        prompt += make_prompt("Stay put", f"Dear General {message.sender.name}, I obey your commands as if they were the last breath of a dying brother.", should_obey=True)
        prompt += make_prompt("Go and attack #1", f"Dear General {message.sender.name}, I regret that my conscience compels me to disobey.", should_obey=False)
        prompt += make_prompt(input=message.contents, should_obey=obey)
        return sorted(self.ask_generator(
            prompt=prompt,
            length=20,
            hint=f"Dear General {message.sender.name},",
            n=4
        ), key=len)[-2].split("\n")[0]


    def create_name(self) -> str:
        output = self.ask_generator(
            prompt=f"The name of the warrior general from {self.birth_location.parent_feature.name} was \"",
            length=3)
        output = output.replace(".", "\"")
        output = output.replace(",", "\"")
        output = output.replace(":", "\"")
        return output.split("\"")[0]

    def get_descriptors(self) -> List[str]:
        output = self.ask_generator(
            prompt=f"The three best words that describe {self.name} the warrior chief are wise, brave, and",
            length=3,
            n=15)
        adjectives = []
        for rest in output:
            if len(rest.split(" ")) < 2:
                continue
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
        return self.summarize_character(repetitive_character_profile, 50, hint=f"Warrior General {self.name}.")

    def get_actions(self) -> List[Action]:
        print("actions from messages:")
        print(self.pending_messages)
        actions = []
        for message in self.pending_messages:
            is_motion_order = is_movement_order(message.contents)
            occupation_order = is_occupation_order(message.contents)

            if is_motion_order and not occupation_order:
                print("ordered to move!")
                actions.append(Movement(message.loc_map["#0"], 0))
            elif occupation_order:
                actions.append(Occupy())
            else:
                print("not ordered to move")

            # generate reply
            reply = self.reply_to_message(message, obey=True)
            actions.append(Dispatch(reply, message.sender))


        self.pending_messages = []
        return actions
