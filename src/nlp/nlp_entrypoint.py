from nlp_actor import NLPActor
from src.world import Location, GeographicFeature, Actor, Message

homeland = Location(
    parent_feature=GeographicFeature(
        name="Snorsgard",
        adjacencies=[],
        children=[],
        population=190,
        nexus_location=None
    ),
    actors=[]
)

my_actor = NLPActor(homeland)

me = Actor(homeland, "Strackus")

message = Message(
    homeland, homeland, me, my_actor,
    contents="Dear Bjorn,\nPlease aid me in the coming war.\nSincerely, Strackus")

# print(my_actor.bio)
#
# response = my_actor.respond_to_order(message)

# print(response.contents)

print(my_actor.name)

print(my_actor.descriptors)

print(my_actor.character_profile)