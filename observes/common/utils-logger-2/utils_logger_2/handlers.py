# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import bugsnag
from bugsnag.handlers import (
    BugsnagHandler,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
import logging
from logging import (
    Formatter,
    Handler,
)
from typing import (
    IO,
)
from utils_logger_2.env import (
    Envs,
)
from utils_logger_2.levels import (
    LoggingLvl,
)


@dataclass(frozen=True)
class BugsnagConf:
    app_type: str
    app_version: str
    project_root: str
    auto_capture_sessions: bool
    api_key: str
    release_stage: Envs


def bug_handler(conf: BugsnagConf, min: LoggingLvl) -> Cmd[Handler]:
    def _action() -> Handler:
        bugsnag.configure(  # type: ignore[no-untyped-call]
            app_type=conf.app_type,
            app_version=conf.app_version,
            project_root=conf.project_root,
            auto_capture_sessions=conf.auto_capture_sessions,
            api_key=conf.api_key,
            release_stage=conf.release_stage.value,
        )
        handler = BugsnagHandler()  # type: ignore[no-untyped-call]
        handler.setLevel(min.value)
        return handler

    return Cmd.from_cmd(_action)


def logger_handler(
    debug: bool, show_time: bool, target: IO[str]
) -> Cmd[Handler]:
    def _action() -> Handler:
        prefix = "%(name)s> " if debug else ""
        _time = "%(asctime)s " if show_time else ""
        _format = _time + prefix + "[%(levelname)s] %(message)s"
        formatter = Formatter(_format)
        handler = logging.StreamHandler(target)
        handler.setFormatter(formatter)
        return handler

    return Cmd.from_cmd(_action)
