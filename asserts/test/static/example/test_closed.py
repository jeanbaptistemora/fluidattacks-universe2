# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# /usr/bin/python3
"""Test exploit."""

from fluidasserts.format import (
    string,
)

otp = "123456"
string.is_otp_token_insecure(otp)
