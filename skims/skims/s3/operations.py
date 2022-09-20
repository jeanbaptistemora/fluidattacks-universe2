# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    UnavailabilityError,
)
from db_model.advisories.constants import (
    SUPPORTED_PLATFORMS,
)
from db_model.advisories.types import (
    Advisory,
)
import json
from s3.resource import (
    get_s3_resource,
    s3_shutdown,
)
from tempfile import (
    NamedTemporaryFile,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)
from utils.logs import (
    log_blocking,
)


async def upload_object(
    client: Any, file_name: str, dict_object: Dict[str, Any], bucket: str
) -> None:
    try:
        await client.put_object(
            Body=json.dumps(dict_object, indent=2, sort_keys=True),
            Bucket=bucket,
            Key=file_name,
        )
        print(f"Added file: {file_name}")
    except ClientError as ex:
        raise UnavailabilityError() from ex


async def download_json_fileobj(
    client: Any,
    bucket: str,
    file_name: str,
) -> Dict[str, Any]:
    return_value: Dict[str, Any] = {}
    with NamedTemporaryFile() as temp:
        try:
            await client.download_fileobj(
                bucket,
                file_name,
                temp,
            )
            temp.seek(0)
            return_value = json.loads(temp.read().decode(encoding="utf-8"))
        except ValueError as ex:
            log_blocking("error", "%s", ex)
        return return_value


async def download_advisories() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    try:
        client = await get_s3_resource()
        s3_advisories = {}
        s3_patch_advisories = {}
        bucket_name = "skims.sca"
        for plt in SUPPORTED_PLATFORMS:
            dict_obj: Dict[str, Any] = await download_json_fileobj(
                client, bucket_name, f"{plt}.json"
            )
            s3_advisories.update({plt: dict_obj})
            dict_patch_obj: Dict[str, Any] = await download_json_fileobj(
                client, bucket_name, f"{plt}_patch.json"
            )
            s3_patch_advisories.update({plt: dict_patch_obj})
    finally:
        await s3_shutdown()
    return s3_advisories, s3_patch_advisories


async def upload_advisories(
    to_storage: List[Advisory],
    s3_advisories: Optional[Dict[str, Any]] = None,
    is_patch: bool = False,
) -> None:
    s3_advisories = {} if s3_advisories is None else s3_advisories
    for adv in to_storage:
        if adv.package_manager not in s3_advisories:
            s3_advisories.update({adv.package_manager: {}})
        if adv.package_name not in s3_advisories[adv.package_manager]:
            s3_advisories[adv.package_manager].update({adv.package_name: {}})
        s3_advisories[adv.package_manager][adv.package_name].update(
            {adv.associated_advisory: adv.vulnerable_version}
        )
    try:
        client = await get_s3_resource()
        for key, value in s3_advisories.items():
            await upload_object(
                client=client,
                bucket="skims.sca",
                dict_object=value,
                file_name=f"{key}{'_patch' if is_patch else ''}.json",
            )
    except UnavailabilityError as ex:
        log_blocking("error", "%s", ex.new())
    finally:
        await s3_shutdown()
