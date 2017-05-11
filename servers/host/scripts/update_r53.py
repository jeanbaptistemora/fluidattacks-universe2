
import boto3

ID_HZ = "Z97LJOL6ETZND"
REGION_NAME = 'us-east-1'
IP_ADDRESS_FILE = '/tmp/instance_ip.txt'


def make_update(ip):

    client = boto3.client('route53',
                          region_name=REGION_NAME,)

    response = client.change_resource_record_sets(
                    HostedZoneId=ID_HZ,
                    ChangeBatch={
                        'Comment': 'Cambio de Server',
                        'Changes': [
                            {
                                'Action': 'UPSERT',
                                'ResourceRecordSet': {
                                    'Name': 'fluid.la.',
                                    'Type': 'A',
                                    'TTL': 300,
                                    'ResourceRecords': [
                                        {
                                            'Value': ip
                                        },
                                    ]
                                }
                            },
                            {
                                'Action': 'UPSERT',
                                'ResourceRecordSet': {
                                    'Name': 'mail.fluid.la.',
                                    'Type': 'A',
                                    'TTL': 300,
                                    'ResourceRecords': [
                                        {
                                            'Value': ip
                                        },
                                    ]
                                }
                            },
                            ]
                    }
                )
    print response


def main():

    lines = open(IP_ADDRESS_FILE, "r")
    ips = lines.readlines()
    make_update(ips[0])


main()
