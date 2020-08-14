#/usr/bin/env python3
#-.- coding: utf-8 -.-
"""
This migration aims to clean the organization table by deleting
all organizations that do not have a group attached

Execution Time: 2020-07-16 20:38:00 UTC-5
Finalization Time: 2020-07-16 20:51:0 UTC-5
"""
import asyncio
import os

from backend.domain import organization as org_domain


STAGE: str = os.environ['STAGE']


async def main() -> None:
    async for org_id, org_name, groups in \
            org_domain.iterate_organizations_and_groups():
        if not groups:
            if STAGE == 'test':
                print(f'Organization {org_name} will be deleted')
            else:
                await org_domain.delete_organization(org_id)


if __name__ == '__main__':
    asyncio.run(main())
