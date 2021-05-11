
# None


from ariadne import ObjectType

from api.resolvers.event import consulting


EVENT = ObjectType('Event')
EVENT.set_field('consulting', consulting.resolve)
