from ariadne.types import (
    Extension,
    Resolver,
)
from graphql import (
    GraphQLResolveInfo,
)
from inspect import (
    isawaitable,
)
import newrelic.agent
from typing import (
    Any,
)


class NewRelicTracingExtension(Extension):
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
