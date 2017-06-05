# pylint: disable=E0402
from ..dao import integrates_dao

# pylint: disable=W0613
def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        integrates_dao.update_user_login_dao(user)
        return

    username = details['username']
    first_name = details['first_name']
    last_name = details['last_name']
    email = details['email']

    integrates_dao.create_user_dao(email, username=username,
                                   first_name=first_name,
                                   last_name=last_name)


def check_registered(strategy, details, backend, *args, **kwargs):
    email = details['email']
    is_registered = integrates_dao.is_registered_dao(email)
    role = integrates_dao.get_role_dao(email)
    company = integrates_dao.get_company_dao(email)

    strategy.session_set('username', email)
    strategy.session_set('registered', is_registered)
    strategy.session_set('role', role)
    strategy.session_set('company', company)
