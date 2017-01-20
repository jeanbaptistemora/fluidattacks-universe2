# -*- coding: utf-8 -*-

"""Modulo para creación de los registros DNS en Route53.
"""

# 3rd party imports
import boto3

# local imports
# none

IP_ADDRESS_FILE = '/tmp/instance_ip.txt'
HOST_ZONE_ID = 'ZE6FC3YSG85FX'

def upsert_ip():A
	client = boto3.client('route53')
	hostedZoneId = HOST_ZONE_ID

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
