
# pylint: disable=import-error

import os
import sys
import boto3
from asgiref.sync import sync_to_async
from backend.decorators import require_login
from backend.domain import (
    finding as finding_domain, project as project_domain,
    vulnerability as vuln_domain
)
from backend.exceptions import ErrorUploadingFileS3
from backend.utils import reports
from backend.dal.helpers import cloudfront
from backend.utils.passphrase import get_passphrase
from backend import util
from app.documentator.pdf import CreatorPDF
from app.documentator.secure_pdf import SecurePDF
from app.techdoc.it_report import ITReport
from __init__ import (
    FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY, FI_AWS_S3_BUCKET,
    FI_CLOUDFRONT_REPORTS_DOMAIN
)
from ariadne import convert_kwargs_to_snake_case

CLIENT_S3 = boto3.client('s3',
                         aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
                         aws_secret_access_key=FI_AWS_S3_SECRET_KEY,
                         aws_session_token=os.environ.get('AWS_SESSION_TOKEN'))

BUCKET_S3 = FI_AWS_S3_BUCKET


@convert_kwargs_to_snake_case
def resolve_report_mutation(obj, info, **parameters):
    """Resolve reports mutation."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return util.run_async(resolver_func, obj, info, **parameters)


@require_login
# pylint: disable=too-many-locals
async def _do_request_report(_, info, **parameters):
    success = False
    project_name = parameters.get('project_name')
    report_type = parameters.get('report_type')
    user_info = util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    user_name = user_email.split('@')[0]
    findings = \
        await sync_to_async(
            project_domain.list_findings)(project_name.lower())
    findings = await sync_to_async(finding_domain.get_findings)(findings)
    findings = [
        await sync_to_async(finding_domain.cast_new_vulnerabilities)
        (await sync_to_async(vuln_domain.get_open_vuln_by_type)
         (finding['findingId'], info.context), finding)
        for finding in findings]
    description = \
        await sync_to_async(
            project_domain.get_description)(project_name.lower())

    findings_ord = util.ord_asc_by_criticidad(findings)
    if report_type == 'PDF':
        pdf_maker = CreatorPDF(parameters.get('lang', ''), 'tech')
        secure_pdf = SecurePDF()
        findings = pdf_evidences(findings_ord)
        report_filename = ''
        pdf_maker.tech(findings, project_name, description)
        report_filename = secure_pdf.create_full(user_name,
                                                 pdf_maker.out_name,
                                                 project_name)
        success, uploaded_file_name = reports.upload_report(report_filename)
        if not success:
            raise ErrorUploadingFileS3()
        signed_url = cloudfront.sign_url(
            FI_CLOUDFRONT_REPORTS_DOMAIN, uploaded_file_name, 120.0)
        reports.send_report_password_email(user_email,
                                           project_name.lower(),
                                           secure_pdf.password, 'PDF',
                                           signed_url)
    elif report_type == 'XLS':
        it_report = ITReport(project_name, findings_ord, user_name)
        filepath = it_report.result_filename
        password = get_passphrase(4)
        reports.set_xlsx_password(filepath, str(password))
        reports.send_report_password_email(user_email,
                                           project_name.lower(),
                                           password, 'XLS', '')

    return dict(success=success)


def pdf_evidences(findings):
    for finding in findings:
        folder_name = finding['projectName'] + '/' + finding['findingId']
        evidence = finding['evidence']
        evidence_set = [{
            'id': '{}/{}'.format(folder_name, evidence[ev_item]['url']),
            'explanation': evidence[ev_item]['description'].capitalize()
        } for ev_item in evidence if evidence[ev_item]['url'].endswith('.png')]

        if evidence_set:
            finding['evidence_set'] = evidence_set
            for evidence in evidence_set:
                CLIENT_S3.download_file(
                    BUCKET_S3,
                    evidence['id'],
                    '/usr/src/app/app/documentator/images/' +
                    evidence['id'].split('/')[2])
                evidence['name'] = 'image::../images/' + \
                    evidence['id'].split('/')[2] + '[align="center"]'

    return findings
