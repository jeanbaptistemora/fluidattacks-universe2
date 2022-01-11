from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE as DYNAMODB_TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)
import logging
import logging.config
from redshift import (
    operations as redshift_ops,
)
from redshift.operations import (
    SCHEMA_NAME,
)
from settings import (
    LOGGING,
    NOEXTRA,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
REDSHIFT_METADATA_TABLE: str = f"{SCHEMA_NAME}.vulns_metadata"


async def remove(*, vulnerability_id: str) -> None:
    primary_key = keys.build_key(
        facet=DYNAMODB_TABLE.facets["vulnerability_metadata"],
        values={"id": vulnerability_id},
    )

    key_structure = DYNAMODB_TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
        ),
        facets=(
            DYNAMODB_TABLE.facets["vulnerability_metadata"],
            DYNAMODB_TABLE.facets["vulnerability_historic_state"],
            DYNAMODB_TABLE.facets["vulnerability_historic_treatment"],
            DYNAMODB_TABLE.facets["vulnerability_historic_verification"],
            DYNAMODB_TABLE.facets["vulnerability_historic_zero_risk"],
        ),
        table=DYNAMODB_TABLE,
    )
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item[key_structure.partition_key],
                sort_key=item[key_structure.sort_key],
            )
            for item in response.items
        ),
        table=DYNAMODB_TABLE,
    )


async def initialize_metadata_table() -> None:
    LOGGER.info(
        f"Ensuring {REDSHIFT_METADATA_TABLE} table exists...", **NOEXTRA
    )
    await redshift_ops.execute(
        f"""
            CREATE TABLE IF NOT EXISTS {REDSHIFT_METADATA_TABLE} (
                id VARCHAR,
                custom_severity INTEGER,
                finding_id VARCHAR NOT NULL,
                skims_method VARCHAR,
                type VARCHAR NOT NULL,

                UNIQUE (
                    id
                ),
                PRIMARY KEY (
                    id
                )
            )
        """,
    )
