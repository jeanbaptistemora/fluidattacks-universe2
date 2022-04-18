# Target Redshift

Reads a [Singer](https://www.singer.io/) formatted stream from stdin,
and persists it to [Amazon Redshift](https://aws.amazon.com/redshift/).

Data is bulk loaded through a native implementation of Redshift Queries, it's fast, reliable, and resource efficient.

# How to install
Download a fresh copy of the source code and install from source:

```bash
$ cd target-redshift
$ python3 -m pip install .
```

Installation requires python 3.6 or later.

# How to use
Create a JSON authentication file and save it as `auth.json`:

```json
{
    "dbname": "database_name",
    "user": "database_user",
    "password": "database_password",
    "host": "xxxxx.xxxx.us-east-1.redshift.amazonaws.com",
    "port": "5439"
}
```

Now pass it as argument to target-redshift:

```bash
$ tap-any-singer-tap | target-redshift --auth auth.json --drop-schema --schema-name "schema_name"
```

It will automatically run a VACUUM operation on your tables after the loading process to guarantee maximum query efficiency.

# Sponsor

[![Fluid attacks logo][logo]](https://fluidattacks.com/)

[logo]: https://fluidattacks.com/theme/images/logo.png
