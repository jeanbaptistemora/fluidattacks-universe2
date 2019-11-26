#! /usr/bin/env python3

"""Generate CloudFormation tests."""

import os
import textwrap
import troposphere
import troposphere.ec2
import troposphere.fsx
import troposphere.iam
import troposphere.kms
import troposphere.rds
import troposphere.dynamodb
import troposphere.cloudfront
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
                'Effect': 'Deny',
                'Action': '*',
                'Resource': '*',
            },
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
                        'Effect': 'Deny',
                        'Action': '*',
                        'Resource': '*',
                    },
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
    PubliclyAccessible='false',
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
key = troposphere.kms.Key(
    title='key1',
    KeyPolicy={
    },
    EnableKeyRotation='true',
)
security_group = troposphere.ec2.SecurityGroup(
    title='securityGroup1',
    GroupDescription='groupDescription1',
    SecurityGroupEgress=[
        {
            'IpProtocol': 'tcp',
            'CidrIp': '127.0.0.1/32',
            'FromPort': 8000,
            'ToPort': 8000,
        },
    ],
)
ec2_volume = troposphere.ec2.Volume(
    title='ec2Volume1',
    AvailabilityZone='us-east-1',
)
ec2_volume2 = troposphere.ec2.Volume(
    title='ec2Volume2',
    AvailabilityZone='us-east-1',
    Encrypted=troposphere.Join('', ['tr', 'ue']),
)
ec2_instance = troposphere.ec2.Instance(
    title='ec2instance1',
    IamInstanceProfile='iamInstanceProfile1',
)
dynamodb_table = troposphere.dynamodb.Table(
    title='dynamoDBTable1',
    AttributeDefinitions=[
        troposphere.dynamodb.AttributeDefinition(
            title='attributeDefinition1',
            AttributeName='columnA',
            AttributeType='S',
        ),
    ],
    KeySchema=[
        troposphere.dynamodb.KeySchema(
            title='keySchema1',
            AttributeName='columnA',
            KeyType='HASH',
        ),
    ],
    BillingMode='PAY_PER_REQUEST',
    PointInTimeRecoverySpecification=\
        troposphere.dynamodb.PointInTimeRecoverySpecification(
            title='pointInTimeRecoverySpecification1',
            PointInTimeRecoveryEnabled=True,
        ),
)
fsx_filesystem = troposphere.fsx.FileSystem(
    title='fileSystem1',
    FileSystemType='LUSTRE',
    SubnetIds=[
        'sn-123',
    ],
    LustreConfiguration=troposphere.fsx.LustreConfiguration(
        title='lustreConfiguration',
    ),
    KmsKeyId='kms-123',
)
cloudfront_distribution = troposphere.cloudfront.Distribution(
    title='distribution1',
    DistributionConfig=troposphere.cloudfront.DistributionConfig(
        DefaultCacheBehavior=troposphere.cloudfront.DefaultCacheBehavior(
            ForwardedValues=troposphere.cloudfront.ForwardedValues(
                QueryString=False,
            ),
            TargetOriginId='target-origin-id',
            ViewerProtocolPolicy='redirect-to-https',
        ),
        Enabled=True,
        Origins=[
            troposphere.cloudfront.Origin(
                DomainName='domain-name',
                Id='id',
                CustomOriginConfig=troposphere.cloudfront.CustomOriginConfig(
                    OriginProtocolPolicy='https-only',
                    OriginSSLProtocols=[
                        'TLSv1.2',
                    ],
                ),
            ),
        ],
        ViewerCertificate=troposphere.cloudfront.ViewerCertificate(
            MinimumProtocolVersion='TLSv1.2_2018',
        ),
    ),
)
template.add_resource(role)
template.add_resource(secret)
template.add_resource(cluster)
template.add_resource(instance)
template.add_resource(policy)
template.add_resource(managed_policy)
template.add_resource(user)
template.add_resource(key)
template.add_resource(security_group)
template.add_resource(ec2_volume)
template.add_resource(ec2_volume2)
template.add_resource(ec2_instance)
template.add_resource(dynamodb_table)
template.add_resource(fsx_filesystem)
template.add_resource(cloudfront_distribution)
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
secret2 = troposphere.secretsmanager.Secret(
    title='secret2',
)
cluster = troposphere.rds.DBCluster(
    title='cluster1',
    Engine='postgres',
    StorageEncrypted=False,
    # Disables automated back-ups
    BackupRetentionPeriod=0,
)
cluster2 = troposphere.rds.DBCluster(
    title='cluster2',
    Engine='postgres',
    BackupRetentionPeriod=troposphere.If('prod', 32, 0),
)
instance = troposphere.rds.DBInstance(
    title='instance1',
    DBInstanceClass='t2.micro',
    Engine='postgres',
    MasterUsername='user',
    MasterUserPassword='pass',
    StorageEncrypted=False,
    BackupRetentionPeriod='0',
    PubliclyAccessible='true',
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
                'Effect': 'Deny',
                'Action': '*',
                'Resource': '*',
            },
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
key = troposphere.kms.Key(
    title='key1',
    KeyPolicy={
    },
    EnableKeyRotation='false',
)
security_group = troposphere.ec2.SecurityGroup(
    title='securityGroup1',
    GroupDescription='groupDescription1',
    SecurityGroupIngress=[
        {
            'IpProtocol': '-1',
            'CidrIp': '0.0.0.0/0',
            'FromPort': 1,
            'ToPort': 65535
        },
        {
            'IpProtocol': '-1',
            'CidrIpv6': '::/0',
            'FromPort': 1,
            'ToPort': 65535
        },
        {
            'IpProtocol': '-1',
            'CidrIp': '123.123.123.0/24',
            'FromPort': 22,
            'ToPort': 22
        },
        {
            'IpProtocol': '-1',
            'CidrIpv6': '2001:db8:a0b:12f0::64/16',
            'FromPort': 22,
            'ToPort': 22
        },
    ],
)
security_group_egress = troposphere.ec2.SecurityGroupEgress(
    title='securityGroupEgress1',
    IpProtocol='-1',
    FromPort=1,
    ToPort=65535,
    GroupId=troposphere.Ref(security_group),
    DestinationSecurityGroupId=troposphere.GetAtt('securityGroup2', 'GroupId'),
)
security_group_ingress = troposphere.ec2.SecurityGroupIngress(
    title='securityGroupIngress1',
    IpProtocol='-1',
    FromPort=1,
    ToPort=65535,
    GroupId=troposphere.GetAtt('securityGroup2', 'GroupId'),
    SourceSecurityGroupId=troposphere.GetAtt('securityGroup1', 'GroupId'),
)
ec2_volume = troposphere.ec2.Volume(
    title='ec2Volume1',
    AvailabilityZone='us-east-1',
    Encrypted='false',
)
ec2_instance = troposphere.ec2.Instance(
    title='ec2instance1',
)
dynamodb_table = troposphere.dynamodb.Table(
    title='dynamoDBTable1',
    AttributeDefinitions=[
        troposphere.dynamodb.AttributeDefinition(
            title='attributeDefinition1',
            AttributeName='columnA',
            AttributeType='S',
        ),
    ],
    KeySchema=[
        troposphere.dynamodb.KeySchema(
            title='keySchema1',
            AttributeName='columnA',
            KeyType='HASH',
        ),
    ],
    BillingMode='PAY_PER_REQUEST',
    PointInTimeRecoverySpecification=\
        troposphere.dynamodb.PointInTimeRecoverySpecification(
            title='pointInTimeRecoverySpecification1',
            PointInTimeRecoveryEnabled=False,
        ),
)
dynamodb_table2 = troposphere.dynamodb.Table(
    title='dynamoDBTable2',
    AttributeDefinitions=[
        troposphere.dynamodb.AttributeDefinition(
            title='attributeDefinition2',
            AttributeName='columnA',
            AttributeType='S',
        ),
    ],
    KeySchema=[
        troposphere.dynamodb.KeySchema(
            title='keySchema2',
            AttributeName='columnA',
            KeyType='HASH',
        ),
    ],
    BillingMode='PAY_PER_REQUEST',
)
fsx_filesystem = troposphere.fsx.FileSystem(
    title='fileSystem1',
    FileSystemType='LUSTRE',
    SubnetIds=[
        'sn-123',
    ],
    LustreConfiguration=troposphere.fsx.LustreConfiguration(
        title='lustreConfiguration',
    )
)
cloudfront_distribution = troposphere.cloudfront.Distribution(
    title='distribution1',
    DistributionConfig=troposphere.cloudfront.DistributionConfig(
        DefaultCacheBehavior=troposphere.cloudfront.DefaultCacheBehavior(
            ForwardedValues=troposphere.cloudfront.ForwardedValues(
                QueryString=False,
            ),
            TargetOriginId='target-origin-id',
            ViewerProtocolPolicy='redirect-to-https',
        ),
        Enabled=True,
        Origins=[
            troposphere.cloudfront.Origin(
                DomainName='domain-name',
                Id='id',
                CustomOriginConfig=troposphere.cloudfront.CustomOriginConfig(
                    OriginProtocolPolicy='https-only',
                    OriginSSLProtocols=[
                        'SSLv3',
                    ],
                ),
            ),
        ],
        ViewerCertificate=troposphere.cloudfront.ViewerCertificate(
            MinimumProtocolVersion='TLSv1.1_2016',
        ),
    ),
)
template.add_resource(role)
template.add_resource(secret)
template.add_resource(secret2)
template.add_resource(cluster)
template.add_resource(cluster2)
template.add_resource(instance)
template.add_resource(policy)
template.add_resource(managed_policy)
template.add_resource(user)
template.add_resource(key)
template.add_resource(security_group)
template.add_resource(security_group_ingress)
template.add_resource(security_group_egress)
template.add_resource(ec2_volume)
template.add_resource(ec2_instance)
template.add_resource(dynamodb_table)
template.add_resource(dynamodb_table2)
template.add_resource(fsx_filesystem)
template.add_resource(cloudfront_distribution)
write_template(template)
