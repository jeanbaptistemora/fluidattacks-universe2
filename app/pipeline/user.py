# pylint: disable=relative-beyond-top-level

from backend.domain import user as user_domain
from backend.mailer import send_mail_new_user

from __init__ import FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS


# pylint: disable=keyword-arg-before-vararg
def create_user(strategy, details, backend, user=None, *args, **kwargs):
    del args
    del kwargs
    del backend
    first_name = details['first_name'][:29]
    last_name = details['last_name'][:29]
    email = details['email'].lower()

    # Put details on session.
    strategy.session_set('first_name', first_name)
    strategy.session_set('last_name', last_name)

    today = user_domain.get_current_date()
    data_dict = {
        'first_name': first_name,
        'last_login': today,
        'last_name': last_name,
        'date_joined': today
    }
    if user:
        if user_domain.get_data(str(user), 'first_name'):
            user_domain.update_last_login(user)
        else:
            user_domain.update_multiple_user_attributes(str(user), data_dict)
    else:
        mail_to = [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
        name = first_name + ' ' + last_name
        context = {
            'name_user': name,
            'mail_user': email,
        }
        send_mail_new_user(mail_to, context)
        user_domain.update_multiple_user_attributes(email, data_dict)


def check_registered(strategy, details, backend, *args, **kwargs):
    del args
    del kwargs
    del backend
    email = details['email'].lower()
    is_registered = user_domain.is_registered(email)
    last_login = user_domain.get_data(email, 'last_login')
    role = user_domain.get_data(email, 'role')
    company = user_domain.get_data(email, 'company')
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
