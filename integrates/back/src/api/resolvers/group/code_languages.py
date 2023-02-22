from .schema import (
    GROUP,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
    GroupUnreliableIndicators,
)
from db_model.types import (
    CodeLanguage,
)
from decorators import (
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("codeLanguages")
@require_asm
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[CodeLanguage] | None:
    loaders: Dataloaders = info.context.loaders
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(parent.name)
    )
    return group_indicators.code_languages
