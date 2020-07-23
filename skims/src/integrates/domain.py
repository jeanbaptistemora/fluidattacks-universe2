# Standard library
from typing import (
    Dict,
    Tuple,
    Union,
)

# Local libraries
from integrates.dal import (
    do_create_draft,
    do_delete_finding,
    do_upload_vulnerabilities,
    get_group_findings,
    ResultGetGroupFindings,
)
from model import (
    IntegratesVulnerabilitiesLines,
    KindEnum,
    Vulnerability,
)
from utils.aio import (
    unblock,
)
from utils.encodings import (
    yaml_dumps,
)
from utils.string import (
    are_similar,
)


async def build_vulnerabilities_stream(
    *,
    results: Tuple[Vulnerability, ...],
) -> str:

    data_type = Dict[
        KindEnum,
        Tuple[Union[IntegratesVulnerabilitiesLines], ...]
    ]

    def _get_data() -> data_type:
        data: data_type = {
            KindEnum.LINES: tuple(
                IntegratesVulnerabilitiesLines(
                    line=result.where,
                    path=result.what,
                    state=result.state,
                )
                for result in results
                if result.kind == KindEnum.LINES
            ),
            # More bindings for PORTS and INPUTS go here ...
        }

        return data

    return await yaml_dumps(await unblock(_get_data))


async def get_closest_finding_id(
    *,
    create_if_missing: bool = False,
    group: str,
    title: str,
) -> str:
    findings: Tuple[ResultGetGroupFindings, ...] = \
        await get_group_findings(group=group)

    for finding in findings:
        if are_similar(title, finding.title):
            return finding.identifier

    # No similar finding has been found at this point

    if create_if_missing:
        if await do_create_draft(
            group=group,
            title=title,
        ):
            finding_id: str = await get_closest_finding_id(
                create_if_missing=False,
                group=group,
                title=title,
            )
        else:
            finding_id = ''
    else:
        finding_id = ''

    return finding_id


async def delete_closest_findings(*, group: str, title: str) -> bool:
    success: bool = True

    while True:
        finding_id: str = await get_closest_finding_id(
            group=group,
            title=title,
        )

        if finding_id:
            success = success and await do_delete_finding(
                finding_id=finding_id,
            )
        else:
            # All findings have been deleted
            break

    return success


async def do_build_and_upload_vulnerabilities(
    *,
    finding_id: str,
    results: Tuple[Vulnerability, ...],
) -> bool:
    return await do_upload_vulnerabilities(
        finding_id=finding_id,
        stream=await build_vulnerabilities_stream(
            results=results,
        ),
    )
