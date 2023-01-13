import click
from integrates.graphql import (
    create_session,
)
import os
from sorts.association.file import (
    execute_association_rules,
)
from sorts.integrates.dal import (
    get_user_email,
)
from sorts.predict.file import (
    prioritize as prioritize_files,
    update_integrates_toes,
)
from sorts.training.file import (
    get_subscription_file_metadata,
)
from sorts.utils.bugs import (
    configure_bugsnag,
)
from sorts.utils.decorators import (
    shield,
)
from sorts.utils.logs import (
    log,
    log_to_remote_info,
    mixpanel_track,
)
import sys
import time
from training.redshift import (
    db as redshift,
)


@click.command(
    help="File prioritizer according to the likelihood of finding "
    "a vulnerability"
)
@click.argument(
    "subscription",
    type=click.Path(
        allow_dash=False,
        dir_okay=True,
        exists=True,
        file_okay=False,
        readable=True,
        resolve_path=True,
    ),
)
@click.argument("date", type=str, required=False)
@click.option(
    "--association-rules",
    is_flag=True,
    help="Assign vulnerability suggestions to all the subscription files",
)
@click.option(
    "--get-file-data",
    is_flag=True,
    help="Extract file features from the subscription to train ML models",
)
@click.option(
    "--update-group-priority",
    is_flag=True,
    help="Update ToEs priorities based on Sorts execution folder in S3",
)
@click.option(
    "--token",
    envvar="INTEGRATES_API_TOKEN",
    help="Integrates API token.",
    show_envvar=True,
)
@shield(on_error_return=False)
def execute_sorts(  # pylint: disable=too-many-arguments
    subscription: str,
    date: str,
    association_rules: bool,
    get_file_data: bool,
    update_group_priority: bool,
    token: str,
) -> None:
    configure_bugsnag()
    start_time: float = time.time()
    success: bool = False
    if token:
        create_session(token)
        user_email: str = get_user_email()
        group: str = os.path.basename(os.path.normpath(subscription))
        if get_file_data:
            success = get_subscription_file_metadata(subscription)
        elif association_rules:
            execute_association_rules(group)
            success = True
        elif update_group_priority:
            csv_name: str = f"{group}_sorts_results_file.csv"
            success = update_integrates_toes(group, csv_name, date)
        else:
            success = prioritize_files(subscription)

        execution_time: float = time.time() - start_time
        log_to_remote_info(
            msg=f"Success: {success}",
            subscription=subscription,
            time=f"Finished after {execution_time:.2f} seconds",
            get_file_data=get_file_data,  # type: ignore
            association_rules=association_rules,  # type: ignore
            update_group_priority=update_group_priority,  # type: ignore
            user=user_email,
        )
        redshift.insert(
            "executions",
            {
                "group_name": subscription.split("/")[-1],
                "execution_time": execution_time,
            },
        )
        mixpanel_track(
            user_email,
            "sorts_execution",
            subscription=subscription,
            get_file_data=get_file_data,  # type: ignore
            association_rules=association_rules,  # type: ignore
            update_group_priority=update_group_priority,  # type: ignore
        )
    else:
        log(
            "error",
            "Set the Integrates API token either using the option "
            "--token or the environmental variable "
            "INTEGRATES_API_TOKEN",
        )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
    execute_sorts(prog_name="sorts")
