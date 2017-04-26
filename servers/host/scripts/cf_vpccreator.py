# -*- coding: utf-8 -*-


"""Modulo para creación de VPC con
Cloud Formation
"""

# 3rd party imports
from troposphere import GetAtt,  Output
from troposphere import Ref, Tags, Template
from troposphere.ec2 import PortRange, NetworkAcl, Route, \
    VPCGatewayAttachment, SubnetRouteTableAssociation, Subnet, RouteTable, \
    VPC, NetworkAclEntry, \
    SubnetNetworkAclAssociation, InternetGateway, \
    SecurityGroupRule, SecurityGroup

import cf_creator

# GLOBAL VARIABLES
REGION_NAME = 'us-east-1'


class CFVPCCreator():

    def __init__(self, iprangev="", namev="", ipranges="", names="",
                 namegtw="", SGrules=[], aclentry=[]):

        self.template = Template()
        self.ref_stack_id = Ref('AWS::StackId')
        self.ref_region = Ref('AWS::Region')

        if iprangev != "":

            self.VPC = self.create_vpc(self.template, iprangev, namev)

            self.Subnet = self.create_subnet(self.template, self.VPC, ipranges,
                                             names, REGION_NAME+'a')
            self.BDSubnet = self.create_subnet(self.template, self.VPC,
                                               "192.168.100.64/26", "RDS",
                                               REGION_NAME+'b')

            self.InterGTW = self.create_intergtw(self.template,
                                                 self.VPC, namegtw)

            self.create_routetable(self.template, self.VPC, self.Subnet)

            self.create_ACL(self.template, self.VPC, self.Subnet, aclentry)

            self.securityGroup = self.create_securitygroup(self.template,
                                                           self.VPC, SGrules)

            self.setOutputs()

    def setOutputs(self):

        self.template.add_output([
                Output(
                    "SecGroupID",
                    Description="ID of the secgroup of the newly created EC2 "
                    "instance",
                    Value=GetAtt(self.securityGroup, "GroupId"),
                    ),
                ])

    def create_vpc(self, t, iprange, name):

        vpc = self.template.add_resource(VPC(
            'VPC',
            CidrBlock=iprange,
            Tags=Tags(
                Application=self.ref_stack_id, Name=name)))
        return vpc

    def create_subnet(self, t, VPC, iprange, name, azone):

        subnet = self.template.add_resource(
            Subnet(
                name,
                CidrBlock=iprange,
                VpcId=Ref(VPC),
                AvailabilityZone=azone,
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

    SGrules = secgroup_rules("servers/host/vars/CFvars/ec2secgrorul.txt")
    aclentry = acl_entries("servers/host/vars/CFvars/ec2acl.txt")

    # Crea Stack con EC2
    archivo_ips = open('servers/host/vars/CFvars/iprangeec2.txt', "r")
    ips = archivo_ips.readlines()

    creator = CFVPCCreator(ips[0].split("\n")[0], "FluidNet",
                           ips[1].split("\n")[0], "FluidNetSrv",
                           "FluidNet", SGrules, aclentry)
    cf_creator.deploy_cloudformation(creator.template.to_json(),
                                     "FLUIDServesVPC",
                                     "FLUIDServes VPC", 2)


main()
