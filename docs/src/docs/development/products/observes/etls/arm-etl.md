---
id: arm-etl
title: ARM ETL
sidebar_label: ARM
slug: /development/arm-etl
---

This ETL process extracts data from the ARM database (dynamo) and sends it to
the warehouse (redshift).

:::note
Local execution and sending of jobs will require to
[setup your terminal](/development/setup/terminal) and have access to the
`prod_observes` role and the `CACHIX_AUTH_TOKEN` environment variable.
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

    Data in S3 is transferred into redshift using custom
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
triggered. This phase is **manually** triggered.

1. local execution

    ```bash
    m . /observes/etl/dynamo/centralize
    ```

1. aws batch execution

    ```bash
    m . /computeOnAwsBatch/observesDynamoCentralize
    ```

:::tip
All aws batch executions have their local job equivalent. See
the `computeOnAwsBatch` job definition to view the underlying local command.
:::

## Data-schema determination

This process infer data-schema from raw data and stores the determined
data-schemas into _observes.cache_ s3 bucket for serving as a cache.

This process is triggered by an schedule. It has a frequency of execution
of one week.

```bash
m . /computeOnAwsBatch/observesDynamoSchema
```

## Common issues

ETL jobs are unstable because of redshift or aws unhandled errors.
This are the most common issues:

### CannotInspectContainerError

- Reason: the job finish in an unknown state from aws batch perspective

- Resolution: verify job log (possible false negative)

### InternalError: Out of Memory

- Reason: unknown

- Hypothesis: high db usage demand from concurrent `s3 -> redshift` operations

- Resolution: re-execution (it is likely to need only partial re-execution)

### Host terminated

- Reason: the spot nature of the instances used at aws batch

- Resolution: re-execution

## Rare issues

Some ETL unhandled errors are not frequent

### Stuck queries

- Reason: unknown

- Resolution: [prevent-locks-blocking-queries](https://aws.amazon.com/es/premiumsupport/knowledge-center/prevent-locks-blocking-queries-redshift/#Resolution).

### InternalError stl_load_errors

- Reason: issue [#8258](https://gitlab.com/fluidattacks/universe/-/issues/8258)

- Resolution: unknown (try re-execution)

- Note: this issue should not be raised since the issue was solved

## Partial re-execution

If the job completed to upload data to s3 then a re-upload to redshift can be
done with:

```bash
m . /computeOnAwsBatch/observesRetryRedshiftUpload "{nnn}"
```

Where {nnn} has to be replaced by the number of the segment to be retried.

## Full re-execution

If the job **does not** fully upload data to s3 then full re-execution is
needed:

```bash
m . /computeOnAwsBatch/observesDynamoSegment "{total_segments}" "{segment}"
```

Where {segment} has to be replaced by the number of the segment to be retried,
and {total_segments} with the total number of segments
