
# None


from ariadne import ObjectType

from api.resolvers.tag import groups


TAG = ObjectType('Tag')
TAG.set_field('projects', groups.resolve)
