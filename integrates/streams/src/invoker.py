# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import bugsnag
import importlib
import logging.config
import os
import sys


def initialize_settings() -> None:
    bugsnag.configure(
        api_key=os.environ["BUGSNAG_API_KEY_STREAMS"],
        app_type="worker",
        app_version=os.environ["CI_COMMIT_SHA"],
        notify_release_stages=["prod"],
        project_root=os.path.dirname(os.path.abspath(__file__)),
        release_stage=os.environ["ENVIRONMENT"],
    )
    logging.config.dictConfig(
        {
            "handlers": {
                "bugsnag": {
                    "class": "bugsnag.handlers.BugsnagHandler",
                    "extra_fields": {"extra": ["extra"]},
                    "level": "WARNING",
                },
                "console": {"class": "logging.StreamHandler", "level": "INFO"},
            },
            "loggers": {
                "": {
                    "handlers": ["bugsnag", "console"],
                    "level": "INFO",
                },
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
