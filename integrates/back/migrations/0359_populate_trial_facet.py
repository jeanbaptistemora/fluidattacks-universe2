# pylint: disable=import-error,invalid-name
# type: ignore
"""
Populates the trial facet with data previosly stored in the company facet

Execution Time:    2023-02-07 at 17:20:14 UTC
Finalization Time: 2023-02-07 at 17:20:36 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model import (
    trials as trials_model,
)
from db_model.companies.types import (
    Company,
)
from db_model.trials.types import (
    Trial,
)
from organizations import (
    domain as orgs_domain,
)
import time


async def process_trial(created_by: str, company: Company) -> None:
    await trials_model.add(
        trial=Trial(
            completed=company.trial.completed,
            email=created_by,
            extension_date=company.trial.extension_date,
            extension_days=company.trial.extension_days,
            start_date=company.trial.start_date,
        )
    )


async def main() -> None:
    loaders = get_new_context()
    groups = await orgs_domain.get_all_trial_groups(loaders)
    domains = [group.created_by.split("@")[1] for group in groups]
    companies = await loaders.company.load_many(domains)

    await collect(
        [
            process_trial(group.created_by, company)
            for group, company in zip(groups, companies)
            if company and company.trial.start_date
        ]
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
