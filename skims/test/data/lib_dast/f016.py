from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "DistributionList": {
            "Marker": "mymarker",
            "MaxItems": 1,
            "IsTruncated": False,
            "Quantity": 1,
            "Items": [
                {
                    "Id": "dl-018de572ae43404d8",
                    "ARN": "arn:aws:iam::aws:distribution/mylist",
                }
            ],
        },
        "Distribution": {
            "Id": "dl-018de572ae43404d8",
            "ARN": "arn:aws:iam::aws:distribution/mylist",
            "DistributionConfig": {
                "CallerReference": "string",
                "Aliases": {
                    "Quantity": 1,
                    "Items": [
                        "item1",
                    ],
                },
                "ViewerCertificate": {
                    "CloudFrontDefaultCertificate": True,
                    "IAMCertificateId": "myiamid",
                    "ACMCertificateArn": "myid",
                    "SSLSupportMethod": "sni-only",
                    "MinimumProtocolVersion": "SSLv3",
                    "Certificate": "string",
                    "CertificateSource": "cloudfront",
                },
                "Origins": {
                    "Quantity": 123,
                    "Items": [
                        {
                            "Id": "domainId",
                            "DomainName": "mydomain",
                            "CustomOriginConfig": {
                                "HTTPPort": 123,
                                "HTTPSPort": 123,
                                "OriginProtocolPolicy": "https-only",
                                "OriginSslProtocols": {
                                    "Quantity": 123,
                                    "Items": [
                                        "TLSv1",
                                    ],
                                },
                                "OriginReadTimeout": 123,
                                "OriginKeepaliveTimeout": 123,
                            },
                            "ConnectionAttempts": 123,
                            "ConnectionTimeout": 123,
                            "OriginShield": {
                                "Enabled": True,
                                "OriginShieldRegion": "string",
                            },
                            "OriginAccessControlId": "string",
                        },
                    ],
                },
            },
        },
        "LoadBalancers": [
            {
                "LoadBalancerArn": "arn:aws:iam::aws:elbv2/fluidelb",
            },
        ],
        "Listeners": [
            {
                "ListenerArn": "arn:aws:iam::aws:listener/fluidlist",
                "LoadBalancerArn": "arn:aws:iam::aws:elbv2/fluidelb",
                "Port": 123,
                "SslPolicy": "fluid_ssl_policy",
            }
        ],
        "SslPolicies": [
            {
                "SslProtocols": [
                    "SSLv3",
                    "TLSv1.2",
                ],
                "Ciphers": [
                    {
                        "Name": "ECDHE-ECDSA-AES128-GCM-SHA256",
                        "Priority": 1,
                    },
                ],
            },
        ],
    }
