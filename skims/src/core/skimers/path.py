# Standard library
from itertools import chain

# Local imports
from apis.asserts import (
    get_vulnerabilities,
)
from core.findings.model import (
    Finding as FindingModel,
)
from utils.aio import (
    materialize,
)
from utils.logs import (
    log_blocking,
)


MODEL_INSECURE_RANDOM_NUMBERS_GENERATION = FindingModel(
    asserts_exploit="""
        from fluidasserts.utils import generic
        from fluidasserts.lang import csharp, java, javascript

        generic.add_finding('MODEL_INSECURE_RANDOM_NUMBERS_GENERATION')

        exclude: list = [ '.git/', 'test' ]

        java.has_insecure_randoms(ARGS['path'], exclude=exclude)
        javascript.has_insecure_randoms(ARGS['path'], exclude=exclude)
    """,
    rules=(
        '223',
    ),
    title='FIN.S.0034. Insecure random numbers generation',
)


async def skim(path: str) -> bool:
    log_blocking('debug', 'skim(path=%s)', path)

    _ = chain(*await materialize((
        get_vulnerabilities(model.asserts_exploit)
        for model in [
            MODEL_INSECURE_RANDOM_NUMBERS_GENERATION,
        ]
    )))

    return True
