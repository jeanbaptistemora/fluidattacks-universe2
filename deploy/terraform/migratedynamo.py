import boto3
import sys

newkey = sys.argv[1]
newsecret = sys.argv[2]

oldkey = sys.argv[3]
oldsecret = sys.argv[4]

dynamoclient = boto3.client('dynamodb', region_name='us-east-1',
    aws_access_key_id=oldkey,
    aws_secret_access_key=oldsecret)

dynamotargetclient = boto3.client('dynamodb', region_name='us-east-1',
    aws_access_key_id=newkey,
    aws_secret_access_key=newsecret)

tables = ["alerts_by_company",
          "comments",
          "eventualities",
          "findings_email",
          "remediated",
          "toe",
          "weekly_report",
          "projects",
          "project_access",
          "users",
          "findings",
          "vulnerabilities"]

for table in tables:
    dynamopaginator = dynamoclient.get_paginator('scan')
    tabname="FI_"+table
    targettabname="FI_"+table
    dynamoresponse = dynamopaginator.paginate(
        TableName=tabname,
        Select='ALL_ATTRIBUTES',
        ReturnConsumedCapacity='NONE',
        ConsistentRead=True
    )
    for page in dynamoresponse:
        for item in page['Items']:
            dynamotargetclient.put_item(
                TableName=targettabname,
                Item=item
            )
