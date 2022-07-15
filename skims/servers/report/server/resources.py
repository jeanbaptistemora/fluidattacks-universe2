import aioboto3
import csv
import tempfile
from typing import (
    Any,
    Dict,
    List,
)
import yaml


async def get_config(execution_id: str) -> Dict[str, Any]:
    session = aioboto3.Session()
    async with session.client("s3") as s3_client:
        temp = tempfile.TemporaryFile()
        try:
            await s3_client.download_fileobj(
                "skims.data",
                f"configs/{execution_id}.yaml",
                temp,
            )
            temp.seek(0)
            return yaml.safe_load(temp)
        finally:
            temp.close()


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
            return list(
                csv.DictReader(
                    temp.read().decode(),
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
                )
            )
        finally:
            temp.close()
