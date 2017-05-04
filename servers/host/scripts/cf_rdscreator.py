# -*- coding: utf-8 -*-


"""Modulo para creación de BD RDS con
Cloud Formation
"""

import os
# 3rd party imports
from troposphere import GetAtt,  Output
from troposphere import Ref, Tags, Template
from troposphere.rds import DBInstance, DBSubnetGroup
from troposphere.ec2 import PortRange, NetworkAcl, Route, \
    VPCGatewayAttachment, SubnetRouteTableAssociation, Subnet, RouteTable, \
    VPC, NetworkAclEntry, \
    SubnetNetworkAclAssociation, InternetGateway, \
    SecurityGroupRule, SecurityGroup
import cf_creator


# GLOBAL VARIABLES
DB_TYPE = "db.m1.small"
REGION_NAME = 'us-east-1'
DBData_FILE = '.dbdata.txt'

# In GB
BD_DISK = "5"


class CFRDSCreator():

    def __init__(self, iprangev="", namev="", ipranges="", names="",
                 namegtw="", SGrules=[], aclentry=[]):

        self.template = Template()
        self.ref_stack_id = Ref('AWS::StackId')
        self.ref_region = Ref('AWS::Region')
        self.VPC = self.create_vpc(self.template, "172.35.0.0/16", namev)

        self.Subnet = self.create_subnet(self.template, self.VPC,
                                         "172.35.1.0/24", names,
                                         REGION_NAME+'a')

        self.BDSubnet = self.create_subnet(self.template, self.VPC,
                                           "172.35.2.0/24", "RDS1",
                                           REGION_NAME+'b')

        self.BDSubnet1 = self.create_subnet(self.template, self.VPC,
                                            "172.35.3.0/24", "RDS2",
                                            REGION_NAME+'c')

        self.BDSubnet2 = self.create_subnet(self.template, self.VPC,
                                            "172.35.4.0/24", "RDS3",
                                            REGION_NAME+'d')

        self.BDSubnet3 = self.create_subnet(self.template, self.VPC,
                                            "172.35.5.0/24", "RDS4",
                                            REGION_NAME+'e')

        self.InterGTW = self.create_intergtw(self.template,
                                             self.VPC, namegtw)

        self.create_routetable(self.template, self.VPC, self.Subnet)

        self.create_ACL(self.template, self.VPC, self.Subnet, aclentry)

        self.securityGroup = self.create_securitygroup(self.template,
                                                       self.VPC,
                                                       SGrules)

    '''Fucion que genera una instancia de EC2 en CF con los parametros dados'''
    def create_rds(self, dbname, username, password):

        subnetgroup = DBSubnetGroup(
                                    'DBSubnetGroup',
                                    DBSubnetGroupDescription="Grupo de subnet \
                                    de Exams RDS",
                                    SubnetIds=[Ref(self.Subnet),
                                               Ref(self.BDSubnet),
                                               Ref(self.BDSubnet1),
                                               Ref(self.BDSubnet2),
                                               Ref(self.BDSubnet3)],
                                    )
        mydbsubnetgroup = self.template.add_resource(subnetgroup)

        mydb = DBInstance(
                            "RDSExamsBD",
                            DBName=dbname,
                            AllocatedStorage=BD_DISK,
                            DBInstanceClass=DB_TYPE,
                            Engine="MySQL",
                            EngineVersion="5.6",
                            MasterUsername=username,
                            MasterUserPassword=password,
                            DBSubnetGroupName=Ref(mydbsubnetgroup),
                            VPCSecurityGroups=[Ref(self.securityGroup), ],
                            PubliclyAccessible=True,
                            Tags=Tags(Name="RDS Exams BD",))

        self.template.add_resource(mydb)

        self.template.add_output([
                Output(
                    "Address",
                    Description="Address of the RDS"
                    "instance",
                    Value=GetAtt(mydb, "Endpoint.Address"),),
                Output(
                    "Port",
                    Description="Port of the RDS"
                    "instance",
                    Value=GetAtt(mydb, "Endpoint.Port"),),
                ])

    def create_vpc(self, t, iprange, name):

        vpc = self.template.add_resource(VPC(
            'VPC',
            CidrBlock=iprange,
            EnableDnsSupport=True,
            EnableDnsHostnames=True,
            Tags=Tags(
                Application=self.ref_stack_id, Name=name)))
        return vpc

    def create_subnet(self, t, VPC, iprange, name, region):

        subnet = self.template.add_resource(
            Subnet(
                name,
                AvailabilityZone=region,
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

    SGrules = secgroup_rules("servers/host/vars/CFvars/rdssecgrorul.txt")
    aclentry = acl_entries("servers/host/vars/CFvars/rdsacl.txt")

    # Crea Stack con VPC
    archivo_ips = open('servers/host/vars/CFvars/iprangeec2.txt', "r")
    ips = archivo_ips.readlines()

    creator = CFRDSCreator(ips[0].split("\n")[0], "FluidRDS",
                           ips[1].split("\n")[0], "FluidRDSSrv",
                           "FluidRDS", SGrules, aclentry)
    filepath = os.path.join(os.path.expanduser('~'), DBData_FILE)
    dbdata = open(filepath, "r").readlines()
    name = dbdata[0].split()[0]
    username = dbdata[0].split()[1]
    passwd = dbdata[0].split()[2]
    creator.create_rds(name, username, passwd)
    cf_creator.deploy_cloudformation(creator.template.to_json(),
                                     "FLUIDServesRDS2",
                                     "FLUIDServes RDS", 3)


main()
