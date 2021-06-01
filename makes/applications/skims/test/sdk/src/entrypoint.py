import asyncio
from os import (
    environ,
)
import skims_sdk
import subprocess


async def main() -> None:
    group: str = "continuoustest"
    code, out_, _ = await skims_sdk.queue(
        finding_code=None,
        finding_title="F117. Archivos no auditables 123",
        group=group,
        urgent=True,
        product_api_token=environ["PRODUCT_API_TOKEN"],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    out = out_.decode()

    assert code == 0
    assert "Running on AWS" in out
    assert "Job Queue: skims_soon" in out
    assert (
        f"skims-process-group-{group}-F117 has been successfully sent" in out
        or f"skims-process-group-{group}-F117 is already in queue" in out
    )


if __name__ == "__main__":
    asyncio.run(main())
