#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This migration creates an organization attribute in every fi_projects item
The organization field will have the id of the same
If the organization exists, it will be assigned to the group
It it does not exists, it will be created

Migration must be executed when the code that creates the organization in the 
group creation is in production, so all possible groups have an organization
"""

import os
import uuid
import rollbar
import django

django.setup()

from backend.dal import (
    organization as org_dal,
    project as project_dal
)

STAGE: str = os.environ['STAGE']

def log(message):
    print(message)
    rollbar.report_message(message, level='debug')


def main():
    """
    Assign organization to every group
    """
    log('Starting migration 0009')
    all_projects = project_dal.get_all(
        filtering_exp= 'attribute_exists(companies) and \
            attribute_not_exists(organization)',
        data_attr='project_name,companies')

    if STAGE == 'test':
        log('Organizations will be added as follows:')
        unique_orgs = {}

    for proj in all_projects:
        proj_name = proj.get('project_name')
        org_name = proj.get('companies')[0].lower()
        if STAGE == 'test':
            log('---\nGroup: {}'.format(proj.get('project_name')))
            if org_name not in unique_orgs:
                unique_orgs[org_name] = uuid.uuid4()
            log('pk: ORG#{}\n'
                'sk: {}'.format(unique_orgs[org_name], org_name))
        else:
            org_dict = org_dal.get_or_create(org_name)
            success : bool = project_dal.update(
                data={'organization': org_dict['id']},
                project_name=proj_name)
            if success:
                log('Migration 0009: Group {} '
                    'succesfully migrated'.format(proj_name))


if __name__ == '__main__':
    main()
