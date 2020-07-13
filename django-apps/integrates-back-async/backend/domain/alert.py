from typing import Dict, List
from backend.dal import alert as alert_dal


def get_company_alert(company: str, project_name: str) -> List[Dict[str, str]]:
    return alert_dal.get(company, project_name)
