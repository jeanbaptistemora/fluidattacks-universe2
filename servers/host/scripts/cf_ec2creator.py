# -*- coding: utf-8 -*-


"""Modulo para creación de máquina host para contenedores Docker con
Cloud Formation
"""
# standard imports
import os
import time
# 3rd party imports
from troposphere import GetAtt,  Output
from troposphere import Ref, Tags, Template
from troposphere.ec2 import EIP
import troposphere.ec2 as ec2
import boto3
import cf_creator

# GLOBAL VARIABLES
KEYNAME = "FLUIDServes_Dynamic"
INSTANCE = "FLUIDServesInstance"
IMAGE_ID = "ami-ad593cbb"
INSTANCE_TYPE = "t2.small"
REGION_NAME = 'us-east-1'
STACK_NAME = 'FLUIDServesDynamicTest'
# In GB
INSTANCE_DISK = "100"

INSTANCE_ID_FILE = '/tmp/instance_id.txt'
IP_ADDRESS_FILE = '/tmp/instance_ip.txt'
VPC_FILE = 'servers/host/vars/CFvars/vpc_info.txt'


class CFEC2Creator():

    def __init__(self):

        self.template = Template()
        self.ref_stack_id = Ref('AWS::StackId')
        self.ref_region = Ref('AWS::Region')
        try:
            vpcs = open(VPC_FILE, "r").readlines()
            print "ok"
            self.vpcid = vpcs[0].split()[0]
            self.groupid = vpcs[0].split()[1]
            self.subnetid = vpcs[0].split()[2]
        except Exception as ex:
            print "-> ERROR:\n"+str(ex)+"\n"
            print "-> No se pudo crear el EC2"

    '''Fucion que genera una instancia de EC2 en CF con los parametros dados'''

    def create_ec2(self, keyname, instance, imageid, instancetype):

        eth0 = self.template.add_resource(ec2.NetworkInterface(
            "Eth0",
            Description="eth0",
            GroupSet=[self.groupid, ],
            SourceDestCheck=True,
            SubnetId=self.subnetid,
            Tags=Tags(
                Name="Interface 0",
                Interface="eth0",
                ),
            ))

        instance = ec2_instance = ec2.Instance(
            INSTANCE,
            ImageId=IMAGE_ID,
            KeyName=KEYNAME,
            NetworkInterfaces=[
                    ec2.NetworkInterfaceProperty(
                        NetworkInterfaceId=Ref(eth0),
                        DeviceIndex="0",
                        ),
                    ],
            BlockDeviceMappings=[
                ec2.BlockDeviceMapping(
                    DeviceName="/dev/xvda",
                    Ebs=ec2.EBSBlockDevice(
                        VolumeSize=INSTANCE_DISK
                            )
                        ),
                    ],
            Tags=Tags(Name=INSTANCE,)
            )
        instance.InstanceType = INSTANCE_TYPE

        ec2_instance = self.template.add_resource(instance)

        self.template.add_resource(
            EIP('IPAddress',
                Domain='vpc',
                InstanceId=Ref(ec2_instance)
                ))

        self.template.add_output([
                Output(
                    "InstanceId",
                    Description="InstanceId of the newly created EC2 instance",
                    Value=Ref(ec2_instance),
                ),
                Output(
                    "AZ",
                    Description="Availability Zone of the newly created EC2 "
                    "instance",
                    Value=GetAtt(ec2_instance, "AvailabilityZone"),),
                Output(
                    "PublicIP",
                    Description="Public IP address of the newly created EC2 "
                    "instance",
                    Value=GetAtt(ec2_instance, "PublicIp"),
                    ),
                Output(
                    "SecGroupID",
                    Description="ID of the secgroup of the newly created EC2 "
                    "instance",
                    Value=self.groupid,
                    ),
                Output(
                    "PrivateIP",
                    Description="Private IP address of the newly created EC2 "
                    "instance",
                    Value=GetAtt(ec2_instance, "PrivateIp"),
                ),
                Output(
                    "PublicDNS",
                    Description="Public DNSName of the newly created EC2 "
                    "instance",
                    Value=GetAtt(ec2_instance, "PublicDnsName"),
                ),
                Output(
                    "PrivateDNS",
                    Description="Private DNSName of the newly created EC2 "
                    "instance",
                    Value=GetAtt(ec2_instance, "PrivateDnsName"),
                ),
                ])


'''Funcion crea el KEY para el ssh
   Input> none
   Output> none'''


def create_key_pair():

    client = boto3.client(
        'ec2',
        region_name='us-east-1',
    )
    try:
        client.delete_key_pair(KeyName=KEYNAME)
    except:
        pass
    response = client.create_key_pair(KeyName=KEYNAME)

    key_file = '/tmp/' + KEYNAME + '.pem'
    with open(key_file, 'w') as key_fd:
        key_fd.write(response['KeyMaterial'])
    os.chmod(key_file, 0400)


def main():

    create_key_pair()

    # Crea Stack con EC2
    creator = CFEC2Creator()
    stackname = "FLUIDServesDynamic" + time.strftime("%Y%m%d%I%M")
    creator.create_ec2(KEYNAME, INSTANCE, IMAGE_ID, INSTANCE_TYPE)
    cf_creator.deploy_cloudformation(creator.template.to_json(),
                                     stackname,
                                     "FLUIDServes Instance", 0)


main()
