#/usr/bin/python3
"""Test exploit."""

from fluidasserts.format import jks

jks.use_password('not-existing-path', 'password')
