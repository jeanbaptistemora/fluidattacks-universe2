---
id: arm-etl
title: Arm ETL
sidebar_label: Arm
slug: /development/arm-etl
---

This ETL process extracts data from the arm database (dynamo) and sends it to
the warehouse (redshift).

:::note
Local execution and sending of jobs will require access to the
'prod_observes' role
:::

## Architecture

The ETL has three core procedures:

- Segment ETL

    where the ETL is executed over a segment of the dynamo data.

- Data centralization

    where segmented data uploaded to redshift is centralized
    into one redshift-schema.

- Data-schema determination

    where the schema of the data is inferred.

:::caution
Do not confuse: _redshift-schema_ is an entity that groups a collection of
tables (like a folder), instead, data-schema is the metadata of some data
(e.g. their column names and types)
:::

## Segment ETL

The segment ETL consist of four phases that execute concurrently.
This process is triggered by an schedule.

1. Segment extraction

    The data is extracted using a
    [parallel scan](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.ParallelScan)
    over one specific segment.
1. Data transform

    By using the auto generated data-schemas, the data is adjusted.

1. S3 upload

    Data is transformed into a csv file (one for each data-schema)
    and uploaded into the _observes.etl-data_ bucket.

1. Redshift load

    Data at S3 is transferred into redshift using custom
    redshift queries.

:::info
Data is uploaded first to s3 and then to redshift due to performance issues.
The custom redshift load query from s3 is more efficient than direct upload
queries.
:::

## Data centralization

This ETL uses various batch jobs to perform the _segment ETL_ over various
segments of data. As a consequence various redshift-schemas are generated
(one for each segment). Since the data is expected to be in one redshift-schema,
the centralization procedure glues the data together.

When data segments finish successfully the centralization process can be
triggered. This phase is manually triggered.

1. _Temporal centralized redshift-schema_ should be regenerated

    ```bash
    m . /observes/etl/dynamo/prepare "dynamodb_integrates_vms_merged_parts_loading" "s3://observes.cache/dynamoEtl/vms_schema"
    ```

1. Centralization procedure merges data into the _temporal centralized redshift-schema_

    ```bash
    m . /observes/etl/dynamo/centralize
    ```

1. _Temporal centralized redshift-schema_ must be renamed with an SQL query

    ```sql
    ALTER SCHEMA "dynamodb_integrates_vms_merged_parts_loading" RENAME TO "dynamodb_integrates_vms"
    ```

1. Re-execute centralization

    to merge the renamed redshift-schema into the production schema

    ```bash
    m . /observes/etl/dynamo/centralize
    ```

## Data-schema determination

This process infer data-schema from raw data and stores the determined
data-schemas into _observes.cache_ s3 bucket for serving as a cache.

This process is triggered by an schedule. It has a frequency of execution
of one week.

```bash
m . /computeOnAwsBatch/observesDynamoSchema
```

## Common issues

- Host terminated

    This error is due to the spot nature of the instances used
    at batch. Depending on where the ETL has stopped it may require re-execution
    of the segment ETL i.e. if the job completed to upload data to s3, the job can
    be modified and executed locally to perform only the _redshift load_ phase of
    the ETL.

- InternalError stl_load_errors

    i.e. `psycopg2.errors.InternalError_: Load into table 'integrates_vms' failed.
    Check 'stl_load_errors' system table for detail`
    This error is due to [#8258](https://gitlab.com/fluidattacks/universe/-/issues/8258)
    Re-execution will probably fail again. To solve this modify the s3 data file
    (in this case the 'integrates_vms' file) by trimming some multi line fields.
    There is no a defined trim length for the solution, the idea is that the file
    gets segmented by redshift in the right spot.

- CannotInspectContainerError

    This error express that the job finish in an
    unknown state (can be success or fail), nevertheless the job state is set to
    failed. This requires manual inspection of the job log to confirm failure.

- Stuck queries:

    If some query seems stuck see [this resolution](https://aws.amazon.com/es/premiumsupport/knowledge-center/prevent-locks-blocking-queries-redshift/#Resolution).
