# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import json
import os
from typing import (
    Any,
)

DATA: dict[str, Any] = json.loads(os.environ["DATA"])


def main() -> None:
    print(
        json.dumps(
            {
                name: {
                    **values,
                    "environment": [
                        {
                            "Name": var,
                            "Value": os.environ[var],
                        }
                        for var in values["environment"]
                    ],
                }
                for name, values in DATA.items()
            },
            separators=(",", ":"),
        )
    )


main()
