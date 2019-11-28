# Tap AWS DynamoDB

Reads the [AWS DynamoDB's API](https://aws.amazon.com/dynamodb/),
and persists it to a [Singer](https://www.singer.io/) formatted stream.

# How to install
Download a fresh copy of the source code and install it from source:

```bash
$ cd tap-awsdynamodb
$ python3 -m pip install .
```

Installation requires python 3.6 or later.

# How to update the schema

```bash
cd tap_awsdynamodb

python3 -m pip install --user .

rm -rf /logs/*

echo '{ "AWS_ACCESS_KEY_ID":"'$( \
        vault read -field=aws_dynamodb_access_key secret/serves \
     )'", "AWS_SECRET_ACCESS_KEY":"'$( \
        vault read -field=aws_dynamodb_secret_key secret/serves \
     )'", "AWS_DEFAULT_REGION":"'$( \
        vault read -field=aws_dynamodb_default_region secret/serves \
    )'"}' > /tap_secret.json

tap-awsdynamodb \
    --auth /tap_secret.json \
    --discover > tentative.json

tap-awsdynamodb \
    --auth /tap_secret.json \
    --conf ../../conf/awsdynamodb.json \
    --update-config tentative.json > pre-final.json

mv pre-final.json ../../conf/awsdynamodb.json
```

Then fill the diffs manually

# Sponsor

[![Fluid attacks logo][logo]](https://fluidattacks.com/)

[logo]: https://fluidattacks.com/web/theme/images/logo.png
