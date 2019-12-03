"""Send new vulnerabilities mail lambda function."""
import json
import mandrill


# pylint: disable=unused-argument
def send_mail_new_vulnerabilities(event, context):
    """Lambda code."""
    try:
        record = event['Records'][0]
        template_name = record['attributes']['MessageGroupId']
        body = json.loads(record['body'])

        message = body['message']
        api_key = body['api_key']
    except KeyError:
        return {
            'statusCode': 200,
            'body': json.dumps('An invalid message was given.')
        }
    try:
        mandrill_client = mandrill.Mandrill(api_key)
        mandrill_client.messages.send_template(template_name, [], message)
    except mandrill.InvalidKeyError:
        return {
            'statusCode': 200,
            'body': json.dumps('An invalid key was given.')
        }
    return {
        'statusCode': 200,
        'body': json.dumps('Done.')
    }
