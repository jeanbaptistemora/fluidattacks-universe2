from ctx import (
    CTX,
)
from model import (
    core_model,
)
from model.core_model import (
    LocalesEnum,
    SkimsDastConfig,
)
import os


def create_test_context(
    debug: bool = True,
    include: tuple[str, ...] = (),
    exclude: tuple[str, ...] = (),
) -> None:
    CTX.debug = debug
    CTX.config = core_model.SkimsConfig(
        apk=core_model.SkimsAPKConfig(
            exclude=(),
            include=(),
        ),
        checks=set(core_model.FindingEnum),
        commit=None,
        dast=SkimsDastConfig(
            aws_credentials=[],
            http=core_model.SkimsHttpConfig(
                include=(),
            ),
            ssl=core_model.SkimsSslConfig(
                include=(),
            ),
            urls=(),
            http_checks=False,
            ssl_checks=False,
        ),
        group=None,
        language=LocalesEnum.EN,
        namespace="test",
        output=None,
        path=core_model.SkimsPathConfig(
            include=include,
            exclude=exclude,
            lib_path=True,
            lib_root=True,
        ),
        start_dir=os.getcwd(),
        working_dir=os.getcwd(),
        execution_id="123456789",
    )
