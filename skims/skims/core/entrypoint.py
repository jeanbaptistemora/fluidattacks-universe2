# Standard library
from asyncio import (
    wait_for,
)
import csv
import logging
from os import (
    chdir,
    getcwd,
)
from typing import (
    Dict,
    Optional,
)

# Third party imports
from aioextensions import (
    collect,
)

# Local imports
from config import (
    load,
)
from core.persist import (
    persist,
)
from lib_path.analyze import (
    analyze as analyze_paths,
)
from state.ephemeral import (
    EphemeralStore,
    get_ephemeral_store,
    reset as reset_ephemeral_state,
)
from utils.ctx import (
    CTX,
)
from utils.logs import (
    log,
    set_level,
)
from utils.model import (
    FindingEnum,
)
from zone import (
    t,
)


async def execute_skims(token: Optional[str]) -> bool:
    """Execute skims according to the provided config.

    :param token: Integrates API token
    :type token: str
    :raises MemoryError: If not enough memory can be allocated by the runtime
    :raises SystemExit: If any critical error occurs
    :return: A boolean indicating success
    :rtype: bool
    """
    success: bool = True

    stores: Dict[FindingEnum, EphemeralStore] = {
        finding: get_ephemeral_store() for finding in FindingEnum
    }

    await wait_for(
        collect((
            analyze_paths(stores=stores),
        )),
        CTX.config.timeout,
    )

    if CTX.config.output:
        await notify_findings_as_csv(stores, CTX.config.output)
    else:
        await notify_findings_as_snippets(stores)

    if CTX.config.group and token:
        msg = 'Results will be synced to group: %s'
        await log('info', msg, CTX.config.group)

        success = await persist(
            group=CTX.config.group,
            stores=stores,
            token=token,
        )
    else:
        success = True
        await log('info', ' '.join((
            'In case you want to persist results to Integrates',
            'please make sure you set the --token and --group flag in the CLI',
        )))

    return success


async def notify_findings_as_snippets(
    stores: Dict[FindingEnum, EphemeralStore],
) -> None:
    """Print user-friendly messages about the results found."""
    for store in stores.values():
        async for result in store.iterate():
            if result.skims_metadata:
                await log(
                    'info', '{title}: {what}\n\n{snippet}\n'.format(
                        title=t(result.finding.value.title),
                        what=result.what,
                        snippet=result.skims_metadata.snippet,
                    ))


async def notify_findings_as_csv(
    stores: Dict[FindingEnum, EphemeralStore],
    output: str,
) -> None:
    headers = ('title', 'what', 'where', 'cwe')
    rows = [
        {
            'cwe': ' + '.join(sorted(result.skims_metadata.cwe)),
            'title': t(result.finding.value.title),
            'what': result.what,
            'where': result.where,
        }
        for store in stores.values()
        async for result in store.iterate()
        if result.skims_metadata
    ]

    with open(output, 'w') as file:
        writer = csv.DictWriter(file, headers, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(sorted(rows, key=str))

    await log('info', 'An output file has been written: %s', output)


async def main(
    config: str,
    group: Optional[str],
    token: Optional[str],
) -> bool:
    if CTX.debug:
        set_level(logging.DEBUG)

    try:
        startdir: str = getcwd()
        CTX.config = load(group, config)
        await reset_ephemeral_state()
        await log('info', 'Startup working dir is: %s', startdir)
        await log('info', 'Moving working dir to: %s', CTX.config.working_dir)
        chdir(CTX.config.working_dir)
        return await execute_skims(token)
    finally:
        chdir(startdir)
        await reset_ephemeral_state()
