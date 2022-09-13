# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

""" Auxiliar functions for forms handling """


def is_exploitable(explotability: float, version: str) -> str:
    if version == "3.1":
        if explotability >= 0.97:
            exploitable = "Si"
        else:
            exploitable = "No"
    else:
        if explotability in (1.0, 0.95):
            exploitable = "Si"
        else:
            exploitable = "No"
    return exploitable
