from nlp_actor import NLPActor
from src.actor import Actor, Message
from src.world import Location, GeographicFeature

homeland = Location(
    parent_feature=GeographicFeature(
        name="Moria",
        adjacencies=[],
        children=[],
        population=190,
        nexus_location=None
    ),
    actors=[],
    name="Mordor"
)

my_actors = [NLPActor(homeland) for _ in range(2)]

me = Actor(homeland, "Strackus")

message = Message(
    homeland, homeland, me, my_actors[0],
    contents="stay put",
    arrival_time=0)

# print(my_actor.bio)
#
# response = my_actor.respond_to_order(message)

# print(response.contents)

print("Names")
print([my_actor.name for my_actor in my_actors])

print("Adjectives")
print([my_actor.descriptors for my_actor in my_actors])

print("Profiles")
print([my_actor.character_profile for my_actor in my_actors])

print("Replies")
print([my_actor.reply_to_message(message, obey=False) for my_actor in my_actors])

print("Images")
print([my_actor.character_profile_image_url for my_actor in my_actors])