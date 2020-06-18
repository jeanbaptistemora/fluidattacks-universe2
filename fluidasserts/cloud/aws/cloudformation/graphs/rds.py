"""
AWS CloudFormation checks for ``RDS`` (Relational Database Service).
"""

# Standard imports
from contextlib import suppress
from typing import List
from typing import Tuple
from typing import Union

# 3rd party imports
from neo4j import Result
from neo4j import Session

# Local imports
from fluidasserts import MEDIUM
from fluidasserts import SAST
from fluidasserts.helper.aws import CloudFormationInvalidTypeError
from fluidasserts.cloud.aws.cloudformation import _get_result_as_tuple
from fluidasserts.cloud.aws.cloudformation import Vulnerability
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.db.neo4j_connection import ConnectionString
from fluidasserts.db.neo4j_connection import driver_session
from fluidasserts.helper import aws as helper


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_unencrypted_storage(connection: ConnectionString) -> Tuple:
    """
    Check if any ``DBCluster`` or ``DBInstance`` use unencrypted storage.

    The following checks are performed:

    * F26 RDS DBCluster should have StorageEncrypted enabled
    * F27 RDS DBInstance should have StorageEncrypted enabled

    :param connection: Connection String to neo4j.
    :returns: - ``OPEN`` if **StorageEncrypted** attribute is set to **false**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    queries: List = [
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(db:RDS)
        WHERE (db:DBCluster OR db:DBInstance) AND NOT exists((db)-[*2]->(
            :StorageEncrypted))
        RETURN template.path as path, db.name as resource, db.line as line, [x
         IN labels(db) WHERE x IN ['DBCluster', 'DBInstance']][0] as type
        """,
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(db:RDS)-[*2]->(
            encryption:StorageEncrypted)
        WHERE (db:DBCluster OR db:DBInstance) AND exists((encryption.value))
        RETURN template.path as path, db.name as resource,
            encryption.line as line, encryption.value as encryption, [x
               IN labels(db) WHERE x IN ['DBCluster', 'DBInstance']][0] as type
        """,
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(db:RDS)-[*2]->(
            :StorageEncrypted)-[:REFERENCE]->()-[:HAS*1..2]->(encryption)
        WHERE (db:DBCluster OR db:DBInstance) AND exists((encryption.value))
        RETURN template.path as path, db.name as resource,
            encryption.line as line, encryption.value as encryption, [x
               IN labels(db) WHERE x IN ['DBCluster', 'DBInstance']][0] as type
        """
    ]
    session: Session = driver_session(connection)
    query_result: List[Result] = [
        record for query in queries for record in list(session.run(query))
    ]
    for record in query_result:
        res_storage_encrypted: bool = record.get('encryption', False)

        with suppress(CloudFormationInvalidTypeError):
            res_storage_encrypted = helper.to_boolean(res_storage_encrypted)

        is_vulnerable: bool = not res_storage_encrypted

        if is_vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=record['path'],
                    entity=f'AWS::RDS::{record["type"]}',
                    identifier=record['resource'],
                    line=record['line'],
                    reason='uses unencrypted storage'))
    session.close()
    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS clusters or instances have unencrypted storage',
        msg_closed='RDS clusters or instances have encrypted storage')


@api(risk=MEDIUM, kind=SAST)
@unknown_if(FileNotFoundError)
def has_not_automated_backups(connection: ConnectionString) -> Tuple:
    """
    Check if any ``DBCluster`` or ``DBInstance`` have not automated backups.

    :param connection: Connection String to neo4j.
    :returns: - ``OPEN`` if **BackupRetentionPeriod** attribute is set to 0.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    vulnerabilities: List[Vulnerability] = []
    queries: List[str] = [
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(db:RDS)-[*2]->(
            backup:BackupRetentionPeriod)
            WHERE (db:DBCluster OR db:DBInstance) AND exists(backup.value)
        RETURN template.path as path, backup.line as line,
            backup.value as backup, [x IN labels(db) WHERE x IN ['DBCluster',
                'DBInstance']][0] as type, db.name as resource
        """,
        """
        MATCH (template:CloudFormationTemplate)-[*2]->(db:RDS)-[*2]->(
            :BackupRetentionPeriod)-[:REFERENCE]->()-[:HAS*1..2]->(backup)
            WHERE (db:DBCluster OR db:DBInstance) AND exists(backup.value)
        RETURN template.path as path, backup.line as line,
            backup.value as backup, [x IN labels(db) WHERE x IN ['DBCluster',
                'DBInstance']][0] as type, db.name as resource
        """
    ]
    session: Session = driver_session(connection)
    query_result: List[Result] = [
        record for query in queries for record in list(session.run(query))
    ]
    for record in query_result:
        back_up_retention_period: Union[str, int] = record.get('backup', 1)

        if not helper.is_scalar(back_up_retention_period):
            continue

        is_vulnerable: bool = back_up_retention_period in (0, '0')

        if is_vulnerable:
            vulnerabilities.append(
                Vulnerability(
                    path=record['path'],
                    entity=f'AWS::RDS::{record["type"]}',
                    identifier=record['resource'],
                    line=record['line'],
                    reason='has not automated backups enabled'))
    session.close()
    return _get_result_as_tuple(
        vulnerabilities=vulnerabilities,
        msg_open='RDS cluster or instances have not automated backups enabled',
        msg_closed='RDS cluster or instances have automated backups enabled')
