#/usr/bin/python3
"""Test exploit."""

from fluidasserts.format import string

otp = '123456'
string.is_otp_token_insecure(otp)
