# -*- coding: utf-8 -*-

"""Modulo para creación de los registros DNS en Route53.
"""

# standard imports
import os
import sys
import time
# 3rd party imports
import boto3

# local imports
# none
HOSTED_ZONE_ID = '/tmp/hosted-zones.txt'


def create_zone():

	zones = ["fluidsignaltest.com", "fluidtest.la", "fluidsignaltest.co"]
	for zone in zones:
    		client = boto3.client('route53')
		response = client.create_hosted_zone(
    			Name = zone,
    			CallerReference='Creacion'+ zone + time.strftime("%H:%M:%S"),
    			HostedZoneConfig={
        		'PrivateZone': False
    			},
		)
		hosted_id = response['HostedZone']['Id'].split('/')[2]
	 	with open(HOSTED_ZONE_ID, 'w') as hosted_fd:
           		hosted_fd.write(hosted_id)
create_zone()
