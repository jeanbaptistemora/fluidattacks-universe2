# pylint: disable=E0402
from ..dao import integrates_dao
from ..mailer import send_mail_new_user

FLUID_DOMAIN = '@fluid.la'

# pylint: disable=W0613
def create_user(strategy, details, backend, user=None, *args, **kwargs):
    username = details['username']
    first_name = details['first_name']
    last_name = details['last_name']
    email = details['email']

    # Put details on session
    strategy.session_set('first_name', first_name)
    strategy.session_set('last_name', last_name)

    if user:
        integrates_dao.update_user_login_dao(user)
    else:
        to = ["aroldan@fluid.la", "glopez@fluid.la", "projects@fluid.la",
              "production@fluid.la", "technology@fluid.la"]
        name = first_name + ' ' + last_name
        context = {
            'name_user': name,
            'mail_user': email,
            }
        send_mail_new_user(to, context)
        integrates_dao.create_user_dao(email, username=username,
                                       first_name=first_name,
                                       last_name=last_name)

    if email.endswith(FLUID_DOMAIN):
        integrates_dao.register(email)
        integrates_dao.assign_role(email, 'analyst')
        integrates_dao.assign_company(email, 'FLUID')

def check_registered(strategy, details, backend, *args, **kwargs):
    email = details['email']
    is_registered = integrates_dao.is_registered_dao(email)
    last_login = integrates_dao.get_user_last_login_dao(email)
    print (last_login)
    role = integrates_dao.get_role_dao(email)
    company = integrates_dao.get_company_dao(email)

    strategy.session_set('username', email)
    strategy.session_set('registered', is_registered)
    strategy.session_set('role', role)
    strategy.session_set('company', company)
    strategy.session_set('last_login', last_login)
