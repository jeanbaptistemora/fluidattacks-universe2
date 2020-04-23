# pylint: disable=import-error
import re

from typing import Dict
from asgiref.sync import sync_to_async
from backend.decorators import require_login, enforce_user_level_auth_async
from backend import util

from ariadne import convert_kwargs_to_snake_case


@require_login
@enforce_user_level_auth_async
@convert_kwargs_to_snake_case
async def resolve_invalidate_cache(_, info, pattern: str) -> Dict[str, bool]:
    """Resolve invalidate_cache."""
    success = False
    regex = r'^\w+$'
    if re.match(regex, pattern):
        await sync_to_async(util.invalidate_cache)(pattern)
        success = True
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Pattern {pattern} was \
removed from cache')  # pragma: no cover
    return dict(success=success)
