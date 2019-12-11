"""PDF creator lambda."""
# pylint: disable=import-error
# pylint: disable=unused-argument
# pylint: disable=too-many-locals
import json
import os

import boto3

from documentator.pdf import CreatorPDF
from documentator.secure_pdf import SecurePDF


def lambda_handler(event, context):
    """Lambda handler."""
    ret = project_to_pdf(event)
    return {
        'statusCode': 200,
        'body': json.dumps(ret)
    }


def project_to_pdf(event):
    """Export a project to a PDF."""
    try:
        lang = event['lang']
        project = event['project']
        doctype = event['doctype']
        findings = event['findings']
        description = event['description']
        user = event['user']
        api_key = event['api_key']
    except KeyError:
        return 'An invalid message was given.'

    pdf_maker = CreatorPDF(lang, doctype)
    secure_pdf = SecurePDF()
    report_filename = ''
    if doctype == 'tech':
        pdf_maker.tech(findings, project, description)
        report_filename = secure_pdf.create_full(user,
                                                 pdf_maker.out_name,
                                                 project)
    else:
        return 'Disabled report generation.'
    if not os.path.isfile(report_filename):
        return 'Could not generate PDF report.'
    with open(report_filename, 'rb') as document:
        contents = document.read()

    payload_dict = {
        'message': event,
        'content': contents,
        'api_key': api_key
    }

    lambda_client = boto3.client('lambda')
    ret = lambda_client.invoke(
        FunctionName='integrates-send-mail-new-vulnerabilities',
        InvocationType='Event',
        LogType='Tail',
        Payload=json.dumps(payload_dict),
        Context='LambdaPdfCreator'
    )
    return ret
