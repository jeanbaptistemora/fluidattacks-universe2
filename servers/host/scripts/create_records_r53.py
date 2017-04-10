# -*- coding: utf-8 -*-
"""Modulo para creación de los registros DNS en Route53.
"""
# 3rd party imports
import boto3

# local imports
# none

IP_ADDRESS_FILE = '/tmp/instance_ip.txt'
HOST_ZONE_ID = 'Z97LJOL6ETZND'


def upsert_ip():

    client = boto3.client('route53')
    with open(IP_ADDRESS_FILE) as ip_fd:
        IP_ADDRESS = ip_fd.read().rstrip()
    client.change_resource_record_sets(
        HostedZoneId=HOST_ZONE_ID,
        ChangeBatch={
            'Changes': [
                {
                 'Action': 'UPSERT',
                 'ResourceRecordSet': {
                     'Name': 'prueba.fluid.la',
                     'Type': 'A',
                     'TTL': 300,
                     'ResourceRecords': [
                         {
                          'Value': IP_ADDRESS
                         },
                     ],
                 }
                 },
            ]
        },
    )


upsert_ip()
