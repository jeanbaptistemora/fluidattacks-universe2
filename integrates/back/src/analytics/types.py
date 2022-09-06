from typing import (
    NamedTuple,
)


class GraphicParameters(NamedTuple):
    document_type: str
    document_name: str
    entity: str
    generator_name: str
    generator_type: str
    height: int
    subject: str
    width: int


class GraphicsForEntityParameters(NamedTuple):
    entity: str
    subject: str


class GraphicsCsvParameters(NamedTuple):
    document_name: str
    document_type: str
    entity: str
    subject: str


class ReportParameters(NamedTuple):
    entity: str
    subject: str
