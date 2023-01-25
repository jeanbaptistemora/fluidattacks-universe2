from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "Reservations": [
            {
                "Groups": [
                    {
                        "GroupName": "mygroup",
                        "GroupId": "gr-018de572ae43404d8",
                    },
                ],
                "Instances": [
                    {
                        "AmiLaunchIndex": 1,
                        "InstanceId": "int-018de572ae43404d8",
                        "ImageId": "img-018de572ae43404d8",
                        "NetworkInterfaces": [
                            {
                                "Association": {"PublicIp": "127.0.0.0"},
                            },
                        ],
                        "State": {
                            "Code": 1,
                            "Name": "pending",
                        },
                    },
                ],
                "OwnerId": "owner_123",
            },
        ],
        "InstanceId": "pol-018de572ae43404d8",
        "InstanceInitiatedShutdownBehavior": {"Value": "terminate"},
        "KeyPairs": [
            {
                "KeyPairId": "kp-018de572ae43404d8",
                "KeyName": "testKey",
                "KeyType": "rsa",
                "PublicKey": "publickey",
                "CreateTime": "2015/05/05",
            },
        ],
        "SecurityGroups": [
            {
                "Description": "An unused security group",
                "GroupName": "UnusedGroup",
                "GroupId": "sg-018de572ae43404d8",
                "OwnerId": "owner-018de572ae43404d8",
            }
        ],
        "Images": [
            {
                "Architecture": "i386",
                "ImageId": "img-018de572ae43404d8",
                "Public": True,
                "BlockDeviceMappings": [
                    {
                        "Ebs": {
                            "Encrypted": False,
                        },
                    },
                ],
                "ImageOwnerAlias": "privateOwner",
            }
        ],
        "Account": "123456789012",
        "Arn": "arn:aws:iam::123456789012:user/fluid",
        "Snapshots": [
            {
                "Encrypted": False,
                "SnapshotId": "snp-018de572ae43404d8",
                "State": "pending",
            },
        ],
    }
