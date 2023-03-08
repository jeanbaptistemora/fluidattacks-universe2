from graphql import (
    Source,
)
from graphql.language import (
    parser,
)
from opentelemetry.instrumentation.instrumentor import (  # type: ignore
    BaseInstrumentor,
)
from opentelemetry.instrumentation.utils import (
    unwrap,
)
from opentelemetry.trace import (
    get_tracer,
)
import re
from typing import (
    Any,
    Callable,
)
from wrapt import (
    wrap_function_wrapper,
)


class GraphQLCoreInstrumentor(BaseInstrumentor):
    """
    OpenTelemetry instrumentor for graphql-core

    Pending contribution to upstream
    https://github.com/open-telemetry/opentelemetry-python-contrib/
    """

    def _instrument(self, **kwargs: Any) -> None:
        # pylint: disable=attribute-defined-outside-init
        self._tracer = get_tracer(__name__)

        wrap_function_wrapper(
            "graphql.language.parser",
            "parse",
            self._patched_parse,
        )

    def _uninstrument(self, **kwargs: Any) -> None:
        unwrap(parser, "parse")

    def _patched_parse(
        self,
        original_func: Callable[..., Any],
        _instance: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        with self._tracer.start_as_current_span("graphql.parse") as span:
            source = _get_source(args[0])
            span.set_attribute("graphql.source", source)

            return original_func(*args, **kwargs)


def _get_source(source: parser.SourceType) -> str:
    if isinstance(source, str):
        value = source
    elif isinstance(source, Source):
        value = source.body
    else:
        value = ""

    return re.sub(r"\s+", " ", value).strip()
