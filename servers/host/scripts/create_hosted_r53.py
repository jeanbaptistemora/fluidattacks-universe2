# -*- coding: utf-8 -*-

"""Modulo para creación de los registros DNS en Route53.
"""

# standard imports
import time
# 3rd party imports
import boto3

# local imports
# none
HOSTED_ZONE_ID = '/tmp/hosted-zones.txt'
HOSTED_ZONES = ["fluidsignaltest.com", "fluidtest.la", "fluidsignaltest.co"]


def create_zone():
        with open(HOSTED_ZONE_ID, 'a') as hosted_fd:
		zones = HOSTED_ZONES,
		for zone in HOSTED_ZONES:
    			client = boto3.client('route53')
			response = client.create_hosted_zone(
    				Name = zone,
    				CallerReference='Creacion'+ zone + time.strftime("%H:%M:%S"),
    				HostedZoneConfig={
        			'PrivateZone': False
    				},
			)
			hosted_id = response['HostedZone']['Id'].split('/')[2]
           		hosted_fd.write(hosted_id)
create_zone()
