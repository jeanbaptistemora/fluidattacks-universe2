# Standard libraries
import random
from typing import Any

# Local libraries
from backend import util
from custom_exceptions import InvalidDraftTitle
from model import findings
from model.findings.types import (
    Finding,
    FindingState,
)
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
)


async def create_draft_new(
    context: Any,
    group_name: str,
    title: str,
    **kwargs: Any
) -> None:
    if not findings_utils.is_valid_finding_title(title):
        raise InvalidDraftTitle()

    group_name = group_name.lower()
    last_fs_id = 550000000
    finding_id = str(random.randint(last_fs_id, 1000000000))
    user_info = await util.get_jwt_content(context)
    analyst_email = user_info['user_email']
    source = util.get_source(context)
    draft = Finding(
        affected_systems=kwargs.get('affected_systems', ''),
        analyst_email=analyst_email,
        attack_vector_desc=kwargs.get('attack_vector_desc', ''),
        cwe_url=kwargs.get('cwe_url', ''),
        description=kwargs.get('description', ''),
        group_name=group_name,
        id=finding_id,
        state=FindingState(
            modified_by=analyst_email,
            modified_date=datetime_utils.get_iso_date(),
            source=source,
            status='CREATED',
        ),
        risk=kwargs.get('risk', ''),
        recommendation=kwargs.get('recommendation', ''),
        requirements=kwargs.get('requirements', ''),
        title=title,
        threat=kwargs.get('threat', ''),
        type=kwargs.get('type', ''),
    )
    await findings.create(finding=draft)
