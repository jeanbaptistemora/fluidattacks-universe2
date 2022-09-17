# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# type: ignore

# -.- coding: utf-8 -.-
# pylint: disable=invalid-name
"""
This migration aims to clean the organization table by deleting
all organizations that do not have a group attached

Execution Time: 2020-07-16 20:38:00 UTC-5
Finalization Time: 2020-07-16 20:51:0 UTC-5
"""
from aioextensions import (
    run,
)
from organizations import (
    domain as orgs_domain,
)
import os

STAGE: str = os.environ["STAGE"]


async def main() -> None:
    async for org_id, org_name, groups in (
        orgs_domain.iterate_organizations_groups()
    ):
        if not groups:
            if STAGE == "test":
                print(f"Organization {org_name} will be deleted")
            else:
                await orgs_domain.remove_organization_legacy(org_id)


if __name__ == "__main__":
    run(main())
