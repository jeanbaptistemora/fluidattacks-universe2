from aioextensions import (
    collect,
)
import boto3
from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_FERNET_TOKEN,
)
from cryptography.fernet import (
    Fernet,
)
import csv
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.roots.types import (
    Root,
)
from db_model.toe_lines.types import (
    GroupToeLinesRequest,
    ToeLines,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from newutils import (
    bugsnag as bugsnag_utils,
)
from organizations import (
    domain as orgs_domain,
)
import os
from schedulers.common import (
    info,
)
import tempfile
from toe.lines import (
    domain as toe_lines_domain,
)
from toe.lines.types import (
    ToeLinesAttributesToUpdate,
)

# Constants
FERNET = Fernet(FI_FERNET_TOKEN)

S3_BUCKET_NAME: str = "sorts"
S3_RESOURCE = boto3.resource("s3")
S3_BUCKET = S3_RESOURCE.Bucket(S3_BUCKET_NAME)

bugsnag_utils.start_scheduler_session()


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
)
async def update_toe_lines(
    current_value: ToeLines, attributes: ToeLinesAttributesToUpdate
) -> None:
    await toe_lines_domain.update(
        current_value,
        attributes,
    )


async def update_toe_lines_priority(  # pylint: disable=too-many-locals
    group_name: str,
    current_date: datetime,
    group_toe_lines: tuple[ToeLines, ...],
    predicted_files: csv.DictReader,
) -> None:
    loaders: Dataloaders = get_new_context()
    in_scope_toes = []
    updates = []
    in_scope_count = 0
    out_scope_count = 0

    for predicted_file in predicted_files:
        decryped_filepath = FERNET.decrypt(
            predicted_file["file"].encode()
        ).decode()
        predicted_nickname, predicted_filename = decryped_filepath.split(
            "/", 1
        )
        predicted_file_prob = int(float(predicted_file["prob_vuln"]))

        for toe_line in group_toe_lines:
            root: Root = await loaders.root.load(
                (group_name, toe_line.root_id)
            )
            root_nickname = root.state.nickname
            if (
                toe_line.filename == predicted_filename
                and root_nickname == predicted_nickname
            ):
                updates.append(
                    update_toe_lines(
                        toe_line,
                        ToeLinesAttributesToUpdate(
                            sorts_risk_level=predicted_file_prob,
                            sorts_risk_level_date=current_date,
                        ),
                    )
                )
                in_scope_toes.append(toe_line)
                in_scope_count += 1

    for toe_line in group_toe_lines:
        if (
            toe_line not in in_scope_toes
            and toe_line.state.sorts_risk_level_date != datetime(1970, 1, 1)
        ):
            updates.append(
                update_toe_lines(
                    toe_line,
                    ToeLinesAttributesToUpdate(
                        sorts_risk_level_date=datetime(1970, 1, 1),
                    ),
                )
            )
            out_scope_count += 1

    info(
        f"Group {group_name} has {len(group_toe_lines)} present toe lines "
        f"with {in_scope_count} toe lines to be updated using Sorts "
        f"and {out_scope_count} toe lines out of Sorts scope"
    )

    await collect(tuple(updates))


async def process_group(group_name: str, current_date: datetime) -> None:
    loaders: Dataloaders = get_new_context()
    info(f"Processing group {group_name}")

    group_toe_lines = await loaders.group_toe_lines.load_nodes(
        GroupToeLinesRequest(group_name=group_name, be_present=True)
    )

    csv_name: str = f"{group_name}_sorts_results_file.csv"

    with tempfile.TemporaryDirectory() as tmp_dir:
        local_file: str = os.path.join(tmp_dir, csv_name)
        try:
            S3_BUCKET.Object(
                f"sorts-execution-results/{csv_name}"
            ).download_file(local_file)
        except ClientError as error:
            if error.response["Error"]["Code"] == "404":
                info(f"There is no {group_name} file in S3")
                return

        with open(local_file, "r", encoding="utf8") as csv_file:
            reader = csv.DictReader(csv_file)
            await update_toe_lines_priority(
                group_name, current_date, group_toe_lines, reader
            )
            info(f"ToeLines's sortsFileRisk for {group_name} updated")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await orgs_domain.get_all_active_group_names(loaders)
    current_date = datetime.now()
    current_date = current_date.replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    await collect(
        tuple(
            process_group(group_name, current_date)
            for group_name in group_names
        ),
        workers=8,
    )
