from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "SecurityGroups": [
            {
                "Description": "myunsafegroup",
                "GroupName": "sec1",
                "IpPermissions": [
                    {
                        "FromPort": 88,
                        "ToPort": 500,
                        "IpProtocol": "-1",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0",
                            },
                        ],
                        "Ipv6Ranges": [
                            {
                                "CidrIpv6": "::/0",
                            },
                        ],
                        "PrefixListIds": [],
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
                        "ToPort": 123,
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
                        "UserIdGroupPairs": [],
                    },
                ],
                "VpcId": "vpc-0d95ded12635e8383",
            },
            {
                "Description": "myunsafegroup_rfc1918",
                "GroupName": "sec1",
                "IpPermissions": [
                    {
                        "FromPort": 1,
                        "ToPort": 2,
                        "IpProtocol": "ftp",
                        "IpRanges": [
                            {
                                "CidrIp": "172.16.0.0/12",
                            },
                        ],
                        "Ipv6Ranges": [
                            {
                                "CidrIpv6": "1:1:1:0/12",
                            },
                        ],
                        "PrefixListIds": [],
                        "UserIdGroupPairs": [
                            {
                                "GroupId": "sg-018de572ae43404d8",
                                "UserId": "fluidattacks",
                            },
                        ],
                    },
                ],
                "OwnerId": "dev",
                "GroupId": "sg-018de572ae43404d9",
                "IpPermissionsEgress": [
                    {
                        "FromPort": 123,
                        "ToPort": 123,
                        "IpProtocol": "2",
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
                        "UserIdGroupPairs": [],
                    },
                ],
                "VpcId": "vpc-0d95ded12635e8384",
            },
            {
                "Description": "myunsafegroup_dns",
                "GroupName": "sec1",
                "IpPermissions": [
                    {
                        "FromPort": 50,
                        "ToPort": 70,
                        "IpProtocol": "udp",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0",
                            },
                        ],
                        "Ipv6Ranges": [
                            {
                                "CidrIpv6": "::/0",
                            },
                        ],
                        "PrefixListIds": [],
                        "UserIdGroupPairs": [
                            {
                                "GroupId": "sg-018de572ae43404d8",
                                "UserId": "fluidattacks",
                            },
                        ],
                    },
                ],
                "OwnerId": "dev",
                "GroupId": "sg-018de572ae43404d10",
                "IpPermissionsEgress": [
                    {
                        "FromPort": 123,
                        "ToPort": 123,
                        "IpProtocol": "2",
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
                        "UserIdGroupPairs": [],
                    },
                ],
                "VpcId": "vpc-0d95ded12635e8385",
            },
            {
                "Description": "myunsafegroup_ftp",
                "GroupName": "sec1",
                "IpPermissions": [
                    {
                        "FromPort": 19,
                        "ToPort": 22,
                        "IpProtocol": "tcp",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0",
                            },
                        ],
                        "Ipv6Ranges": [
                            {
                                "CidrIpv6": "::/0",
                            },
                        ],
                        "PrefixListIds": [],
                        "UserIdGroupPairs": [
                            {
                                "GroupId": "sg-018de572ae43404d11",
                                "UserId": "fluidattacks",
                            },
                        ],
                    },
                ],
                "OwnerId": "dev",
                "GroupId": "sg-018de572ae43404d10",
                "IpPermissionsEgress": [
                    {
                        "FromPort": 123,
                        "ToPort": 123,
                        "IpProtocol": "2",
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
                        "UserIdGroupPairs": [],
                    },
                ],
                "VpcId": "vpc-0d95ded12635e8386",
            },
            {
                "Description": "myunsafegroup_openallports",
                "GroupName": "sec1",
                "IpPermissions": [
                    {
                        "FromPort": 0,
                        "ToPort": 65535,
                        "IpProtocol": "tcp",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0",
                            },
                        ],
                        "Ipv6Ranges": [
                            {
                                "CidrIpv6": "::/0",
                            },
                        ],
                        "PrefixListIds": [],
                        "UserIdGroupPairs": [
                            {
                                "GroupId": "sg-018de572ae43404d11",
                                "UserId": "fluidattacks",
                            },
                        ],
                    },
                ],
                "OwnerId": "dev",
                "GroupId": "sg-018de572ae43404d10",
                "IpPermissionsEgress": [
                    {
                        "FromPort": 0,
                        "ToPort": 65535,
                        "IpProtocol": "2",
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
                        "UserIdGroupPairs": [],
                    },
                ],
                "VpcId": "vpc-0d95ded12635e8386",
            },
            {
                "Description": "myunsafegroup_default",
                "GroupName": "default",
                "IpPermissions": [
                    {
                        "FromPort": 0,
                        "ToPort": 65535,
                        "IpProtocol": "tcp",
                        "IpRanges": [
                            {
                                "CidrIp": "0.0.0.0/0",
                            },
                        ],
                        "Ipv6Ranges": [
                            {
                                "CidrIpv6": "::/0",
                            },
                        ],
                        "PrefixListIds": [],
                        "UserIdGroupPairs": [
                            {
                                "GroupId": "sg-018de572ae43404d11",
                                "UserId": "fluidattacks",
                            },
                        ],
                    },
                ],
                "OwnerId": "dev",
                "GroupId": "sg-018de572ae43404d10",
                "IpPermissionsEgress": [
                    {
                        "FromPort": 0,
                        "ToPort": 65535,
                        "IpProtocol": "2",
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
                        "UserIdGroupPairs": [],
                    },
                ],
                "VpcId": "vpc-0d95ded12635e8386",
            },
        ],
        "Reservations": [
            {
                "Groups": [
                    {"GroupName": "string", "GroupId": "string"},
                ],
                "Instances": [
                    {
                        "AmiLaunchIndex": 123,
                        "ImageId": "string",
                        "InstanceId": "fluidunsafeinstance_234",
                        "State": {
                            "Code": 123,
                            "Name": "pending",
                        },
                    }
                ],
                "OwnerId": "fluid_234",
            }
        ],
    }
