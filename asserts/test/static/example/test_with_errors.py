#/usr/bin/python3
"""Test exploit."""

from fluidasserts.format import string

# it's missing one argument
string.is_otp_token_insecure()
