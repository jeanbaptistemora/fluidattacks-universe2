# -*- coding: utf-8 -*-


"""Modulo para creación de Buckets S3 con Cloud Formation
"""

# 3rd party imports
from troposphere import Output
from troposphere import Ref, Template
from troposphere.s3 import Bucket
import cf_creator

# GLOBAL VARIABLES
KEYNAME = "FLUIDServes_Dynamic"
REGION_NAME = 'us-east-1'


class CFBucketCreator():

    def __init__(self):

        self.template = Template()

    def create_bucket(self, name):

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


def main():

    # Crea Stack de Bucket S3
    s3creator = CFBucketCreator()
    s3creator.create_bucket("fluidserves")
    cf_creator.deploy_cloudformation(s3creator.template.to_json(),
                                     "FLUIDS3Serves", "FLUID Serves S3", 1)

    s3creator = CFBucketCreator()
    s3creator.create_bucket("fluidstores")
    cf_creator.deploy_cloudformation(s3creator.template.to_json(),
                                     "FLUIDS3Stores", "FLUID Stores S3", 1)


main()
