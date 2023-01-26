from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "LoadBalancers": [
            {
                "LoadBalancerArn": "arn:aws:iam::aws:loadbalancer/lbv2",
                "DNSName": "myDNSname",
                "CanonicalHostedZoneId": "0:0/",
                "CreatedTime": "2015/01/01",
                "LoadBalancerName": "myname",
                "Scheme": "internet-facing",
                "VpcId": "string",
                "State": {"Code": "active", "Reason": "string"},
                "Type": "application",
                "IpAddressType": "ipv4",
                "CustomerOwnedIpv4Pool": "string",
            },
        ],
        "Attributes": [
            {
                "Key": "access_logs.s3.enabled",
                "Value": "false",
            },
            {
                "Key": "deletion_protection.enabled",
                "Value": "false",
            },
        ],
        "DistributionList": {
            "Marker": "string",
            "NextMarker": "string",
            "MaxItems": 1,
            "IsTruncated": True,
            "Quantity": 1,
            "Items": [
                {
                    "Id": "dl-018de572ae43404d8",
                    "ARN": "arn:aws:iam::aws:loadbalancer/",
                    "Status": "string",
                    "DomainName": "string",
                }
            ],
        },
        "Distribution": {
            "Id": "dist-018de572ae43404d8",
            "ARN": "arn:aws:iam::aws:distribution/",
            "Status": "on",
            "DistributionConfig": {
                "Logging": {
                    "Enabled": False,
                    "IncludeCookies": True,
                },
            },
        },
        "DistributionConfig": {
            "Logging": {
                "Enabled": False,
                "IncludeCookies": True,
            },
        },
        "trailList": [
            {
                "Name": "mytrailList",
                "IncludeGlobalServiceEvents": False,
                "IsMultiRegionTrail": False,
                "HomeRegion": "us-east",
                "TrailARN": "arn:aws:iam::aws:trailList/mytrail",
                "LogFileValidationEnabled": False,
            },
        ],
        "Buckets": [
            {
                "Name": "myBucketName",
            },
        ],
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
                        "Monitoring": {
                            "State": "unavailable",
                        },
                    },
                ],
                "OwnerId": "owner_123",
            },
        ],
    }
