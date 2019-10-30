#! /usr/bin/env python3

"""Generate CloudFormation tests."""

import os
import textwrap
import troposphere
import troposphere.rds


def write_template(template: troposphere.Template) -> bool:
    """Write a template to the target file."""
    base_path: str = os.path.abspath(os.path.dirname(__file__))
    target_dir_path: str = os.path.join(base_path, template.description)
    target_file_path: str = os.path.join(target_dir_path, 'template.yml')

    os.makedirs(target_dir_path, exist_ok=True)

    print(target_file_path)
    content: str = template.to_yaml()
    print(textwrap.indent(content, prefix='+   '))
    with open(target_file_path, 'w') as target_file_handle:
        target_file_handle.write(content)


#
# Safe
#

template = troposphere.Template(
    Description='rds-safe',
)
cluster = troposphere.rds.DBCluster(
    title='cluster1',
    Engine='postgres',
    StorageEncrypted=True,
    BackupRetentionPeriod=32,
)
instance = troposphere.rds.DBInstance(
    title='instance1',
    DBInstanceClass='t2.micro',
    Engine='postgres',
    MasterUsername='user',
    MasterUserPassword='pass',
    StorageEncrypted=True,
    BackupRetentionPeriod='32',
)
template.add_resource(cluster)
template.add_resource(instance)
write_template(template)

#
# Vulnerable
#

template = troposphere.Template(
    Description='rds-vulnerable',
)
cluster = troposphere.rds.DBCluster(
    title='cluster1',
    Engine='postgres',
    StorageEncrypted=False,
    # Disables automated back-ups
    BackupRetentionPeriod=0,
)
instance = troposphere.rds.DBInstance(
    title='instance1',
    DBInstanceClass='t2.micro',
    Engine='postgres',
    MasterUsername='user',
    MasterUserPassword='pass',
    StorageEncrypted=False,
    # Disables automated back-ups
    BackupRetentionPeriod='0',
)
template.add_resource(cluster)
template.add_resource(instance)
write_template(template)
