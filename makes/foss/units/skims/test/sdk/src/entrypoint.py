import asyncio
from os import (
    environ,
)
import skims_sdk
import subprocess


async def main() -> None:
    group: str = "continuoustest"
    code, out_, err_ = await skims_sdk.queue(
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
    err = err_.decode()

    assert code == 0, (out, err)
    assert "Making secrets for AWS" in err, [out, err]
    assert "Checking if job" in err, [out, err]
    assert (
        f"{group}-F117-test has been successfully sent" in err
        or f"{group}-F117-test is already in queue" in err
    ), [out, err]


if __name__ == "__main__":
    asyncio.run(main())
