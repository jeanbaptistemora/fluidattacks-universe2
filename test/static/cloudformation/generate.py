#! /usr/bin/env python3

"""Generate CloudFormation tests."""

import os
import textwrap
import troposphere
import troposphere.iam
import troposphere.rds
import troposphere.secretsmanager


def write_template(template: troposphere.Template) -> bool:
    """Write a template to the target file."""
    base_path: str = os.path.abspath(os.path.dirname(__file__))
    target_dir_path: str = os.path.join(base_path, template.description)
    os.makedirs(target_dir_path, exist_ok=True)
    for extension, kwargs in (
            ('yaml', {
                'clean_up': True,
                'long_form': True
            }),
            ('json', {
                'indent': 2
            })):
        target_file_path: str = os.path.join(
            target_dir_path, f'template.{extension}')
        print(target_file_path)
        content: str = getattr(template, f'to_{extension}')(**kwargs)
        print(textwrap.indent(content, prefix='+   '))
        with open(target_file_path, 'w') as target_file_handle:
            target_file_handle.write(content)


#
# Safe
#

template = troposphere.Template(
    Description='safe',
)
role = troposphere.iam.Role(
    title='role1',
    AssumeRolePolicyDocument={
        'Version': '2012-10-17',
        'Statement': [
            {
                'Effect': 'Allow',
                # F2: IAM role should not allow * action on its trust policy
                'Action': [
                    'ecr:Get*',
                ],
                'Resource': [
                    '*',
                ],
            },
            # W14: IAM role should not allow Allow+NotAction on trust
            #   permissions
            # F6: IAM role should not allow Allow+NotPrincipal in its trust
            #   policy
        ],
    },
    ManagedPolicyArns=[
        # W43: IAM role should not have AdministratorAccess policy
    ],
    Policies=[
        troposphere.iam.Policy(
            title='policy1',
            PolicyName='policy1',
            PolicyDocument={
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        # F3: IAM role should not allow * action on its
                        #   permissions policy
                        'Action': [
                            'ecr:Get*',
                        ],
                        # W11: IAM role should not allow * resource on its
                        #   permissions policy
                        # F38: IAM role should not allow * resource with
                        #   PassRole action on its permissions policy
                        'Resource': [
                            'arn:aws:ecr:us-east-1::repository/*',
                        ],
                    },
                    # W15: IAM role should not allow Allow+NotAction
                    # W21: IAM role should not allow Allow+NotResource
                ],
            },
        ),
    ],
)
secret = troposphere.secretsmanager.Secret(
    title='secret1',
    GenerateSecretString=troposphere.secretsmanager.GenerateSecretString(
        title='generateSecretString1',
        ExcludeCharacters='',
        PasswordLength=32,
        ExcludeLowercase=False,
        ExcludeUppercase='false',
        ExcludeNumbers=0,
        ExcludePunctuation='False',
        RequireEachIncludedType='true',
    ),
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
policy = troposphere.iam.PolicyType(
    title='policy1',
    PolicyName='policy1',
    PolicyDocument={
        'Version': '2012-10-17',
        'Statement': [
            {
                # F4: IAM managed policy should not allow * action
                'Effect': 'Allow',
                'Action': [
                    'ecr:Get*',
                ],
                # W12: IAM managed policy should not allow * resource
                # F39: IAM managed policy should not allow a * resource with
                #   PassRole action
                'Resource': [
                    'arn:aws:ecr:us-east-1::repository/*',
                ],
            },
            # W16: IAM managed policy should not allow Allow+NotAction
            # W22: IAM managed policy should not allow Allow+NotResource
        ],
    },
    # F11: IAM managed policy should not apply directly to users.
    #   Should be on group
    Users=[
    ],
)
managed_policy = troposphere.iam.ManagedPolicy(
    title='mangedPolicy1',
    PolicyDocument={
        'Version': '2012-10-17',
        'Statement': [
            {
                # F5: IAM managed policy should not allow * action
                'Effect': 'Allow',
                'Action': [
                    'ecr:Get*',
                ],
                # W13: IAM managed policy should not allow * resource
                # F40: IAM managed policy should not allow a * resource with
                #   PassRole action
                'Resource': [
                    'arn:aws:ecr:us-east-1::repository/*',
                ],
            },
            # W17: IAM managed policy should not allow Allow+NotAction
            # W23: IAM managed policy should not allow Allow+NotResource
        ],
    },
    # F12: IAM managed policy should not apply directly to users.
    #   Should be on group
    Users=[
    ],
)
user = troposphere.iam.User(
    title='user1',
    # F10: IAM user should not have any inline policies.
    #   Should be centralized Policy object on group (Role)
    Groups=[
        'role1',
    ],
)
template.add_resource(role)
template.add_resource(secret)
template.add_resource(cluster)
template.add_resource(instance)
template.add_resource(policy)
template.add_resource(managed_policy)
template.add_resource(user)
write_template(template)

#
# Vulnerable
#

template = troposphere.Template(
    Description='vulnerable',
)
role = troposphere.iam.Role(
    title='role1',
    AssumeRolePolicyDocument={
        'Version': '2012-10-17',
        'Statement': [
            {
                'Effect': 'Allow',
                # F2: IAM role should not allow * action on its trust policy
                'Action': [
                    'ecr:*',
                ],
                'Resource': [
                    '*',
                ],
            },
            {
                # W14: IAM role should not allow Allow+NotAction on trust
                #   permissions
                'Effect': 'Allow',
                'NotAction': [
                ],
            },
            {
                # F6: IAM role should not allow Allow+NotPrincipal in its trust
                #   policy
                'Effect': 'Allow',
                'NotPrincipal': [
                ],
            },
        ],
    },
    ManagedPolicyArns=[
        # W43: IAM role should not have AdministratorAccess policy
        'arn:aws:iam::aws:policy/AdministratorAccess',
    ],
    Policies=[
        troposphere.iam.Policy(
            title='policy1',
            PolicyName='policy1',
            PolicyDocument={
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        # F3: IAM role should not allow * action on its
                        #   permissions policy
                        'Action': [
                            'ecr:*',
                        ],
                        # W11: IAM role should not allow * resource on its
                        #   permissions policy
                        # F38: IAM role should not allow * resource with
                        #   PassRole action on its permissions policy
                        'Resource': [
                            '*',
                        ],
                    },
                    {
                        'Effect': 'Allow',
                        'Action': 'ecr:*',
                        'Resource': '*',
                    },
                    {
                        # W15: IAM role should not allow Allow+NotAction
                        'Effect': 'Allow',
                        'NotAction': [
                        ],
                    },
                    {
                        # W21: IAM role should not allow Allow+NotResource
                        'Effect': 'Allow',
                        'NotResource': [
                        ],
                    },
                ],
            },
        ),
    ],
)
secret = troposphere.secretsmanager.Secret(
    title='secret1',
    GenerateSecretString=troposphere.secretsmanager.GenerateSecretString(
        title='generateSecretString1',
        ExcludeCharacters=('01234567890'
                           'abcdefghijklmnopqrstuvwxyz'
                           'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                           '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'),
        PasswordLength=10,
        ExcludeLowercase=True,
        ExcludeUppercase='true',
        ExcludeNumbers=1,
        ExcludePunctuation='True',
        RequireEachIncludedType='false',
    ),
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
policy = troposphere.iam.PolicyType(
    title='policy1',
    PolicyName='policy1',
    PolicyDocument={
        'Version': '2012-10-17',
        'Statement': [
            {
                # F4: IAM managed policy should not allow * action
                'Effect': 'Allow',
                'Action': [
                    'ecr:*',
                ],
                # W12: IAM managed policy should not allow * resource
                # F39: IAM managed policy should not allow a * resource with
                #   PassRole action
                'Resource': [
                    '*',
                ],
            },
            {
                'Effect': 'Allow',
                'Action': 'ecr:*',
                'Resource': '*',
            },
            {
                # W16: IAM managed policy should not allow Allow+NotAction
                'Effect': 'Allow',
                'NotAction': [
                ],
            },
            {
                # W22: IAM managed policy should not allow Allow+NotResource
                'Effect': 'Allow',
                'NotResource': [
                ],
            },
        ],
    },
    # F11: IAM managed policy should not apply directly to users.
    #   Should be on group
    Users=[
        'user1',
    ],
)
managed_policy = troposphere.iam.ManagedPolicy(
    title='mangedPolicy1',
    PolicyDocument={
        'Version': '2012-10-17',
        'Statement': [
            {
                # F5: IAM managed policy should not allow * action
                'Effect': 'Allow',
                'Action': [
                    'ecr:*',
                ],
                # W13: IAM managed policy should not allow * resource
                # F40: IAM managed policy should not allow a * resource with
                #   PassRole action
                'Resource': [
                    '*',
                ],
            },
            {
                'Effect': 'Allow',
                'Action': 'ecr:*',
                'Resource': '*',
            },
            {
                # W17: IAM managed policy should not allow Allow+NotAction
                'Effect': 'Allow',
                'NotAction': [
                ],
            },
            {
                # W23: IAM managed policy should not allow Allow+NotResource
                'Effect': 'Allow',
                'NotResource': [
                ],
            },
        ],
    },
    # F12: IAM managed policy should not apply directly to users.
    #   Should be on group
    Users=[
        'user1',
    ],
)
user = troposphere.iam.User(
    title='user1',
    # F10: IAM user should not have any inline policies.
    #   Should be centralized Policy object on group (Role)
    Policies=[
        troposphere.Ref(policy),
    ],
)
template.add_resource(role)
template.add_resource(secret)
template.add_resource(cluster)
template.add_resource(instance)
template.add_resource(policy)
template.add_resource(managed_policy)
template.add_resource(user)
write_template(template)
