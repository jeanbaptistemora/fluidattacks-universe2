from app.dal import integrates_dal


def get_company_alert(company, project_name):
    return integrates_dal.get_company_alert_dynamo(company, project_name)


def set_company_alert(company, message, project_name):
    if message in ('ACTIVATE', 'DEACTIVATE'):
        resp = integrates_dal.change_status_comalert_dynamo(
            message, company, project_name)
    else:
        resp = integrates_dal.set_company_alert_dynamo(
            message, company, project_name)
    return resp
