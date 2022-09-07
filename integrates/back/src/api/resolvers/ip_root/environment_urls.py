# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    IPRoot,
    RootEnvironmentUrl,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: IPRoot, info: GraphQLResolveInfo
) -> tuple[RootEnvironmentUrl, ...]:
    loaders: Dataloaders = info.context.loaders
    urls: tuple[
        RootEnvironmentUrl, ...
    ] = await loaders.root_environment_urls.load((parent.id))
    return tuple(url._replace(group_name=parent.group_name) for url in urls)
