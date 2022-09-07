# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

"""
exceptions_close.py.

This is a test module to check exceptions.
"""
try:
    print("Hello world")
except FileNotFoundError:
    print("Managed")
try:
    print("Hello world")
except IndexError:
    print("Managed")
