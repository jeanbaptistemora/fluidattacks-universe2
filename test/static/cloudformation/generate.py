#! /usr/bin/env python3
"""Generate CloudFormation tests."""

# pylint: disable=E0401
# pylint: disable=C0103
# pylint: disable=W0621
# pylint: disable=too-many-lines

import os
import textwrap
import troposphere
import troposphere.s3
import troposphere.ec2
import troposphere.fsx
import troposphere.iam
import troposphere.kms
import troposphere.rds
import troposphere.dynamodb
import troposphere.cloudfront
import troposphere.elasticloadbalancing
import troposphere.elasticloadbalancingv2
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
        target_file_path: str = os.path.join(target_dir_path,
                                             f'template.{extension}')
        print(target_file_path)
        content: str = getattr(template, f'to_{extension}')(**kwargs)
        print(textwrap.indent(content, prefix='+   '))
        with open(target_file_path, 'w') as target_file_handle:
            target_file_handle.write(content)


#
# Safe
#

template = troposphere.Template(Description='safe', )
role = troposphere.iam.Role(
    title='role1',
    AssumeRolePolicyDocument={
        'Version':
        '2012-10-17',
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
            {
                'Effect': 'Allow',
                'Action': [
                    'rds:DeleteDBCluster',
                ],
                'Resource': [
                    'arn:aws:rds:*:*:db/*',
                ],
            },
            {
                'Effect': 'Deny',
                'Action': [
                    'rds:*',
                ],
                'Resource': [
                    '*',
                ],
            },
            {
                'Effect': 'Allow',
                'Action': [
                    'rds:DescribeAccountAttributes*',
                ],
                'Resource': [
                    '*',
                ],
            },
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
                'Version':
                '2012-10-17',
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
rds_db_subnet_group = troposphere.rds.DBSubnetGroup(
    title='DbSubnetGroup',
    DBSubnetGroupDescription='DbSubnetGroupDescription',
    SubnetIds=[
        'sn-123',
    ],
)
rds_cluster = troposphere.rds.DBCluster(
    title='cluster1',
    Engine='postgres',
    StorageEncrypted=True,
    BackupRetentionPeriod=32,
    DeletionProtection='true',
    DBSubnetGroupName=troposphere.Ref(rds_db_subnet_group),
    EnableIAMDatabaseAuthentication=True,
)
rds_instance = troposphere.rds.DBInstance(
    title='instance1',
    DBInstanceClass='t3.nano',
    EnableIAMDatabaseAuthentication=True,
    DBSubnetGroupName=troposphere.Ref(rds_db_subnet_group),
    Engine='postgres',
    MasterUsername='user',
    MasterUserPassword='pass',
    StorageEncrypted=True,
    BackupRetentionPeriod='32',
    PubliclyAccessible='false',
    DeletionProtection=True,
)
policy = troposphere.iam.PolicyType(
    title='policy1',
    PolicyName='policy1',
    PolicyDocument={
        'Version':
        '2012-10-17',
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
    Users=[],
)
managed_policy = troposphere.iam.ManagedPolicy(
    title='mangedPolicy1',
    PolicyDocument={
        'Version':
        '2012-10-17',
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
    Users=[],
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
    KeyPolicy={},
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
ec2_launch_template = troposphere.ec2.LaunchTemplate(
    title='launchTemplate',
    LaunchTemplateName='launchTemplate',
    LaunchTemplateData=troposphere.ec2.LaunchTemplateData(
        DisableApiTermination=True,
        SecurityGroups=[
            'security-group-test',
        ],
    ),
)
ec2_instance = troposphere.ec2.Instance(
    title='ec2instance1',
    DisableApiTermination=True,
    IamInstanceProfile='iamInstanceProfile1',
    LaunchTemplate=troposphere.ec2.LaunchTemplateSpecification(
        LaunchTemplateId=troposphere.Ref(ec2_launch_template),
        LaunchTemplateName='launchTemplate',
        Version=troposphere.GetAtt('launchTemplate', 'LatestVersionNumber'),
    ),
    NetworkInterfaces=[
        troposphere.ec2.NetworkInterfaceProperty(
            DeviceIndex=0,
            AssociatePublicIpAddress=False,
        ),
    ],
    SecurityGroups=[
        'security-group-test',
    ],
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
    PointInTimeRecoverySpecification=troposphere.dynamodb.
    PointInTimeRecoverySpecification(
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
        title='lustreConfiguration', ),
    KmsKeyId='kms-123',
)
cloudfront_distribution = troposphere.cloudfront.Distribution(
    title='distribution1',
    DistributionConfig=troposphere.cloudfront.DistributionConfig(
        CacheBehaviors=[
            troposphere.cloudfront.CacheBehavior(
                ForwardedValues=troposphere.cloudfront.ForwardedValues(
                    QueryString=False, ),
                TargetOriginId='target-origin-id',
                ViewerProtocolPolicy='redirect-to-https',
                PathPattern='test',
            ),
        ],
        DefaultCacheBehavior=troposphere.cloudfront.DefaultCacheBehavior(
            ForwardedValues=troposphere.cloudfront.ForwardedValues(
                QueryString=False, ),
            TargetOriginId='target-origin-id',
            ViewerProtocolPolicy='redirect-to-https',
        ),
        Enabled=True,
        Logging=troposphere.cloudfront.Logging(
            Bucket='buckettest',
            IncludeCookies=False,
            Prefix='log_'
            ),
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
        Restrictions=troposphere.cloudfront.Restrictions(
            GeoRestriction=troposphere.cloudfront.GeoRestriction(
                Locations=['Colombia'],
                RestrictionType='whitelist'
            )
        ),
        ViewerCertificate=troposphere.cloudfront.ViewerCertificate(
            MinimumProtocolVersion='TLSv1.2_2018', ),
    ),
)
s3_bucket = troposphere.s3.Bucket(
    title='s3Bucket',
    AccessControl='Private',
    LoggingConfiguration=troposphere.s3.LoggingConfiguration(
        LogFilePrefix="log"
    )
)
elb_entity = troposphere.elasticloadbalancing.LoadBalancer(
    title='elasticLoadBalancer',
    AccessLoggingPolicy=troposphere.elasticloadbalancing.AccessLoggingPolicy(
        Enabled=True, ),
    Listeners=[
        troposphere.elasticloadbalancing.Listener(
            InstancePort=443,
            LoadBalancerPort=443,
            Protocol='HTTPS',
        ),
    ],
)
elb2_entity = troposphere.elasticloadbalancingv2.LoadBalancer(
    title='elasticLoadBalancerV2',
    LoadBalancerAttributes=[
        troposphere.elasticloadbalancingv2.LoadBalancerAttributes(
            Key='deletion_protection.enabled',
            Value='true',
        ),
        troposphere.elasticloadbalancingv2.LoadBalancerAttributes(
            Key='access_logs.s3.enabled',
            Value='true',
        ),
    ],
    SubnetMappings=[
        troposphere.elasticloadbalancingv2.SubnetMapping(
            AllocationId='mock',
            SubnetId='mock',
        ),
    ])
elb2_listener = troposphere.elasticloadbalancingv2.Listener(
    title='Elb2Listener',
    Certificates=[],
    DefaultActions=[],
    LoadBalancerArn='loadbal',
    Port=443,
    Protocol='HTTPS',
    SslPolicy='ELBSecurityPolicy-2016-08'
)
ebl2_target_group = troposphere.elasticloadbalancingv2.TargetGroup(
    title='TargetGroup1',
    Name='MyTargets',
    TargetType='ip',
    Port=443,
    Protocol="HTTPS",
    HealthCheckEnabled=True,
    VpcId='test'
)
template.add_resource(role)
template.add_resource(secret)
template.add_resource(rds_cluster)
template.add_resource(rds_instance)
template.add_resource(policy)
template.add_resource(managed_policy)
template.add_resource(user)
template.add_resource(key)
template.add_resource(security_group)
template.add_resource(ec2_volume)
template.add_resource(ec2_volume2)
template.add_resource(ec2_instance)
template.add_resource(ec2_launch_template)
template.add_resource(dynamodb_table)
template.add_resource(ebl2_target_group)
template.add_resource(elb2_listener)
template.add_resource(fsx_filesystem)
template.add_resource(cloudfront_distribution)
template.add_resource(s3_bucket)
template.add_resource(elb_entity)
template.add_resource(elb2_entity)
write_template(template)

#
# Vulnerable
#

template = troposphere.Template(Description='vulnerable', )
role = troposphere.iam.Role(
    title='role1',
    AssumeRolePolicyDocument={
        'Version':
        '2012-10-17',
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
                'NotAction': [],
            },
            {
                # F6: IAM role should not allow Allow+NotPrincipal in its trust
                #   policy
                'Effect': 'Allow',
                'NotPrincipal': [],
            },
            {
                'Effect': 'Allow',
                'Action': [
                    'rds:StopDBCluster',
                ],
                'Resource': '*',
            },
            {
                'Effect': 'Allow',
                'Action': [
                    'ec2:*KeyPair',
                ],
                'Resource': '*',
            },
            {
                'Effect': 'Allow',
                'Action': [
                    'ec2:*',
                ],
                'Resource': '*',
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
                'Version':
                '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        # F3: IAM role should not allow * action on its
                        #   permissions policy
                        'Action': [
                            'ecr:*',
                            'ssm:*',
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
                        'Action': 'iam:ListUsers',
                        'Resource': '*',
                    },
                    {
                        'Effect': 'Allow',
                        'Action': 'ecr:*',
                        'Resource': '*',
                    },
                    {
                        # W15: IAM role should not allow Allow+NotAction
                        'Effect': 'Allow',
                        'NotAction': [],
                    },
                    {
                        # W21: IAM role should not allow Allow+NotResource
                        'Effect': 'Allow',
                        'NotResource': [],
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
secret2 = troposphere.secretsmanager.Secret(title='secret2', )
rds_cluster = troposphere.rds.DBCluster(
    title='cluster1',
    Engine='postgres',
    StorageEncrypted=False,
    # Disables automated back-ups
    BackupRetentionPeriod=0,
    DeletionProtection='false',
)
rds_cluster2 = troposphere.rds.DBCluster(
    title='cluster2',
    Engine='postgres',
    BackupRetentionPeriod=troposphere.If('prod', 32, 0),
)
rds_instance = troposphere.rds.DBInstance(
    title='instance1',
    DBInstanceClass='t3.nano',
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
        'Version':
        '2012-10-17',
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
                'NotAction': [],
            },
            {
                # W22: IAM managed policy should not allow Allow+NotResource
                'Effect': 'Allow',
                'NotResource': [],
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
        'Version':
        '2012-10-17',
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
                'NotAction': [],
            },
            {
                # W23: IAM managed policy should not allow Allow+NotResource
                'Effect': 'Allow',
                'NotResource': [],
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
        "Version": "2012-10-17",
        "Id": "key-default-1",
        "Statement": [
            {
                "Sid": "Enable IAM User Permissions",
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": "kms:*",
                "Resource": "*"
            },
        ]
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
            'IpProtocol': 'tcp',
            'CidrIp': '10.0.0.0/8',
            'FromPort': 69,
            'ToPort': 69
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
ec2_launch_template = troposphere.ec2.LaunchTemplate(
    title='launchTemplate',
    LaunchTemplateName='launchTemplate',
    LaunchTemplateData=troposphere.ec2.LaunchTemplateData(
        DisableApiTermination=False,
        InstanceInitiatedShutdownBehavior='terminate',
    ))
ec2_launch_template2 = troposphere.ec2.LaunchTemplate(
    title='launchTemplate2',
    LaunchTemplateName='launchTemplate2',
)
ec2_instance = troposphere.ec2.Instance(
    title='ec2instance1',
    DisableApiTermination=False,
    LaunchTemplate=troposphere.ec2.LaunchTemplateSpecification(
        LaunchTemplateId=troposphere.Ref(ec2_launch_template),
        LaunchTemplateName='launchTemplate',
        Version=troposphere.GetAtt('launchTemplate', 'LatestVersionNumber'),
    ),
    NetworkInterfaces=[
        troposphere.ec2.NetworkInterfaceProperty(
            DeviceIndex=0,
            AssociatePublicIpAddress=True,
        ),
    ],
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
    PointInTimeRecoverySpecification=troposphere.dynamodb.
    PointInTimeRecoverySpecification(
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
        title='lustreConfiguration', ))
cloudfront_distribution = troposphere.cloudfront.Distribution(
    title='distribution1',
    DistributionConfig=troposphere.cloudfront.DistributionConfig(
        CacheBehaviors=[
            troposphere.cloudfront.CacheBehavior(
                ForwardedValues=troposphere.cloudfront.ForwardedValues(
                    QueryString=False, ),
                TargetOriginId='target-origin-id',
                ViewerProtocolPolicy='allow-all',
                PathPattern='test',
            ),
        ],
        DefaultCacheBehavior=troposphere.cloudfront.DefaultCacheBehavior(
            ForwardedValues=troposphere.cloudfront.ForwardedValues(
                QueryString=False, ),
            TargetOriginId='target-origin-id',
            ViewerProtocolPolicy='allow-all',
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
        Restrictions=troposphere.cloudfront.Restrictions(
            GeoRestriction=troposphere.cloudfront.GeoRestriction(
                Locations=['Colombia'],
                RestrictionType='none'
            )
        ),
        ViewerCertificate=troposphere.cloudfront.ViewerCertificate(
            MinimumProtocolVersion='TLSv1.1_2016', ),
    ),
)
s3_bucket = troposphere.s3.Bucket(
    title='s3Bucket',
    AccessControl='PublicReadWrite',
)
elb_entity = troposphere.elasticloadbalancing.LoadBalancer(
    title='elasticLoadBalancer',
    AccessLoggingPolicy=troposphere.elasticloadbalancing.AccessLoggingPolicy(
        Enabled=False, ),
    Listeners=[
        troposphere.elasticloadbalancing.Listener(
            InstancePort=443,
            LoadBalancerPort=443,
            Protocol='HTTPS',
        ),
    ],
)
elb2_entity = troposphere.elasticloadbalancingv2.LoadBalancer(
    title='elasticLoadBalancerV2',
    LoadBalancerAttributes=[
        troposphere.elasticloadbalancingv2.LoadBalancerAttributes(
            Key='deletion_protection.enabled',
            Value='false',
        ),
        troposphere.elasticloadbalancingv2.LoadBalancerAttributes(
            Key='access_logs.s3.enabled',
            Value='false',
        ),
    ],
    SubnetMappings=[
        troposphere.elasticloadbalancingv2.SubnetMapping(
            AllocationId='mock',
            SubnetId='mock',
        ),
    ])
elb2_listener = troposphere.elasticloadbalancingv2.Listener(
    title='Elb2Listener',
    Certificates=[],
    DefaultActions=[],
    LoadBalancerArn='loadbal',
    Port=443,
    Protocol='HTTPS',
    SslPolicy='ELBSecurityPolicy-TLS-1-0-2015-04'
)
ebl2_target_group = troposphere.elasticloadbalancingv2.TargetGroup(
    title='TargetGroup1',
    Name='MyTargets',
    TargetType='ip',
    Port=80,
    Protocol="HTTP",
    HealthCheckEnabled=False,
    VpcId='Test'
)
template.add_resource(role)
template.add_resource(secret)
template.add_resource(secret2)
template.add_resource(rds_cluster)
template.add_resource(rds_cluster2)
template.add_resource(rds_instance)
template.add_resource(policy)
template.add_resource(managed_policy)
template.add_resource(user)
template.add_resource(key)
template.add_resource(security_group)
template.add_resource(security_group_ingress)
template.add_resource(security_group_egress)
template.add_resource(ec2_volume)
template.add_resource(ec2_instance)
template.add_resource(ec2_launch_template)
template.add_resource(ec2_launch_template2)
template.add_resource(dynamodb_table)
template.add_resource(dynamodb_table2)
template.add_resource(ebl2_target_group)
template.add_resource(fsx_filesystem)
template.add_resource(cloudfront_distribution)
template.add_resource(s3_bucket)
template.add_resource(elb_entity)
template.add_resource(elb2_entity)
template.add_resource(elb2_listener)
write_template(template)

#
# Code as data
#

# Safe

template = troposphere.Template(Description='code_as_data_safe', )

param_ip_security_group = troposphere.Parameter(
    'IpSecurityGroup',
    Description="Ip of SecurityGroup",
    Type="String",
    Default="111.123.123.0/32")
template.add_parameter(param_ip_security_group)

security_group = troposphere.ec2.SecurityGroup(
    title='securityGroup1',
    GroupDescription='groupDescription1',
    SecurityGroupIngress=[{
        'IpProtocol': 'tcp',
        'CidrIp': troposphere.Ref(param_ip_security_group),
        'FromPort': 22,
        'ToPort': 22
    }, {
        'IpProtocol': 'tcp',
        'CidrIp': '32.45.123.0/32',
        'FromPort': 22,
        'ToPort': 22
    }, {
        'IpProtocol': 'udp',
        'CidrIpv6': '2001:db8:a0b:12f0::64/128',
        'FromPort': 22,
        'ToPort': 22
    }])

security_group2 = troposphere.ec2.SecurityGroup(
    title='securityGroup2',
    GroupDescription='groupDescription1',
    SecurityGroupIngress=[{
        'IpProtocol': 'tcp',
        'CidrIp': '20.123.123.0/32',
        'FromPort': 22,
        'ToPort': 22
    }],
    SecurityGroupEgress=[{
        'IpProtocol': 'tcp',
        'CidrIp': '127.0.0.1/32',
        'FromPort': 8000,
        'ToPort': 8000
    }])

security_group_egress = troposphere.ec2.SecurityGroupEgress(
    title='securityGroupEgress1',
    IpProtocol='tcp',
    FromPort=22,
    ToPort=22,
    GroupId=troposphere.Ref(security_group),
    DestinationSecurityGroupId=troposphere.GetAtt('securityGroup1', 'GroupId'))
volume_1 = troposphere.ec2.Volume(
    title='volume1',
    VolumeType='gp2',
    AvailabilityZone=troposphere.Ref('AWS::Region'),
    Encrypted=True,
    Size=120
)
template.add_resource(volume_1)
template.add_resource(security_group)
template.add_resource(security_group2)
template.add_resource(security_group_egress)
write_template(template)

# vulnerable
template = troposphere.Template(Description='code_as_data_vulnerable')

param_ip_security_group = troposphere.Parameter(
    'IpSecurityGroup',
    Description="Ip of SecurityGroup",
    Type="String",
    Default="10.0.0.0/8")
param_insecure_ip_protocol = troposphere.Parameter(
    'IpInsecureProtocol',
    Description="Insecure ip protocol",
    Type="String",
    Default="-1")
param_disable = troposphere.Parameter(
    'DisableFeature',
    Type='String',
    Default=False)
param_terminate = troposphere.Parameter(
    'TerminateInstance',
    Type='String',
    Default='terminate')
param_enable_public_ip = troposphere.Parameter(
    'EnablePublicIp',
    Type='Boolean',
    Default=True)
param_backup_period = troposphere.Parameter(
    'BackupPeriod',
    Type='Integer',
    Default=0)
template.add_parameter(param_disable)
template.add_parameter(param_ip_security_group)
template.add_parameter(param_insecure_ip_protocol)
template.add_parameter(param_terminate)
template.add_parameter(param_enable_public_ip)
template.add_parameter(param_backup_period)

security_group1 = troposphere.ec2.SecurityGroup(
    title='securityGroup1',
    GroupDescription='groupDescription1',
    SecurityGroupIngress=[{
        'IpProtocol': '-1',
        'CidrIp': '0.0.0.0/0',
        'FromPort': 1,
        'ToPort': 65535
    }, {
        'IpProtocol': '-1',
        'CidrIp': troposphere.Ref(param_ip_security_group),
        'FromPort': 1,
        'ToPort': 65535
    }, {
        'IpProtocol': troposphere.Ref(param_insecure_ip_protocol),
        'CidrIpv6': '::/0',
        'FromPort': 1,
        'ToPort': 65535
    }])
security_group2 = troposphere.ec2.SecurityGroup(
    title='securityGroup2',
    GroupDescription='groupDescription2')
security_group_egress1 = troposphere.ec2.SecurityGroupEgress(
    title='securityGroupEgress1',
    IpProtocol='-1',
    FromPort=22,
    ToPort=8080,
    CidrIp='34.229.161.227/16',
    GroupId=troposphere.Ref(security_group2))
security_group_ingress1 = troposphere.ec2.SecurityGroupIngress(
    title='securityGroupIngress1',
    IpProtocol=troposphere.Ref(param_insecure_ip_protocol),
    FromPort=22,
    ToPort=8080,
    CidrIp='110.229.161.227/16',
    GroupName='securityGroup2',
    GroupId=troposphere.Ref(security_group2))
security_group_ingress2 = troposphere.ec2.SecurityGroupIngress(
    title='securityGroupIngress2',
    IpProtocol='-1',
    FromPort=22,
    ToPort=8080,
    CidrIp=troposphere.Ref(param_ip_security_group),
    GroupName='securityGroup2')
volume_1 = troposphere.ec2.Volume(
    title='volume1',
    VolumeType='gp2',
    AvailabilityZone=troposphere.Ref('AWS::Region'),
    Encrypted=False,
    Size=120
)
volume_2 = troposphere.ec2.Volume(
    title='volume2',
    VolumeType='gp2',
    AvailabilityZone=troposphere.Ref('AWS::Region'),
    Encrypted=troposphere.Ref(param_disable),
    Size=120
)
ec2_instance1 = troposphere.ec2.Instance(
    title='ec2instance1',
    DisableApiTermination=False,
    NetworkInterfaces=[
        troposphere.ec2.NetworkInterfaceProperty(
            DeviceIndex=0,
            AssociatePublicIpAddress=troposphere.Ref(param_enable_public_ip))])
ec2_instance2 = troposphere.ec2.Instance(
    title='ec2instance2',
    IamInstanceProfile='iamInstanceProfile1',
    LaunchTemplate=troposphere.ec2.LaunchTemplateSpecification(
        LaunchTemplateId=troposphere.Ref(ec2_launch_template),
        LaunchTemplateName='launchTemplate',
        Version=troposphere.GetAtt('launchTemplate', 'LatestVersionNumber'),
    ),
    NetworkInterfaces=[
        troposphere.ec2.NetworkInterfaceProperty(
            DeviceIndex=0,
            AssociatePublicIpAddress=True,
        ),
    ],
    SecurityGroups=[
        'security-group-test',
    ])
ec2_instance3 = troposphere.ec2.Instance(
    InstanceInitiatedShutdownBehavior=troposphere.Ref(param_terminate),
    title='ec2instance3')
ec2_instance4 = troposphere.ec2.Instance(
    title='ec2instance4',
    InstanceInitiatedShutdownBehavior='terminate',
    DisableApiTermination=troposphere.Ref(param_disable))
ec2_launch_template1 = troposphere.ec2.LaunchTemplate(
    title='launchTemplate1',
    LaunchTemplateName='launchTemplate1',
    LaunchTemplateData=troposphere.ec2.LaunchTemplateData(
        DisableApiTermination=troposphere.Ref(param_disable),
        InstanceInitiatedShutdownBehavior='terminate',
    ))
rds_cluster1 = troposphere.rds.DBCluster(
    title='cluster1',
    Engine='postgres',
    StorageEncrypted=False,
    BackupRetentionPeriod=troposphere.Ref(param_backup_period),
    DeletionProtection='true')
rds_cluster2 = troposphere.rds.DBCluster(
    title='cluster2',
    Engine='postgres',
    StorageEncrypted=troposphere.Ref(param_disable),
    BackupRetentionPeriod=0,
    DeletionProtection='true')

template.add_resource(security_group1)
template.add_resource(security_group2)
template.add_resource(security_group_egress1)
template.add_resource(security_group_ingress1)
template.add_resource(security_group_ingress2)
template.add_resource(volume_1)
template.add_resource(volume_2)
template.add_resource(ec2_instance1)
template.add_resource(ec2_instance2)
template.add_resource(ec2_instance3)
template.add_resource(ec2_instance4)
template.add_resource(ec2_launch_template)
template.add_resource(ec2_launch_template1)
template.add_resource(ec2_launch_template2)
template.add_resource(rds_cluster1)
template.add_resource(rds_cluster2)
write_template(template)
