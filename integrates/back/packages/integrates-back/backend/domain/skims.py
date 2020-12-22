# Standard
from typing import Tuple

# Third party
import aiohttp
from aiohttp import FormData

# Local
from __init__ import (
    CI_PROJECT_ID,
    PRODUCT_PIPELINE_TOKEN,
)


async def execute_skims(group_name: str) -> Tuple[bool, str]:
    url = 'https://gitlab.com/api/v4/projects/{}/trigger/pipeline'.format(
        CI_PROJECT_ID)
    form = FormData()
    form.add_field('token', PRODUCT_PIPELINE_TOKEN)
    form.add_field('ref', 'master')
    form.add_field('variables[CI_COMMIT_TITLE]', 'skims')
    form.add_field('variables[SKIMS_GROUP_TO_PROCESS_ON_AWS]', group_name)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form) as response:
            pipeline_url = (await response.json()).get('web_url', None)
            return (bool(pipeline_url), pipeline_url)
