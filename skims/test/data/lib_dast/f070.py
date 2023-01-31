from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "TargetGroups": [
            {
                "TargetGroupArn": "arn:aws:iam::123456789012:tg/wrongport",
                "Port": 123,
                "TargetType": "instance",
            },
            {
                "TargetGroupArn": "arn:aws:iam::123456789012:tg/noport",
                "TargetType": "instance",
            },
            {
                "TargetType": "lambda",
                "TargetGroupArn": "arn:aws:iam::123456789012:tg/mytarget1",
            },
            {
                "Port": 443,
                "TargetType": "ip",
                "TargetGroupArn": "arn:aws:iam::123456789012:tg/mytarget2",
            },
        ],
        "LoadBalancers": [
            {
                "LoadBalancerArn": "arn:aws:iam::123456789012:lb/mylb1",
            }
        ],
        "Listeners": [
            {
                "ListenerArn": "arn:aws:iam::123456789012:list/unsafelistener",
                "LoadBalancerArn": "arn:aws:iam::123456789012:lb/mylb1",
                "Port": 123,
                "SslPolicy": "ELBSecurityPolicy-FS-1-2-Res-2019-08",
            },
            {
                "ListenerArn": "arn:aws:iam::123456789012:list/safelistener",
                "LoadBalancerArn": "arn:aws:iam::123456789012:lb/mylb1",
                "Port": 123,
                "SslPolicy": "ELBSecurityPolicy-TLS13-1-2-Res-2021-06",
            },
        ],
    }
