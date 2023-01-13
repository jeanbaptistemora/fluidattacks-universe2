---
id: zoho-etl
title: Zoho CRM ETL
sidebar_label: ZohoCRM
slug: /development/zoho-etl
---

This ETL process extracts data from the Zoho CRM api and sends it to
the warehouse (redshift).

:::note
Local execution and sending of jobs will require to
[setup your terminal](/development/setup/terminal) and have access to the
`prod_observes` role and the `CACHIX_AUTH_TOKEN` environment variable.
:::

## Architecture

- Prepare

    The ETL request export data on batch jobs through the zoho API. It saves
    the job id on redshift for future retrieval. Job is triggered by an
    schedule; local execution can be done with:

    ```bash
    m . /observes/etl/zoho-crm/fluid
    ```

- Core

    This is the core ETL process which downloads the results of the previously
    requested data.

    ```bash
    m . /observes/etl/zoho-crm/fluid/prepare
    ```

## Common issues

Sometimes the ETL cannot continue normally

### expired bulk data

- Reason: [#5441](https://gitlab.com/fluidattacks/universe/-/issues/5441)

- Resolution: delete bulk_jobs state and retry prepare and core procedures

    ```sql
    delete from zoho_crm.bulk_jobs
    ```

