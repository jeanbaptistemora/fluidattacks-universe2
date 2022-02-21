from ctx import (
    CTX,
)
from model import (
    core_model,
)
from model.core_model import (
    LocalesEnum,
)
import os
from typing import (
    Tuple,
)


def create_test_context(
    debug: bool = True,
    include: Tuple[str, ...] = (),
    exclude: Tuple[str, ...] = (),
) -> None:
    CTX.debug = debug
    CTX.config = core_model.SkimsConfig(
        apk=core_model.SkimsAPKConfig(
            exclude=(),
            include=(),
        ),
        checks=set(core_model.FindingEnum),
        group=None,
        http=core_model.SkimsHttpConfig(
            include=(),
        ),
        language=LocalesEnum.EN,
        namespace="test",
        output=None,
        path=core_model.SkimsPathConfig(
            include=include,
            exclude=exclude,
            lib_path=True,
            lib_root=True,
        ),
        ssl=core_model.SkimsSslConfig(
            include=(),
        ),
        start_dir=os.getcwd(),
        working_dir=os.getcwd(),
    )
