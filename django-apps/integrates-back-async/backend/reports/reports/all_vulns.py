from backend.utils import reports as reports_utils
from backend.reports.all_vulns import generate_all_vulns_xlsx


async def generate(user_email: str, project_name: str = '') -> str:
    report_filepath = await generate_all_vulns_xlsx(user_email, project_name)
    uploaded_file_name = await reports_utils.upload_report(report_filepath)
    uploaded_file_url = await reports_utils.sign_url(
        uploaded_file_name,
        minutes=1.0 / 6
    )

    return uploaded_file_url
