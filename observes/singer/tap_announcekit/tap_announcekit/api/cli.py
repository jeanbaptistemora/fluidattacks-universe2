from dataclasses import (
    dataclass,
)
import json
from returns.io import (
    IO,
)
from sgqlc import (
    codegen,
    introspection,
)
from sgqlc.endpoint.http import (
    HTTPEndpoint,
)
import sys
from tap_announcekit.api import (
    API_ENDPOINT,
)
from typing import (
    IO as IO_FILE,
    Optional,
)


def get_api_schema(target: IO_FILE[str]) -> IO[None]:
    endpoint = HTTPEndpoint(API_ENDPOINT)
    data = endpoint(
        introspection.query,
        introspection.variables(
            include_description=False,
            include_deprecated=False,
        ),
    )
    json.dump(data, target, sort_keys=True, indent=4, default=str)
    target.write("\n")
    if data.get("errors"):
        sys.exit(1)
    return IO(None)


@dataclass(frozen=True)
class ArgsAdapter:
    def __init__(
        self,
        api_schema: IO_FILE[str],
        output_code: IO_FILE[str],
        schema_name: Optional[str] = None,
        docstrings: bool = False,
    ) -> None:
        object.__setattr__(self, "schema.json", api_schema)
        object.__setattr__(self, "schema.py", output_code)
        object.__setattr__(self, "schema_name", schema_name)
        object.__setattr__(self, "docstrings", docstrings)


def gen_schema_code(
    api_schema: IO_FILE[str], output_code: IO_FILE[str]
) -> IO[None]:
    codegen.schema.handle_command(ArgsAdapter(api_schema, output_code))
    return IO(None)
