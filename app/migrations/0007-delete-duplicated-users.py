"""
This migration erases duplicate users from both DynamoDB and MySQL,
created by the Azure auth backend when it could not resolve the user correctly.

Execution Time: 2020-06-02 19:07 UTC-5
Finalization Time: 2020-06-02 19:12 UTC-5
"""
import os
from typing import (
    cast,
    Dict,
    List,
)

import bugsnag
import django
from backend.dal.user import (
    delete as delete_dynamo_user,
    get_all as get_all_dynamo_users
)
from boto3.dynamodb.conditions import Attr

# Allows to import Django Apps
django.setup()


from django.contrib.auth.models import User


PROVIDER = 'azuread-tenant-oauth2'
STAGE: str = os.environ['STAGE']


def delete_duplicated_users_dynamo() -> None:
    for user in get_all_dynamo_users(Attr('email').exists(), 'email'):
        # Duplicated usernames have the syntax user@domain.comrandom_string
        if len(user['email'].split('.')[-1]) > 10:
            if STAGE == 'test':
                print('User {} will be deleted from DynamoDB...'.format(user['email']))
            else:
                delete_dynamo_user(user['email'])
                log('Migration 0007: User {} was deleted from DynamoDB'.format(user['email']))


def delete_duplicated_users_mysql() -> None:
    users_created_with_errors = []

    for user in User.objects.filter(social_auth__provider=PROVIDER):
        try:
            if '@' not in user.social_auth.get(provider=PROVIDER).uid:
                if len(user.username.split('.')[-1]) > 10:
                    if STAGE == 'test':
                        print('User {} will be deleted from MySQL'.format(user.username))
                    else:
                        user.delete()
                        log('Migration 0007: User {} was deleted from MySQL'.format(user.username))
                elif user.email not in users_created_with_errors:
                    users_created_with_errors.append(user.email)
        except:
            log('Migration 0007: Special case found with user {}'.format(user.email))


    if users_created_with_errors:
        fix_users_created_with_errors(users_created_with_errors)


def fix_users_created_with_errors(email_list: List[str]) -> None:
    for email in email_list:
        users = User.objects.filter(email=email).order_by('id')
        if len(users) == 2:
            if STAGE == 'test':
                print('User {} will be deleted from MySQL'.format(users[1].username))
                print('User {} uid will be updated from {} to {}'.format(
                    users[0].username,
                    users[0].social_auth.get(provider=PROVIDER).uid,
                    email
                    )
                )
            else:
                users[1].delete()
                users[0].social_auth.update(uid=email)
                log('Migration 0007: User {} was deleted from MySQL'.format(users[1].username))
                log('Migration 0007: User {} uid was be updated from {} to {}'.format(
                    users[0].username,
                    users[0].social_auth.get(provider=PROVIDER).uid,
                    email
                    )
                )
        else:
            print('Migration 0007: Special case for user with email {}'.format(email))



def log(message: str) -> None:
    if STAGE != 'test':
        bugsnag.notify(Exception(message), severity='info')


def main() -> None:
    delete_duplicated_users_dynamo()
    delete_duplicated_users_mysql()
    log('Migration 0007: finished migration successfully')


if __name__ == '__main__':
    main()
