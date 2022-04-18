# pylint: disable=invalid-name
"""
Remove from redshift vulns that belong to removed findings.
This vulns were not marked as DELETED when the finding was removed, so they
were wrongly migrated to redshift.

Execution Time:    2022-04-18 at 21:28:34 UTC
Finalization Time: 2022-04-18 at 21:51:53 UTC
"""

from aioextensions import (
    run,
)
import csv
import logging
import logging.config
from redshift import (
    operations as redshift_ops,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")

SCHEMA_NAME: str = "integrates"
METADATA_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_metadata"
STATE_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_state"
TREATMENT_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_treatment"
VERIFICATION_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_verification"
ZERO_RISK_TABLE: str = f"{SCHEMA_NAME}.vulnerabilities_zero_risk"


async def _remove_vulns_from_table(
    *,
    table: str,
    vuln_ids: list[str],
) -> None:
    sql_vars = [
        dict(
            id=vuln_id,
        )
        for vuln_id in vuln_ids
    ]
    await redshift_ops.execute_batch(  # nosec
        sql_query=f"""
            DELETE FROM {table}
            WHERE id=%(id)s
        """,
        sql_vars=sql_vars,
    )


async def main() -> None:
    with open("0205_data.csv", mode="r", encoding="utf8") as in_file:
        reader = csv.reader(in_file)
        vuln_ids = [rows[0] for rows in reader if rows[0] != "uuid str"]
    LOGGER_CONSOLE.info(
        "Vuln UUIDs read from file",
        extra={"extra": {"vulns_uuids_len": len(vuln_ids)}},
    )

    vuln_tables = [
        STATE_TABLE,
        TREATMENT_TABLE,
        VERIFICATION_TABLE,
        ZERO_RISK_TABLE,
        METADATA_TABLE,
    ]
    for table in vuln_tables:
        await _remove_vulns_from_table(
            table=table,
            vuln_ids=vuln_ids,
        )
        LOGGER_CONSOLE.info(
            "Table updated",
            extra={"extra": {"table": table}},
        )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
