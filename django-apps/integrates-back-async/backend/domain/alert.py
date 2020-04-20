from typing import Dict, List
from backend.dal import alert as alert_dal


def get_company_alert(company: str, project_name: str) -> List[Dict[str, str]]:
    return alert_dal.get(company, project_name)


def set_company_alert(company: str, message: str, project_name: str) -> bool:
    if message in ('ACTIVATE', 'DEACTIVATE'):
        resp = alert_dal.change_status(message, company, project_name)
    else:
        resp = alert_dal.put(message, company, project_name)
    return resp
