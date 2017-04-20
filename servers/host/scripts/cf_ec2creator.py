# -*- coding: utf-8 -*-


"""Modulo para creación de máquina host para contenedores Docker con
Cloud Formation
"""
# standard imports
import os
# 3rd party imports
from troposphere import GetAtt,  Output
from troposphere import Ref, Tags, Template
from troposphere.ec2 import PortRange, NetworkAcl, Route, \
    VPCGatewayAttachment, SubnetRouteTableAssociation, Subnet, RouteTable, \
    VPC, NetworkAclEntry, \
    SubnetNetworkAclAssociation, EIP, InternetGateway, \
    SecurityGroupRule, SecurityGroup
import troposphere.ec2 as ec2
import boto3
import cf_creator

# GLOBAL VARIABLES
KEYNAME = "FLUIDServes_Dynamic"
INSTANCE = "FLUIDServesInstance"
IMAGE_ID = "ami-49e5cb5e"
INSTANCE_TYPE = "t2.small"
REGION_NAME = 'us-east-1'
STACK_NAME = 'FLUIDServesDynamicTest'
# In GB
INSTANCE_DISK = "20"

INSTANCE_ID_FILE = '/tmp/instance_id.txt'
IP_ADDRESS_FILE = '/tmp/instance_ip.txt'


class CFEC2Creator():

    def __init__(self, iprangev="", namev="", ipranges="", names="",
                 namegtw="", SGrules=[], aclentry=[]):

        self.template = Template()
        self.ref_stack_id = Ref('AWS::StackId')
        self.ref_region = Ref('AWS::Region')

        if iprangev != "":

            self.VPC = self.create_vpc(self.template, iprangev, namev)

            self.Subnet = self.create_subnet(self.template, self.VPC, ipranges,
                                             names)

            self.InterGTW = self.create_intergtw(self.template,
                                                 self.VPC, namegtw)

            self.create_routetable(self.template, self.VPC, self.Subnet)

            self.create_ACL(self.template, self.VPC, self.Subnet, aclentry)

            self.securityGroup = self.create_securitygroup(self.template,
                                                           self.VPC, SGrules)

    '''Fucion que genera una instancia de EC2 en CF con los parametros dados'''
    def create_ec2(self, keyname, instance, imageid, instancetype):

        eth0 = self.template.add_resource(ec2.NetworkInterface(
            "Eth0",
            Description="eth0",
            GroupSet=[Ref(self.securityGroup), ],
            SourceDestCheck=True,
            SubnetId=Ref(self.Subnet),
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
                DependsOn='AttachGateway',
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
                    Value=GetAtt(self.securityGroup, "GroupId"),
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

    def create_vpc(self, t, iprange, name):

        vpc = self.template.add_resource(VPC(
            'VPC',
            CidrBlock=iprange,
            Tags=Tags(
                Application=self.ref_stack_id, Name=name)))
        return vpc

    def create_subnet(self, t, VPC, iprange, name):

        subnet = self.template.add_resource(
            Subnet(
                'Subnet',
                CidrBlock=iprange,
                VpcId=Ref(VPC),
                Tags=Tags(
                    Application=self.ref_stack_id, Name=name)))
        return subnet

    def create_intergtw(self, t, VPC, name):

        internetGateway = self.template.add_resource(
            InternetGateway(
                'InternetGateway',
                Tags=Tags(
                    Application=self.ref_stack_id, Name=name)))

        self.template.add_resource(
            VPCGatewayAttachment(
                'AttachGateway',
                VpcId=Ref(VPC),
                InternetGatewayId=Ref(internetGateway)))

        return internetGateway

    def create_routetable(self, t, VPC, subnet):

        routeTable = self.template.add_resource(
            RouteTable(
                'RouteTable',
                VpcId=Ref(VPC),
                Tags=Tags(
                    Application=self.ref_stack_id)))

        self.template.add_resource(
            Route(
                'Route',
                DependsOn='AttachGateway',
                GatewayId=Ref('InternetGateway'),
                DestinationCidrBlock='0.0.0.0/0',
                RouteTableId=Ref(routeTable),
                ))

        self.template.add_resource(
            SubnetRouteTableAssociation(
                    'SubnetRouteTableAssociation',
                    SubnetId=Ref(subnet),
                    RouteTableId=Ref(routeTable),
                ))

    def create_ACL(self, t, VPC, subnet, aclentry):

        networkAcl = self.template.add_resource(
            NetworkAcl(
                'NetworkAcl',
                VpcId=Ref(VPC),
                Tags=Tags(
                    Application=self.ref_stack_id),
            ))

        for i in aclentry:
            self.template.add_resource(
                NetworkAclEntry(
                        i[0],
                        NetworkAclId=Ref(networkAcl),
                        RuleNumber=i[1],
                        Protocol=i[2],
                        PortRange=PortRange(To=i[3], From=i[4]),
                        Egress=i[5],
                        RuleAction=i[6],
                        CidrBlock=i[7],
                        ))

        self.template.add_resource(
            SubnetNetworkAclAssociation(
                'SubnetNetworkAclAssociation',
                SubnetId=Ref(subnet),
                NetworkAclId=Ref(networkAcl),
                ))

    def create_securitygroup(self, t, VPC, SGrules):

        # BASADO EN EL DE PROD
        sec_rules = []
        for i in SGrules:
            sec_rules.append(SecurityGroupRule(
                IpProtocol=i[0],
                FromPort=i[1],
                ToPort=i[2],
                CidrIp=i[3]))

        instanceSecurityGroup = self.template.add_resource(
            SecurityGroup(
                'InstanceSecurityGroup',
                GroupDescription='Grupo de seguridad para fluidserves',
                SecurityGroupIngress=sec_rules,
                VpcId=Ref(VPC),
                ))
        return instanceSecurityGroup


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


def acl_entries(txtfile):

    aclentry = []

    with open(txtfile) as f:
        lines = f.readlines()

        for line in lines:
            entries = line.split()
            aclentry.append([entries[0], entries[1], entries[2], entries[3],
                            entries[4], entries[5], entries[6], entries[7]])

    return aclentry


def secgroup_rules(txtfile):

    SGrules = []

    with open(txtfile) as f:
        lines = f.readlines()

        for line in lines:
            entries = line.split()
            SGrules.append([entries[0], entries[1], entries[2], entries[3]])

    return SGrules


def main():

    create_key_pair()
    SGrules = secgroup_rules("servers/host/vars/CFvars/ec2secgrorul.txt")
    aclentry = acl_entries("servers/host/vars/CFvars/ec2acl.txt")

    # Crea Stack con EC2
    archivo_ips = open('servers/host/vars/CFvars/iprangeec2.txt', "r")
    ips = archivo_ips.readlines()
    creator = CFEC2Creator(ips[0].split("\n")[0], "FluidNet",
                           ips[1].split("\n")[0], "FluidNetSrv",
                           "FluidNet", SGrules, aclentry)

    creator.create_ec2(KEYNAME, INSTANCE, IMAGE_ID, INSTANCE_TYPE)
    cf_creator.deploy_cloudformation(creator.template.to_json(),
                                     "FLUIDServesDynamic",
                                     "FLUIDServes Instance", 0)


main()
