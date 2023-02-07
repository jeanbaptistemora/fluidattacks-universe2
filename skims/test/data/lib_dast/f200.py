from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "Vpcs": [
            {
                "State": "pending",
                "VpcId": "fluidvpc1",
                "OwnerId": "fluidattacks",
                "InstanceTenancy": "default",
            },
        ],
    }
