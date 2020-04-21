
# pylint: disable=import-error

import sys
import threading
from asgiref.sync import sync_to_async
from backend.decorators import require_login
from backend.domain import (
    finding as finding_domain, project as project_domain,
    report as report_domain, vulnerability as vuln_domain
)
from backend.typing import SimplePayload as SimplePayloadType
from backend import util

from ariadne import convert_kwargs_to_snake_case


@convert_kwargs_to_snake_case
def resolve_report_mutation(obj, info, **parameters):
    """Resolve reports mutation."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return util.run_async(resolver_func, obj, info, **parameters)


@require_login
async def _do_request_project_report(_, info,
                                     **parameters) -> SimplePayloadType:
    success = False
    project_name = parameters.get('project_name', '')
    report_type = parameters.get('report_type')
    user_info = util.get_jwt_content(info.context)
    user_email = user_info['user_email']
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
        generate_pdf_report_thread = threading.Thread(
            name='PDF report generation thread',
            target=report_domain.generate_pdf_report,
            args=(project_name,
                  user_email,
                  parameters.get('lang', 'en'),
                  findings_ord,
                  description)
        )
        generate_pdf_report_thread.start()
        success = True
    elif report_type == 'XLS':
        generate_xls_report_thread = threading.Thread(
            name='XLS report generation thread',
            target=report_domain.generate_xls_report,
            args=(project_name,
                  user_email,
                  findings_ord)
        )
        generate_xls_report_thread.start()
        success = True

    return SimplePayloadType(success=success)
