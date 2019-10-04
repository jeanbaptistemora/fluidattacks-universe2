# pylint: disable=E0402
from __future__ import absolute_import
from __init__ import FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS
from ..dal import integrates_dal
from ..domain import user as user_domain
from ..mailer import send_mail_new_user


# pylint: disable=W0613
def create_user(strategy, details, backend, user=None, *args, **kwargs):
    username = details['username'][:63]
    first_name = details['first_name'][:29]
    last_name = details['last_name'][:29]
    email = details['email']

    # Put details on session.
    strategy.session_set('first_name', first_name)
    strategy.session_set('last_name', last_name)

    if user:
        if integrates_dal.has_complete_data(user):
            integrates_dal.update_user_login(user)
        else:
            integrates_dal.update_user_data(email, username, first_name,
                                            last_name)
            integrates_dal.update_user_login(user)
    else:
        mail_to = [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
        name = first_name + ' ' + last_name
        context = {
            'name_user': name,
            'mail_user': email,
        }
        send_mail_new_user(mail_to, context)
        integrates_dal.create_user(email, username=username,
                                   first_name=first_name,
                                   last_name=last_name,
                                   first_time="1")


def check_registered(strategy, details, backend, *args, **kwargs):
    email = details['email']
    is_registered = user_domain.is_registered(email)
    last_login = integrates_dal.get_user_last_login(email)
    role = user_domain.get_role(email)
    company = user_domain.get_organization(email)
    strategy.session_set('username', email)
    strategy.session_set('registered', is_registered)
    if role == 'customeradmin':
        role = 'customer'
    else:
        # different role
        pass
    strategy.session_set('role', role)
    strategy.session_set('company', company)
    strategy.session_set('last_login', last_login)
    strategy.session_set('projects', {})
