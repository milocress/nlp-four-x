import os
import openai

openai.organization = "org-05vQQXUzgb3nMqOdGrdoy9au"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()

print("test")

print(os.getenv("OPENAI_API_KEY"))

openai.organization = "org-05vQQXUzgb3nMqOdGrdoy9au"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()

def is_movement_order(text):
    if len(text) > 1000:
        print("We wish we could afford this")

    prompt = """
Is it a troop motion order? 

"go to #1": yes
"move your troops to #0": yes 
"attack #2": yes 
"order your men to #4": yes 
"stay put for the moment in #1": no 
"how are you?": no 
"what is up?": no 
"wait for more instructions.": no
"""

    prompt += "\"" + text + "\": "

    # print(prompt)

    res = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        max_tokens=1,
        temperature=0
    )

    # print(res)
    #
    # print()

    text_res: str = res["choices"][0]["text"]

    return "yes" in text_res


def test_motion_order_classification():
    # false
    print("should be FALSE:")
    print(is_movement_order("stay put"))
    print(is_movement_order("how are you today? Today sure is good day in #1 isn't it?"))
    print(is_movement_order("hey how are you man, do not move"))
    print(is_movement_order("keep your men at home in the barracks. How's the weather in your province #1"))
    print(is_movement_order("await further orders from #1"))
    print(is_movement_order("is the army in good condition for a future campaign?"))
    print(is_movement_order("are there good sources of nearby water in #1?"))

    # true
    print("should be TRUE:")
    print(is_movement_order("go to #1"))
    print(is_movement_order("go to #0"))
    print(is_movement_order("attack #1 with all possible haste. Do not stay out!!"))
    print(is_movement_order("move to strike in the northern province #1"))
    print(is_movement_order("attack immediately to the heart of the enemy in #1"))
    print(is_movement_order("march towards #1 tomorrow"))
    print(is_movement_order("send your army towards #1 soon"))
    print(is_movement_order("please leave from the barracks and attack the province of #1 soon"))


if __name__ == "__main__":
    test_motion_order_classification()
