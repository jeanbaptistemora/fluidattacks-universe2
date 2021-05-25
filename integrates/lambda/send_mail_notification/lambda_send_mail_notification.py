"""Send new vulnerabilities mail lambda function."""
import json
from typing import (
    Any,
    Dict,
    Union,
)

import mandrill


# Typing
NotificationResponse = Dict[str, Union[int, str]]


def send_mail_notification(event: Dict, _: Any) -> NotificationResponse:
    """Lambda code."""
    response: NotificationResponse = {
        "statusCode": 200,
        "body": json.dumps("Done."),
    }
    try:
        record = event["Records"][0]
        template_name = record["attributes"]["MessageGroupId"]
        body = json.loads(record["body"])

        message = body["message"]
        api_key = body["api_key"]
    except KeyError:
        response = {
            "statusCode": 200,
            "body": json.dumps("An invalid message was given."),
        }
    try:
        mandrill_client = mandrill.Mandrill(api_key)
        mandrill_client.messages.send_template(template_name, [], message)
    except mandrill.InvalidKeyError:
        response = {
            "statusCode": 200,
            "body": json.dumps("An invalid key was given."),
        }
    return response
