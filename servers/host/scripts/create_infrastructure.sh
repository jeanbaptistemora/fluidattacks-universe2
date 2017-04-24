#!/bin/bash

# # Realiza verificaciones de emails y domains de AmazonSES
# python servers/host/scripts/amazonses_creator.py

# Crea las instancias de EC2, VPC, ACL y Security Groups
python servers/host/scripts/cf_ec2creator.py

# # Crea el DNS de Route53 y los registros de DNS
# python servers/host/scripts/cf_r53creator.py
#
# # Crea los Buckets S3
# python servers/host/scripts/cf_s3creator.py
