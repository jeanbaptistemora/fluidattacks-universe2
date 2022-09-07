# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import aioboto3
from config import (
    load,
)
import json
from model.core_model import (
    SkimsConfig,
)
import tempfile
from typing import (
    Any,
    Dict,
)


async def get_config(execution_id: str) -> SkimsConfig:
    group = execution_id.split("_")[0]
    session = aioboto3.Session()
    async with session.client("s3") as s3_client:
        with tempfile.NamedTemporaryFile() as temp:
            await s3_client.download_fileobj(
                "skims.data",
                f"configs/{execution_id}.yaml",
                temp,
            )
            temp.seek(0)
            # FP: The function referred to is from another product (reviews)
            return load(group, temp.name)  # NOSONAR


async def get_results(execution_id: str) -> Dict[str, Any]:
    session = aioboto3.Session()
    async with session.client("s3") as s3_client:
        temp = tempfile.TemporaryFile()
        try:
            await s3_client.download_fileobj(
                "skims.data",
                f"results/{execution_id}.sarif",
                temp,
            )
            temp.seek(0)
            return json.loads(temp.read().decode())
        finally:
            temp.close()
