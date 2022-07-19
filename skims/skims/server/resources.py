import aioboto3
from config import (
    load,
)
import csv
from model.core_model import (
    SkimsConfig,
)
import tempfile
from typing import (
    Any,
    Dict,
    List,
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
            return load(group, temp.name)


async def get_results(execution_id: str) -> List[Dict[str, Any]]:
    session = aioboto3.Session()
    async with session.client("s3") as s3_client:
        temp = tempfile.TemporaryFile()
        try:
            await s3_client.download_fileobj(
                "skims.data",
                f"results/{execution_id}.csv",
                temp,
            )
            temp.seek(0)
            lines = temp.read().decode().splitlines()
            if len(lines) < 2:
                return []

            return list(
                csv.DictReader(
                    lines[1:],
                    [
                        "finding",
                        "kind",
                        "what",
                        "where",
                        "cwe",
                        "stream",
                        "title",
                        "description",
                        "snippet",
                        "method",
                    ],
                ),
            )
        finally:
            temp.close()
