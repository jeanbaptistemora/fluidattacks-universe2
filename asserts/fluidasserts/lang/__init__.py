# -*- coding: utf-8 -*-

"""Fluid Asserts lang package."""


from contextvars import (
    ContextVar,
)
from networkx import (
    DiGraph,
)

GRAPHS = ContextVar("Graphs", default=DiGraph())
