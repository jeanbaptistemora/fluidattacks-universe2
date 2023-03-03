---
id: migrations
title: Database Migrations
sidebar_label: DB Migrations
slug: /development/products/integrates/backend/migrations
---

:::caution
Make sure you read this entire document before running a migration.
:::

## What are migrations?

As Integrates and the business evolves,
it is natural for the structure of the data to change.
In order to keep backwards compatibility,
it is necessary to run data migrations that
change all existing data so it complies
with the latest data schema.

For example:

1. We have a cars database and are storing two attributes,
   `color` and `brand`.
1. At some point in time we decide to also store
   the `price` attribute.
1. When this happens, we have to go through all the already-created cars
   and add the new `price` attribute accordingly.

## Writing migration scripts

:::note
All migration scripts are kept in the repo for traceability purposes,
but are _not_ required to be maintained
and kept up with the rest of the codebase when breaking changes take place.
:::

You can find
all the already-executed migrations
[here](https://gitlab.com/fluidattacks/universe/-/tree/trunk/integrates/back/migrations).
The latest of them may be helpful
as inspiration when creating your own migration.

### Basic properties

All migration scripts have a comment including:

1. A basic description of what they do
1. An `Execution time` that specifies when it started running.
1. A `Finalization Time` that specifies when it finished running.

### The main function

Your migration script should contain a main function,
which will be called when the migration runs.

```py
from aioextensions import (
    run,
)
import time


async def main() -> None:
   """Your code goes here"""


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
```

You can call dataloaders,
domain functions,
data model functions
and even direct calls to the corresponding datastore module,
depending of the level of abstraction
best suited to achieve the intended change.

## Running migrations

:::note
Data migrations tend to be risky operations,
as they may introduce inconsistencies and errors,
and therefore,
it is advised to request a review in the Merge Request before running it.
:::

### Dry runs

As migrations affect production data,
it is very important that you take
all necessary measures
so they work as expected.

A very useful measure are dry runs.
Dry runs allow you to run migrations on
your [local environment](/development/products/integrates#development-environment).

To execute a dry run:

1. Write your migration.
1. Turn on your development environment.
1. Run `m . /integrates/db/migration dev /absolute/path/to/script.py`

:::tip
It is the `dev` argument what allows Makes know that it should do a dry run.
:::

This approach allows you to locally test your migration
until you feel comfortable enough to run it on production.

### Running locally

If you have the required role to modify the database,
migrations can be executed from your machine by running:
`m . /integrates/db/migration prod /absolute/path/to/script.py`

### Running on AWS Batch

Once you know that your migration
does what it is supposed to do,
it is recommended to execute it
using a
[Batch schedule](https://gitlab.com/fluidattacks/universe/-/blob/trunk/common/compute/schedule/data.nix):

1. Write your migration.
1. Create a batch schedule that executes the migration.
1. Deploy both changes to production
1. Wait until the schedule executes.
1. [access the AWS console](http://localhost:3001/development/stack/aws#access-web-console)
   to review the logs of the migration.

This allows the migration to execute on an external environment
from your own machine that is faster and more reliable.

## Restoring to a previous state

If something goes wrong,
you have the option to restore data from a backup.

1. Follow the instructions at https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/PointInTimeRecovery.Tutorial.html
   to restore a Point In Time into a new table.
1. Restore the data by reading from the recovery table,
   and writing into the main table
1. Remove the recovery table
