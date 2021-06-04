from model import (
    core_model,
)
import os
from utils.ctx import (
    CTX,
)


def create_test_context(debug: bool = True) -> None:
    CTX.debug = debug
    CTX.config = core_model.SkimsConfig(
        apk=core_model.SkimsAPKConfig(
            include=(),
        ),
        checks=set(core_model.FindingEnum),
        group=None,
        http=core_model.SkimsHttpConfig(
            include=(),
        ),
        language=core_model.LocalesEnum.EN,
        namespace="test",
        output=None,
        path=core_model.SkimsPathConfig(
            include=(),
            exclude=(),
            lib_path=True,
            lib_root=True,
        ),
        start_dir=os.getcwd(),
        timeout=None,
        working_dir=os.getcwd(),
    )
