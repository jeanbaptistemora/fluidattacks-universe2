# -*- coding: utf-8 -*-

"""Modulo para creación de los registros DNS en Route53.
"""

# standard imports
import os
import sys

# 3rd party imports
import boto3

# local imports
# none

IP_ADDRESS_FILE = '/tmp/instance_ip.txt'

def upsert_ip():
	client = boto3.client('route53')
	hostedZoneId = 'ZE6FC3YSG85FX'

	with open(IP_ADDRESS_FILE) as ip_fd:
		ip = ip_fd.read().rstrip()

	response = client.change_resource_record_sets(
    	HostedZoneId = hostedZoneId,
    	ChangeBatch={
        'Changes': [
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': 'prueba.fluid.com.co',
                    'Type': 'A',
		    'TTL': 300,
                    'ResourceRecords': [
                        {
                            'Value': ip
                        },
                        ],

                    	}		
            		},
            	]
    		}
	)

upsert_ip()
