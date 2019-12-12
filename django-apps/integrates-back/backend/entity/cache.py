import re
from graphene import Boolean, Mutation, String
from backend.decorators import require_login, require_role

from backend import util


class InvalidateCache(Mutation):

    class Arguments():
        pattern = String(required=True)
    success = Boolean()

    @staticmethod
    @require_login
    @require_role(['admin', 'analyst'])
    def mutate(_, info, pattern):
        regex = r'^\w+$'
        if re.match(regex, pattern):
            util.invalidate_cache(pattern)
            success = True
            util.cloudwatch_log(
                info.context,
                f'Security: Pattern {pattern} was removed from cache')
        else:
            success = False

        return InvalidateCache(success=success)
