# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
    new_cmd,
)
import logging
from utils_logger_2.levels import (
    LoggingLvl,
)


@dataclass(frozen=True)
class _Logger:
    logger: logging.Logger


@dataclass(frozen=True)
class Logger:
    _inner: _Logger

    def critical(
        self, formatted_msg: str, values: FrozenList[str]
    ) -> Cmd[None]:
        return Cmd.from_cmd(
            lambda: self._inner.logger.critical(formatted_msg, *values)
        )

    def debug(self, formatted_msg: str, values: FrozenList[str]) -> Cmd[None]:
        return Cmd.from_cmd(
            lambda: self._inner.logger.debug(formatted_msg, *values)
        )

    def info(self, formatted_msg: str, values: FrozenList[str]) -> Cmd[None]:
        return Cmd.from_cmd(
            lambda: self._inner.logger.info(formatted_msg, *values)
        )

    def warning(
        self, formatted_msg: str, values: FrozenList[str]
    ) -> Cmd[None]:
        return Cmd.from_cmd(
            lambda: self._inner.logger.warning(formatted_msg, *values)
        )


def get_logger(name: str) -> Cmd[Logger]:
    def _action() -> Logger:
        log = _Logger(logging.getLogger(name))
        return Logger(log)

    return Cmd.from_cmd(_action)


def set_logger(
    name: str, lvl: LoggingLvl, handlers: FrozenList[Cmd[logging.Handler]]
) -> Cmd[None]:
    def _action(act: CmdUnwrapper) -> None:
        log = logging.getLogger(name)
        log.setLevel(lvl.value)
        for h in handlers:
            log.addHandler(act.unwrap(h))

    return new_cmd(_action)
