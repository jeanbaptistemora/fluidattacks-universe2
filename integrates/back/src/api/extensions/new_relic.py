from api import (
    Operation,
)
from ariadne.types import (
    Extension,
    Resolver,
)
from graphql import (
    GraphQLResolveInfo,
    version,
)
from inspect import (
    isawaitable,
)
import newrelic.agent
from typing import (
    Any,
)


class NewRelicTracingExtension(Extension):
    def request_started(self, context: Any) -> None:
        operation: Operation = context.operation
        newrelic.agent.set_transaction_name(operation.name, "GraphQL")
        newrelic.agent.add_framework_info("GraphQL", version)
        newrelic.agent.add_custom_parameters(
            tuple(operation._asdict().items())
        )

    # pylint:disable=arguments-renamed
    # Disabled due to https://gitlab.com/fluidattacks/product/-/issues/6088
    async def resolve(
        self,
        next_: Resolver,
        parent_: Any,
        info: GraphQLResolveInfo,
        **kwargs: Any,
    ) -> Any:
        path = "/".join(
            field for field in info.path.as_list() if isinstance(field, str)
        )

        with newrelic.agent.FunctionTrace(
            f"resolvers/{path}", group="GraphQL", params=kwargs
        ):
            result = next_(parent_, info, **kwargs)
            if isawaitable(result):
                return await result
            return result
