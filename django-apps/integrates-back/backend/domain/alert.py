from backend.dal import alert as alert_dal


def get_company_alert(company, project_name):
    return alert_dal.get(company, project_name)


def set_company_alert(company, message, project_name):
    if message in ('ACTIVATE', 'DEACTIVATE'):
        resp = alert_dal.change_status(message, company, project_name)
    else:
        resp = alert_dal.put(message, company, project_name)
    return resp
