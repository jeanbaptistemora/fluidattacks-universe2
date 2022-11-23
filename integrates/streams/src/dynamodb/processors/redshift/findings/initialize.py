from ..operations import (
    execute,
    initialize_schema,
    SCHEMA_NAME,
)
from psycopg2 import (
    sql,
)

METADATA_TABLE: str = "findings_metadata"
STATE_TABLE: str = "findings_state"
SEVERITY_CVSS20_TABLE: str = "findings_severity_cvss20"
SEVERITY_CVSS31_TABLE: str = "findings_severity_cvss31"
VERIFICATION_TABLE: str = "findings_verification"
VERIFICATION_VULN_IDS_TABLE: str = "findings_verification_vuln_ids"


def _initialize_metadata_table() -> None:
    execute(
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                cvss_version VARCHAR,
                group_name VARCHAR NOT NULL,
                hacker_email VARCHAR NOT NULL,
                requirements VARCHAR(MAX) NOT NULL,
                sorts VARCHAR NOT NULL,
                title VARCHAR(4096) NOT NULL,

                UNIQUE (
                    id
                ),
                PRIMARY KEY (
                    id
                )
            )
        """
        ).format(
            table=sql.Identifier(SCHEMA_NAME, METADATA_TABLE),
        ),
    )


def _initialize_state_table() -> None:
    execute(
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                modified_date TIMESTAMPTZ NOT NULL,
                modified_by VARCHAR NOT NULL,
                justification VARCHAR NOT NULL,
                source VARCHAR NOT NULL,
                status VARCHAR NOT NULL,

                PRIMARY KEY (
                    id,
                    modified_date
                ),
                FOREIGN KEY (id)
                    REFERENCES {reference_table}(id)
            )
        """,
        ).format(
            table=sql.Identifier(SCHEMA_NAME, STATE_TABLE),
            reference_table=sql.Identifier(SCHEMA_NAME, METADATA_TABLE),
        ),
    )


def _initialize_severity_cvss20_table() -> None:
    execute(
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                access_complexity DECIMAL(5,3) NOT NULL,
                access_vector DECIMAL(5,3) NOT NULL,
                authentication DECIMAL(5,3) NOT NULL,
                availability_impact DECIMAL(5,3) NOT NULL,
                availability_requirement DECIMAL(5,3) NOT NULL,
                collateral_damage_potential DECIMAL(5,3) NOT NULL,
                confidence_level DECIMAL(5,3) NOT NULL,
                confidentiality_impact DECIMAL(5,3) NOT NULL,
                confidentiality_requirement DECIMAL(5,3) NOT NULL,
                exploitability DECIMAL(5,3) NOT NULL,
                finding_distribution DECIMAL(5,3) NOT NULL,
                integrity_impact DECIMAL(5,3) NOT NULL,
                integrity_requirement DECIMAL(5,3) NOT NULL,
                resolution_level DECIMAL(5,3) NOT NULL,

                PRIMARY KEY (
                    id
                ),
                FOREIGN KEY (id)
                    REFERENCES {reference_table}(id)
            )
        """
        ).format(
            table=sql.Identifier(SCHEMA_NAME, SEVERITY_CVSS20_TABLE),
            reference_table=sql.Identifier(SCHEMA_NAME, METADATA_TABLE),
        ),
    )


def _initialize_severity_cvss31_table() -> None:
    execute(
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                attack_complexity DECIMAL(4,2) NOT NULL,
                attack_vector DECIMAL(4,2) NOT NULL,
                availability_impact DECIMAL(4,2) NOT NULL,
                availability_requirement DECIMAL(4,2) NOT NULL,
                confidentiality_impact DECIMAL(4,2) NOT NULL,
                confidentiality_requirement DECIMAL(4,2) NOT NULL,
                exploitability DECIMAL(4,2) NOT NULL,
                integrity_impact DECIMAL(4,2) NOT NULL,
                integrity_requirement DECIMAL(4,2) NOT NULL,
                modified_attack_complexity DECIMAL(4,2) NOT NULL,
                modified_attack_vector DECIMAL(4,2) NOT NULL,
                modified_availability_impact DECIMAL(4,2) NOT NULL,
                modified_confidentiality_impact DECIMAL(4,2) NOT NULL,
                modified_integrity_impact DECIMAL(4,2) NOT NULL,
                modified_privileges_required DECIMAL(4,2) NOT NULL,
                modified_user_interaction DECIMAL(4,2) NOT NULL,
                modified_severity_scope DECIMAL(4,2) NOT NULL,
                privileges_required DECIMAL(4,2) NOT NULL,
                remediation_level DECIMAL(4,2) NOT NULL,
                report_confidence DECIMAL(4,2) NOT NULL,
                severity_scope DECIMAL(4,2) NOT NULL,
                user_interaction DECIMAL(4,2) NOT NULL,

                PRIMARY KEY (
                    id
                ),
                FOREIGN KEY (id)
                    REFERENCES {reference_table}(id)
            )
        """
        ).format(
            table=sql.Identifier(SCHEMA_NAME, SEVERITY_CVSS31_TABLE),
            reference_table=sql.Identifier(SCHEMA_NAME, METADATA_TABLE),
        ),
    )


def _initialize_verification_table() -> None:
    execute(
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                modified_date TIMESTAMPTZ NOT NULL,
                status VARCHAR NOT NULL,

                PRIMARY KEY (
                    id,
                    modified_date
                ),
                FOREIGN KEY (id)
                    REFERENCES {reference_table}(id)
            )
        """
        ).format(
            table=sql.Identifier(SCHEMA_NAME, VERIFICATION_TABLE),
            reference_table=sql.Identifier(SCHEMA_NAME, METADATA_TABLE),
        ),
    )


def _initialize_verification_vuln_ids_table() -> None:
    execute(
        sql.SQL(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                id VARCHAR,
                modified_date TIMESTAMPTZ NOT NULL,
                vulnerability_id VARCHAR NOT NULL,

                PRIMARY KEY (
                    id,
                    modified_date,
                    vulnerability_id
                ),
                FOREIGN KEY (id)
                    REFERENCES {reference_table}(id)
            )
        """
        ).format(
            table=sql.Identifier(SCHEMA_NAME, VERIFICATION_VULN_IDS_TABLE),
            reference_table=sql.Identifier(SCHEMA_NAME, METADATA_TABLE),
        ),
    )


def initialize_tables() -> None:
    initialize_schema()
    _initialize_metadata_table()
    _initialize_state_table()
    _initialize_severity_cvss20_table()
    _initialize_severity_cvss31_table()
    _initialize_verification_table()
    _initialize_verification_vuln_ids_table()
