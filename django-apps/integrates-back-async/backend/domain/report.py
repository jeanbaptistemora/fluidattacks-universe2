
from typing import cast, Dict, List
from backend.typing import Finding as FindingType
from backend.utils import reports
from backend.dal import finding as finding_dal, report as report_dal
from backend.utils.passphrase import get_passphrase
from app.documentator.pdf import CreatorPDF
from app.documentator.secure_pdf import SecurePDF
from app.techdoc.it_report import ITReport


def generate_pdf_report(project_name: str, user_email: str, lang: str,
                        findings_ord: List[Dict[str, FindingType]], description: str):
    user_name = user_email.split('@')[0]
    pdf_maker = CreatorPDF(lang, 'tech')
    secure_pdf = SecurePDF()
    findings = pdf_evidences(findings_ord)
    report_filename = ''
    pdf_maker.tech(findings, project_name, description)
    report_filename = secure_pdf.create_full(user_name,
                                             pdf_maker.out_name,
                                             project_name)
    uploaded_file_name = report_dal.upload_report(report_filename)
    signed_url = report_dal.sign_url(uploaded_file_name)
    reports.send_project_report_email(user_email,
                                      project_name.lower(),
                                      secure_pdf.passphrase, 'PDF',
                                      signed_url)


def generate_xls_report(project_name: str, user_email: str,
                        findings_ord: List[Dict[str, FindingType]]):
    it_report = ITReport(data=findings_ord)
    filepath = it_report.result_filename
    passphrase = get_passphrase(4)
    reports.set_xlsx_passphrase(filepath, str(passphrase))
    uploaded_file_name = report_dal.upload_report(filepath)
    signed_url = report_dal.sign_url(uploaded_file_name)
    reports.send_project_report_email(user_email,
                                      project_name.lower(),
                                      passphrase, 'XLS', signed_url)


def pdf_evidences(findings: List[Dict[str, FindingType]]) -> List[Dict[str, FindingType]]:
    for finding in findings:
        folder_name = str(finding['projectName']) + '/' + str(finding['findingId'])
        evidences = cast(Dict[str, Dict[str, str]], finding['evidence'])
        evidence_set: List[Dict[str, str]] = [{
            'id': '{}/{}'.format(folder_name, str(evidences[ev_item]['url'])),
            'explanation': evidences[ev_item]['description'].capitalize()
        } for ev_item in evidences if evidences[ev_item]['url'].endswith('.png')]

        if evidence_set:
            finding['evidence_set'] = evidence_set
            for evidence in evidence_set:
                finding_dal.download_evidence(
                    evidence['id'],
                    '/usr/src/app/app/documentator/images/' +
                    str(evidence['id']).split('/')[2])
                evidence['name'] = 'image::../images/' + \
                    str(evidence['id']).split('/')[2] + '[align="center"]'

    return findings
