# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import importlib
import logging.config
import sys


def initialize_settings() -> None:
    logging.config.dictConfig(
        {
            "handlers": {
                "console": {"class": "logging.StreamHandler", "level": "INFO"},
            },
            "loggers": {
                "": {"handlers": ["console"], "level": "INFO"},
            },
            "version": 1,
        }
    )


def invoke_consumer(module_name: str) -> None:
    """Invokes the requested consumer"""
    consumer = importlib.import_module(f"{module_name}.consumer")
    consumer.consume()


if __name__ == "__main__":
    initialize_settings()
    invoke_consumer(sys.argv[1])
