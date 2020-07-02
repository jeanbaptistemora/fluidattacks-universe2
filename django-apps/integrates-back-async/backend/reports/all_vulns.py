from backend.utils import reports as reports_utils
from app.documentator.all_vulns import generate_all_vulns_xlsx


def generate(user_email: str, project_name: str = '') -> str:
    report_filepath = generate_all_vulns_xlsx(user_email, project_name)
    uploaded_file_name = reports_utils.upload_report(report_filepath)
    uploaded_file_url = reports_utils.sign_url(
        uploaded_file_name,
        minutes=1.0 / 6
    )

    return uploaded_file_url
