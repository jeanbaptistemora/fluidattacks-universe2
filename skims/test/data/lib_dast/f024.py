from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "SecurityGroups": [
            {
                "Description": "mygroup",
                "GroupName": "sec1",
                "IpPermissions": [
                    {
                        "FromPort": 88,
                        "IpProtocol": "-1",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0",
                            },
                        ],
                        "Ipv6Ranges": [
                            {
                                "CidrIpv6": "string",
                            },
                        ],
                        "PrefixListIds": [],
                        "ToPort": 8001,
                        "UserIdGroupPairs": [
                            {
                                "GroupId": "sg-018de572ae43404d8",
                                "UserId": "fluidattacks",
                            },
                        ],
                    },
                ],
                "OwnerId": "dev",
                "GroupId": "sg-018de572ae43404d8",
                "IpPermissionsEgress": [
                    {
                        "FromPort": 123,
                        "IpProtocol": "-1",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0",
                            },
                        ],
                        "Ipv6Ranges": [
                            {
                                "CidrIpv6": "0:0:0:0/0",
                            },
                        ],
                        "PrefixListIds": [],
                        "ToPort": 123,
                        "UserIdGroupPairs": [],
                    },
                ],
                "Tags": [
                    {"Key": "security", "Value": "test"},
                ],
                "VpcId": "vpc-0d95ded12635e8383",
            },
        ],
        "NextToken": "456789",
    }
