from aiobotocore import (
    client,
    endpoint,
)
from botocore.exceptions import (
    ClientError,
)
from collections.abc import (
    Callable,
    Coroutine,
    Mapping,
)
from opentelemetry import (
    context,
    trace,
)
from opentelemetry.instrumentation.botocore import (  # type: ignore
    _apply_response_attributes,
    _determine_call_context,
    _find_extension,
    _patched_endpoint_prepare_request,
    _safe_invoke,
    BotocoreInstrumentor,
)
from opentelemetry.instrumentation.utils import (
    unwrap,
)
from opentelemetry.semconv.trace import (
    SpanAttributes,
)
from typing import (
    Any,
    cast,
)
from wrapt import (
    wrap_function_wrapper,
)


class AioBotocoreInstrumentor(BotocoreInstrumentor):
    """
    OpenTelemetry instrumentor for aiobotocore

    Pending contribution to upstream
    https://github.com/open-telemetry/opentelemetry-python-contrib/
    """

    def _instrument(self, **kwargs: Any) -> None:
        # pylint: disable=attribute-defined-outside-init
        self._tracer = trace.get_tracer(__name__)
        self.request_hook = kwargs.get("request_hook")
        self.response_hook = kwargs.get("response_hook")

        wrap_function_wrapper(
            "aiobotocore.client",
            "AioBaseClient._make_api_call",
            self._patched_async_api_call,
        )

        wrap_function_wrapper(
            "aiobotocore.endpoint",
            "AioEndpoint.prepare_request",
            _patched_endpoint_prepare_request,
        )

    def _uninstrument(self, **kwargs: Any) -> None:
        unwrap(client.AioBaseClient, "_make_api_call")
        unwrap(endpoint.AioEndpoint, "prepare_request")

    async def _patched_async_api_call(
        self,
        original_func: Callable[..., Coroutine],
        instance: client.AioBaseClient,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        # pylint: disable=protected-access
        if context.get_value(context._SUPPRESS_INSTRUMENTATION_KEY):
            return await original_func(*args, **kwargs)

        call_context = _determine_call_context(
            instance, cast(tuple[str, dict[str, Any]], args)
        )
        if call_context is None:
            return await original_func(*args, **kwargs)

        extension = _find_extension(call_context)
        if not extension.should_trace_service_call():
            return await original_func(*args, **kwargs)

        attributes = {
            SpanAttributes.RPC_SYSTEM: "aws-api",
            SpanAttributes.RPC_SERVICE: call_context.service_id,
            SpanAttributes.RPC_METHOD: call_context.operation,
            "aws.region": call_context.region,
        }

        _safe_invoke(extension.extract_attributes, attributes)

        with self._tracer.start_as_current_span(
            call_context.span_name,
            kind=call_context.span_kind,
            attributes=cast(Mapping[str, str], attributes),
        ) as span:
            _safe_invoke(extension.before_service_call, span)
            self._call_request_hook(span, call_context)

            # pylint: disable=protected-access
            token = context.attach(
                context.set_value(
                    context._SUPPRESS_HTTP_INSTRUMENTATION_KEY, True
                )
            )

            result = None
            try:
                result = await original_func(*args, **kwargs)
            except ClientError as error:
                result = getattr(error, "response", None)
                _apply_response_attributes(span, result)
                _safe_invoke(extension.on_error, span, error)
                raise
            else:
                _apply_response_attributes(span, result)
                _safe_invoke(extension.on_success, span, result)
            finally:
                context.detach(token)
                _safe_invoke(extension.after_service_call)

                self._call_response_hook(span, call_context, result)

            return result
