import asyncio
from os import (
    environ,
)
import skims_sdk
import subprocess


async def main() -> None:
    group: str = "continuoustest"
    code, out_, _ = await skims_sdk.queue(
        finding_code=skims_sdk.get_finding_code_from_title(
            "117. Unverifiable files"
        ),
        group=group,
        namespace="test",
        urgent=False,
        product_api_token=environ["PRODUCT_API_TOKEN"],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    out = out_.decode()

    assert code == 0, out
    assert "Running on AWS" in out, out
    assert "Job Queue: skims_f117_later" in out, out
    assert (
        f"process-{group}-F117-test has been successfully sent" in out
        or f"process-{group}-F117-test is already in queue" in out
    ), out


if __name__ == "__main__":
    asyncio.run(main())
