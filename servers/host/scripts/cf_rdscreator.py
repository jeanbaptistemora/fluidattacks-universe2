# -*- coding: utf-8 -*-


"""Modulo para creación de BD RDS con
Cloud Formation
"""

import os
# 3rd party imports
from troposphere import GetAtt,  Output
from troposphere import Ref, Tags, Template
from troposphere.rds import DBInstance, DBSubnetGroup
import boto3
import cf_creator


# GLOBAL VARIABLES
KEYNAME = "FLUIDServes_Dynamic"
INSTANCE = "FLUIDServesInstance"
IMAGE_ID = "ami-49e5cb5e"
DB_TYPE = "db.m1.small"
REGION_NAME = 'us-east-1'
VPC_IDS_FILE = 'servers/host/vars/CFvars/vpc_ids.txt'
DBData_FILE = '.dbdata.txt'

# In GB
BD_DISK = "5"

INSTANCE_ID_FILE = '/tmp/instance_id.txt'
IP_ADDRESS_FILE = '/tmp/instance_ip.txt'


class CFRDSCreator():

    def __init__(self):

        self.template = Template()
        self.ref_stack_id = Ref('AWS::StackId')
        self.ref_region = Ref('AWS::Region')

    '''Fucion que genera una instancia de EC2 en CF con los parametros dados'''
    def create_rds(self, dbname, username, password):
        ec2 = boto3.resource('ec2',
                             region_name=REGION_NAME,)
        vpcs = open(VPC_IDS_FILE, "r").readlines()
        vpcid = vpcs[0].split()[0]
        groupid = vpcs[0].split()[1]
        vpc = ec2.Vpc(vpcid)

        subnet_iterator = vpc.subnets.all()
        subnets = []
        for i in subnet_iterator:
            subnets.append(i.subnet_id)

        subnetgroup = DBSubnetGroup(
                                    'DBSubnetGroup',
                                    DBSubnetGroupDescription="Grupo de subnet \
                                    de Exams RDS",
                                    SubnetIds=subnets,
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
                            VPCSecurityGroups=[groupid, ],
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


def main():

    creator = CFRDSCreator()
    filepath = os.path.join(os.path.expanduser('~'), DBData_FILE)
    dbdata = open(filepath, "r").readlines()
    name = dbdata[0].split()[0]
    username = dbdata[0].split()[1]
    passwd = dbdata[0].split()[2]
    creator.create_rds(name, username, passwd)
    cf_creator.deploy_cloudformation(creator.template.to_json(),
                                     "FLUIDServesRDS",
                                     "FLUIDServes RDS", 3)


main()
