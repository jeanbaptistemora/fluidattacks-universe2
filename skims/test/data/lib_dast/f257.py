from typing import (
    Any,
)


def mock_data() -> dict[str, Any]:
    return {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "123",
                    }
                ],
                "OwnerId": "fluidattacks",
            }
        ],
        "DisableApiTermination": {
            "Value": False,
        },
    }
