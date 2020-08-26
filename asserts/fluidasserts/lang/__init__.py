# -*- coding: utf-8 -*-

"""Fluid Asserts lang package."""

# standard imports
from contextvars import ContextVar

# 3rd party imports
from networkx import DiGraph

GRAPHS = ContextVar('Graphs', default=DiGraph())
