# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from backend.api.resolvers.new.me import organizations


ME = ObjectType('Me')

ME.set_field('organizations', organizations.resolve)
