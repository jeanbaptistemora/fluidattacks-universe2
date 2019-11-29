"""Send new vulnerabilities mail lambda function."""

import json

import mandrill


# pylint: disable=unused-argument
def send_mail_new_vulnerabilities(event, context):
    """Lambda code."""
    template_name = 'newvulnerabilitiesintegrates'

    record = event['Records'][0]
    body = json.loads(record['body'])

    message = body['message']
    api_key = body['api_key']
    mandrill_client = mandrill.Mandrill(api_key)
    mandrill_client.messages.send_template(template_name, [], message)
    return {
        'statusCode': 200,
        'body': json.dumps('Done.')
    }
