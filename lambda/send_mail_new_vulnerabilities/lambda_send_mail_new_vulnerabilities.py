"""Send new vulnerabilities mail lambda function."""

import json
import os

import mandrill


def send_mail_new_vulnerabilities(event, context):
    """Lambda code."""
    template_name = 'newvulnerabilitiesintegrates'
    message = json.loads(event['message'])
    mandrill_client = mandrill.Mandrill(os.environ['FI_MANDRILL_API_KEY'])
    mandrill_client.messages.send_template(template_name, [], message)
    return {
        'statusCode': 200,
        'body': json.dumps('Done.')
    }
