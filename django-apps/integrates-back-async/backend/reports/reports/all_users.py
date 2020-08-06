from typing import cast, Dict
import uuid
from pyexcelerate import Workbook
from backend.dal import user as user_dal
from backend.domain import user as user_domain
from backend.reports.typing import AllUsersReportHeader
from backend.utils import reports as reports_utils


async def generate(user_email: str) -> str:
    workbook = Workbook()
    sheet_values = [AllUsersReportHeader.labels()]
    row_index = 2

    unique_users = []
    for user in await user_dal.get_platform_users():
        email = str(user.get('user_email', '')).lower()
        if email not in unique_users:
            unique_users.append(email)

            name_attrs = cast(
                Dict[str, str],
                await user_domain.get_attributes(
                    email, ['first_name', 'last_name']
                )
            )
            full_name = ' '.join(list(name_attrs.values()))

            sheet_values.append([full_name, email])
            row_index += 1

    username = user_email.split('@')[0]
    report_filepath = f'/tmp/{username}-{uuid.uuid4()}-allusers.xlsx'
    workbook.new_sheet('Users', data=sheet_values)
    workbook.save(report_filepath)

    uploaded_file_name = await reports_utils.upload_report(report_filepath)
    uploaded_file_url = await reports_utils.sign_url(
        uploaded_file_name,
        minutes=1.0 / 6
    )

    return uploaded_file_url
