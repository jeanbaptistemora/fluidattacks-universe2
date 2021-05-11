
from ariadne import ObjectType

from api.resolvers.git_root import toe_lines


GITROOT: ObjectType = ObjectType('GitRoot')
GITROOT.set_field('toeLines', toe_lines.resolve)
