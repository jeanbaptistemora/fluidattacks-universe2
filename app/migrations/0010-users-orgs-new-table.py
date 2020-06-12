#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This migration creates an organization attribute in every fi_users item
The organization field will have the id of the same
If the organization exists, it will be assigned to the user
It it does not exists, it will be created

Migration must be executed when the code that creates the organization in the 
user creation is in production, so all possible users have an organization
"""

import os
import uuid
import rollbar
import django

django.setup()

from asgiref.sync import async_to_sync
from backend.dal import (
    organization as org_dal,
    user as user_dal
)

STAGE: str = os.environ['STAGE']

def log(message: str) -> None:
    print(message)
    rollbar.report_message(message, level='debug')


def main() -> None:
    """
    Assign organization to every user
    """
    log('Starting migration 0009')
    all_users = user_dal.get_all(
        filter_exp= 'attribute_exists(company)',
        data_attr='email,company')

    if STAGE == 'test':
        log('Organizations will be added as follows:')
        unique_orgs = {}

    for user in all_users:
        user_email = user.get('email')
        org_name = user.get('company').lower()
        if STAGE == 'test':
            log('---\nUser: {}'.format(user_email))
            if org_name not in unique_orgs:
                unique_orgs[org_name] = uuid.uuid4()
            log('pk: ORG#{}\n'
                'sk: {}'.format(unique_orgs[org_name], org_name))
        else:
            org_dict = async_to_sync(org_dal.get_or_create)(org_name)
            success : bool = user_dal.update(
                data={'organization': org_dict['id']},
                email=user_email)
            if success:
                log('Migration 0010: User {} '
                    'succesfully migrated'.format(user_email))


if __name__ == '__main__':
    main()
