# -*- coding: utf-8 -*-


"""Modulo para creación de Buckets S3 con Cloud Formation
"""

# 3rd party imports
from troposphere import Output, Join
from troposphere import Ref, Template
from troposphere.s3 import Bucket, BucketPolicy
import awacs
import awacs.s3
import awacs.aws
import cf_creator

# GLOBAL VARIABLES
KEYNAME = "FLUIDServes_Dynamic"
REGION_NAME = 'us-east-1'


class CFBucketCreator():

    def __init__(self):

        self.template = Template()

    def create_policy(self, bucket):

        self.template.add_resource(BucketPolicy(
                    'IPPolicy',
                    Bucket=Ref(bucket),
                    PolicyDocument=awacs.aws.Policy(
                        Id='FLUIDIPpolicy',
                        Version='2012-10-17',
                        Statement=[
                            awacs.aws.Statement(
                                Action=[awacs.aws.Action("s3", "*")],
                                Condition=awacs.aws.Condition(
                                    awacs.aws.IpAddress(
                                                        {"aws:SourceIp":
                                                         "190.156.227.69/32"}
                                    )
                                ),
                                Effect=awacs.aws.Allow,
                                Principal=awacs.aws.Principal(
                                                        awacs.aws.Everybody),
                                Resource=[Join('', [awacs.s3.ARN(''),
                                          Ref(bucket), '/*'])],
                                Sid='IPAllow'
                            ),
                            awacs.aws.Statement(
                                Action=[awacs.aws.Action("s3", "*")],
                                Condition=awacs.aws.Condition(
                                    awacs.aws.IpAddress(
                                                    {"aws:SourceIp":
                                                     "181.55.92.84/32"}
                                    )
                                ),
                                Effect=awacs.aws.Allow,
                                Principal=awacs.aws.Principal(
                                                        awacs.aws.Everybody),
                                Resource=[Join('', [awacs.s3.ARN(''),
                                          Ref(bucket), '/*'])],
                                Sid='IPAllow'
                            ),
                        ]
                    )
                    )
                    )

    def create_bucket(self, name, policy):

        bucket = self.template.add_resource(
            Bucket(
                'Bucket',
                BucketName=name,
                )
        )

        self.template.add_output(Output(
            "BucketName",
            Value=Ref(bucket),
            Description="Name of S3 bucket"
            ))

        if policy:
            self.create_policy(bucket)


def main():

    # Crea Stack de Bucket S3
    s3creator = CFBucketCreator()
    s3creator.create_bucket("fluidpersistent", False)
    cf_creator.deploy_cloudformation(s3creator.template.to_json(),
                                     "FLUIDS3Persistent",
                                     "FLUID Persistent S3", 1)


main()
