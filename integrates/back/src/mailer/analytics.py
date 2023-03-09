from context import (
    BASE_URL,
)
from dataloaders import (
    Dataloaders,
)


def send_mail_analytics(
    _loaders: Dataloaders, *_email_to: str, **context: str
) -> None:
    _mail_content = context
    _mail_content["live_report_url"] = (
        f'{BASE_URL}/{_mail_content["report_entity_percent"]}s/'
        f'{_mail_content["report_subject_percent"]}/analytics'
    )
