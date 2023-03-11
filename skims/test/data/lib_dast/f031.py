from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    policy = (
        '{"Version":"2008-10-17",'
        '"Statement":['
        '{"Effect":"Allow","Action":["iam:PassRole",],"Resource":"*",},'
        '{"Effect":"Allow","Action":"*","Resource":"*",},'
        '{"Effect":"Allow","Action":["ssm:*",],"Resource":"*",},'
        '{"Effect":"Allow","NotAction":"*","NotResource":["iam:bucket",],},'
        "],}"
    )
    vpc_policy = (
        '{"Version":"2008-10-17",'
        '"Statement":['
        '{"Principal": {"AWS":"*"}, "Resource": "*"}'
        "]}"
    )
    statement = '[{"Effect":"Allow","Action":["*"],"Resource":"*",},]'
    return {
        "Policies": [
            {
                "PolicyName": "unsafePol",
                "PolicyId": "pol-018de572ae43404d8",
                "Arn": "arn:aws:iam::aws:policy/AdministratorAccess",
                "Path": "server-certificate/ProdServerCert",
                "DefaultVersionId": "pol-018",
                "AttachmentCount": 1,
                "PermissionsBoundaryUsageCount": 1,
                "IsAttachable": True,
                "Description": "string",
                "CreateDate": "2015/01/01",
                "UpdateDate": "2015/01/01",
            },
        ],
        "PolicyVersion": {
            "Document": policy,
        },
        "Buckets": [
            {
                "Name": "bucket-018de572ae43404d8",
            }
        ],
        "Owner": {"DisplayName": "string", "ID": "string"},
        "Grants": [
            {
                "Grantee": {
                    "DisplayName": "string",
                    "EmailAddress": "string",
                    "ID": "string",
                    "Type": "CanonicalUser",
                    "URI": "http://acs.amazonaws.com/groups/global/AllUsers",
                },
                "Permission": "FULL_CONTROL",
            },
        ],
        "Roles": [
            {
                "RoleName": "rol-018de572ae43404d8",
                "Arn": "arn:aws:iam::aws:user/rol1",
            }
        ],
        "PolicyNames": [
            "inlinePolicy1",
        ],
        "PolicyDocument": {
            "Statement": statement,
        },
        "Users": [
            {
                "UserName": "bucket-018de572ae43404d8",
                "Arn": "arn:aws:iam::aws:user/user1",
            }
        ],
        "AttachedPolicies": [
            {"PolicyName": "inlinePolicy1", "PolicyArn": "policyArn"},
        ],
        "AccessKeyMetadata": [
            {
                "Status": True,
            },
        ],
        "VpcEndpoints": [
            {
                "VpcEndpointId": "vpcEndPoint1",
                "VpcEndpointType": "GatewayLoadBalancer",
                "VpcId": "vpcEndPoint1",
                "PolicyDocument": vpc_policy,
            }
        ],
    }
