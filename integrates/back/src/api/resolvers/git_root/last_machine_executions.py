from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    LastMachineExecutions,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from machine.jobs import (
    get_active_executions,
)
from roots.types import (
    GitRoot,
)


async def resolve(
    parent: GitRoot, info: GraphQLResolveInfo, **_kwargs: None
) -> LastMachineExecutions:
    loaders: Dataloaders = info.context.loaders
    last_machine_executions = await get_active_executions(parent)
    if any(
        getattr(last_machine_executions, attr) is None
        for attr in LastMachineExecutions._fields
    ):
        machine_executions = await loaders.root_machine_executions.load(
            (parent.id)
        )
        last_complete_execution = next(
            (
                execution
                for execution in machine_executions
                if len(execution.findings_executed) > 1
            ),
            None,
        )
        last_specific_execution = next(
            (
                execution
                for execution in machine_executions
                if len(execution.findings_executed) == 1
            ),
            None,
        )
        last_machine_executions = LastMachineExecutions(
            complete=last_machine_executions.complete
            or last_complete_execution,
            specific=last_machine_executions.specific
            or last_specific_execution,
        )
    return last_machine_executions
