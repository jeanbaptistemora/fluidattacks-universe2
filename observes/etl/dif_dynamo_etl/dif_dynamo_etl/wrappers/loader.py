# Standard libraries
import subprocess
from typing import List
# Third party libraries
# Local libraries
from dif_dynamo_etl.wrappers.transformer import SingerPageData


def upload_page(
    spage: SingerPageData, schema: str, auth_file
) -> None:
    cmd = (
        "echo '[INFO] Running target' && "
        "target-redshift "
        f'--auth "{auth_file.name}" '
        f"--schema-name '{schema}' "
        f"< {spage.name}"
    )
    subprocess.check_output(cmd, shell=True)


def upload_pages(
    spages: List[SingerPageData], schema: str, auth_file
):
    for page in spages:
        upload_page(page, schema, auth_file)
