#!/bin/bash

# # Realiza verificaciones de emails y domains de AmazonSES
# python servers/host/scripts/amazonses_creator.py

# Crea la vpc con subnets
python servers/host/scripts/cf_vpccreator.py

# Crea la bd RDS
python servers/host/scripts/cf_rdscreator.py

# # Crea el DNS de Route53 y los registros de DNS
# python servers/host/scripts/cf_r53creator.py
#
# # Crea los Buckets S3
# python servers/host/scripts/cf_s3creator.py
