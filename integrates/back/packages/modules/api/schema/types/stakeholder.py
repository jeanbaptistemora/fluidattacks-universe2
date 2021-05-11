
# None


from ariadne import ObjectType

from api.resolvers.stakeholder import groups


STAKEHOLDER: ObjectType = ObjectType('Stakeholder')
STAKEHOLDER.set_field('projects', groups.resolve)
