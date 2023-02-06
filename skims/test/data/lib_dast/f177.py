from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "myinst1",
                        "InstanceType": "a1.medium",
                        "SecurityGroups": [
                            {
                                "GroupName": "default",
                                "GroupId": "sg1-018de572ae43404d8",
                            },
                        ],
                    },
                    {
                        "InstanceId": "myinst2",
                        "InstanceType": "a1.medium",
                        "SecurityGroups": [
                            {
                                "GroupName": "safeGroup",
                                "GroupId": "sg2-018de572ae43404d8",
                            },
                        ],
                    },
                ],
            }
        ],
        "LaunchTemplateVersions": [
            {
                "LaunchTemplateId": "ltid1-018de572ae43404d8",
                "LaunchTemplateName": "fluidtemplateunsafe",
                "LaunchTemplateData": {
                    "EbsOptimized": True,
                },
            },
            {
                "LaunchTemplateId": "ltid2-018de572ae43404d8",
                "LaunchTemplateName": "fluidtemplatesafe",
                "LaunchTemplateData": {
                    "SecurityGroupIds": [
                        "sg-018de572ae43404d8",
                    ],
                    "SecurityGroups": [
                        "fluidsecurity",
                    ],
                },
            },
        ],
    }
