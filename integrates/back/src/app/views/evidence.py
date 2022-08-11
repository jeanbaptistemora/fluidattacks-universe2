# Starlette evidences-related methods


import aiohttp
import authz
from context import (
    FI_AWS_S3_BUCKET,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from decorators import (
    retry_on_exceptions,
)
from events.domain import (
    has_access_to_event,
)
from findings.domain import (
    has_access_to_finding,
)
from magic import (
    Magic,
)
from newutils import (
    files as files_utils,
    logs as logs_utils,
    utils,
)
from s3.operations import (
    download_file,
    list_files,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    HTMLResponse,
    JSONResponse,
    Response,
)
from typing import (
    List,
    Sequence,
)

BUCKET_S3 = FI_AWS_S3_BUCKET
download_evidence_file = retry_on_exceptions(
    exceptions=(
        aiohttp.ClientError,
        aiohttp.ClientPayloadError,
    ),
    max_attempts=3,
    sleep_seconds=float("0.2"),
)(download_file)


async def enforce_group_level_role(
    loaders: Dataloaders,
    request: Request,
    group: str,
    *allowed_roles: Sequence[str],
) -> Response:
    response = None
    email = request.session.get("username")
    if not email:
        return HTMLResponse(
            "<script> "
            "var getUrl=window.location.href.split("
            "`${window.location.host}/`); "
            'localStorage.setItem("start_url",getUrl[getUrl.length - 1]); '
            'location = "/"; '
            "</script>"
        )
    requester_role = await authz.get_group_level_role(loaders, email, group)
    if requester_role not in allowed_roles:
        response = Response("Access denied")
        response.status_code = 403
    return response


async def get_evidence(request: Request) -> Response:
    loaders: Dataloaders = get_new_context()
    group_name = request.path_params["group_name"]
    finding_id = request.path_params["finding_id"]
    file_id = request.path_params["file_id"]
    evidence_type = request.path_params["evidence_type"]

    allowed_roles = [
        "admin",
        "architect",
        "customer_manager",
        "hacker",
        "reattacker",
        "resourcer",
        "reviewer",
        "user",
        "user_manager",
        "vulnerability_manager",
    ]
    error = await enforce_group_level_role(
        loaders, request, group_name, *allowed_roles
    )
    if error is not None:
        return error

    username = request.session["username"]
    if (
        evidence_type in ["drafts", "findings", "vulns"]
        and await has_access_to_finding(loaders, username, finding_id)
    ) or (
        evidence_type == "events"
        and await has_access_to_event(loaders, username, finding_id)
    ):
        if file_id is None:
            return Response("Error - Unsent image ID", media_type="text/html")
        evidences = await list_s3_evidences(
            f"{group_name.lower()}/{finding_id}/{file_id}"
        )
        if evidences:
            for evidence in evidences:
                start = evidence.find(finding_id) + len(finding_id)
                localfile = f"/tmp{evidence[start:]}"  # nosec
                localtmp = utils.replace_all(
                    localfile, {".png": ".tmp", ".gif": ".tmp"}
                )
                await download_evidence_file(BUCKET_S3, evidence, localtmp)
                return retrieve_image(localtmp)
        else:
            return JSONResponse(
                {
                    "data": [],
                    "message": "Access denied or evidence not found",
                    "error": True,
                }
            )
    else:
        logs_utils.cloudwatch_log(
            request,
            "Security: Attempted to retrieve evidence without permission",
        )
        return JSONResponse(
            {"data": [], "message": "Evidence type not found", "error": True}
        )


async def list_s3_evidences(prefix: str) -> List[str]:
    return list(await list_files(BUCKET_S3, prefix))


def retrieve_image(img_file: str) -> Response:
    if files_utils.assert_file_mime(
        img_file, ["image/png", "image/jpeg", "image/gif"]
    ):
        with open(img_file, "rb") as file_obj:
            mime = Magic(mime=True)
            mime_type = mime.from_file(img_file)
            return Response(file_obj.read(), media_type=mime_type)
    else:
        return Response(
            "Error: Invalid evidence image format", media_type="text/html"
        )
