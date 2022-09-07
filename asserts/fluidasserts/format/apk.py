# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""This module allows to check ``APK`` vulnerabilities."""


import androguard
from androguard.core.analysis import (
    analysis,
)
from androguard.core.bytecodes import (
    apk,
    dvm,
)
from androguard.misc import (
    AnalyzeAPK,
)
from fluidasserts import (
    _get_result_as_tuple_sast,
    HIGH,
    LOW,
    MEDIUM,
    SAST,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
from functools import (
    lru_cache,
)
import logging
import re
from typing import (
    Any,
    List,
    Tuple,
)

# Set androguard logging levels to CRITICAL
androguard.core.androconf.show_logging(level=logging.CRITICAL)


@lru_cache(maxsize=None, typed=True)
def analyze_apk(path: str) -> tuple:
    """Return the resultant objects after analyzing the apk."""
    return AnalyzeAPK(path)


@lru_cache(maxsize=None, typed=True)
def get_dex(path: str) -> tuple:
    """Return DEX analysis from APK file."""
    apk_obj = apk.APK(path)
    _dex = dvm.DalvikVMFormat(apk_obj.get_dex())
    dex = analysis.Analysis()
    dex.add(_dex)
    dex.create_xref()
    return dex


def get_activities_source(dvms: list) -> str:
    """Decompile given Dalvik VM images."""
    source = [
        x.get_source()
        for dvm in dvms
        for x in dvm.get_classes()
        if "Activity" in x.name
    ]
    return "".join(source)


def is_method_present(dex, class_name, method, descriptor):
    """Search if method is present in decompiled code."""
    met_ana = dex.get_method_analysis_by_name(
        class_name=class_name, method_name=method, method_descriptor=descriptor
    )

    if not met_ana:
        return None

    used_by = [
        x.name for x, _, _ in met_ana.get_xref_from() if "Activity" in x.name
    ]

    return used_by


def get_http_urls(dex):
    """Get HTTP URLs used in APK file."""
    whitelist = {
        "http://schemas.android.com/",
        "http://www.w3.org/",
        "http://apache.org/",
        "http://xml.org/",
        "http://localhost/",
        "http://127.0.0.1/",
        "http://java.sun.com/",
    }
    return [
        x.get_value()
        for x in dex.get_strings()
        if re.match(r"^http?\:\/\/.+", x.get_value())
        and not any(re.match(whitel, x.get_value()) for whitel in whitelist)
    ]
