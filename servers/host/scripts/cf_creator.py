# -*- coding: utf-8 -*-


"""Modulo para despliegue de stacks de Cloud Formation"""

# standard imports
import time

# 3rd party imports

import boto3

# GLOBAL VARIABLES
KEYNAME = "FLUIDServes_Dynamic"
REGION_NAME = 'us-east-1'
INSTANCE_ID_FILE = '/tmp/instance_id.txt'
IP_ADDRESS_FILE = '/tmp/instance_ip.txt'

'''Funcion que crea el Stack en CF
   Input> CF JSON, nombre del stack, nombre de instancia, tipo de stack
        tipo de stack = 0 para instance EC2
                        1 para el resto
   Output> none'''


def deploy_cloudformation(jsonO, stackname, name, type):

    try:
        print "-> Creando el Stack "+stackname+"..."
        client = boto3.client('cloudformation',
                              region_name=REGION_NAME,)

        response = client.create_stack(
            StackName=stackname,
            TemplateBody=str(jsonO),
            DisableRollback=False,
            TimeoutInMinutes=10,
            ResourceTypes=[
                'AWS::*',
                ],
            Tags=[
                {
                 'Key': 'Name',
                 'Value': name
                },
                ]
        )
        verify_creation(client, response["StackId"], type)
    except Exception as ex:
        print "-> ERROR:\n"+str(ex)+"\n"
        print "-> El Stack "+stackname+" ya existe, actualizando..."
        update_stackcf(jsonO, stackname, name, type)


'''Funcion que valida la creacion del stack en CF
   Input> CF JSON
   Output> none'''


def verify_creation(client, stackid, type):

    isnotcreated = True
    consult = ""
    while isnotcreated:
        consult = client.describe_stacks(
            StackName=stackid,
            )
        if consult["Stacks"][0]["StackStatus"] == 'CREATE_COMPLETE' or\
           consult["Stacks"][0]["StackStatus"] == 'UPDATE_COMPLETE':
            isnotcreated = False
            print "-> Stack "+stackid+" creado con exito"
        elif consult["Stacks"][0]["StackStatus"] == 'ROLLBACK_IN_PROGRESS' or \
                consult["Stacks"][0]["StackStatus"] == 'CREATE_FAILED' or \
                consult["Stacks"][0]["StackStatus"] == \
                "UPDATE_ROLLBACK_IN_PROGRESS":
            print "-> No se ha podido crear el Stack "+stackid
            print "-> Response: "+consult
            print ""

        else:
            time.sleep(1)

    if type == 0:
        instance_id = consult["Stacks"][0]["Outputs"][0]["OutputValue"]
        ip_address = consult["Stacks"][0]["Outputs"][2]["OutputValue"]

        with open(INSTANCE_ID_FILE, 'w') as instance_fd:
            instance_fd.write(instance_id)
        with open(IP_ADDRESS_FILE, 'w') as ip_fd:
            ip_fd.write(ip_address)


'''Funcion que elimina Stack en CF
   Input> nombre del stack
   Output> none'''


def delete_stackcf(stackname):

    client = boto3.client('cloudformation',
                          region_name=REGION_NAME,)

    response = client.delete_stack(StackName=stackname)

    print response


'''Funcion que actualiza el Stack en CF
   Input> CF JSON, nombre del stack, nombre de instancia, tipo de stack
        tipo de stack = 0 para instance EC2
                        1 para el resto
   Output> none'''


def update_stackcf(jsonO, stackname, name, type):

    try:
        client = boto3.client('cloudformation',
                              region_name=REGION_NAME,)

        response = client.update_stack(
            StackName=stackname,
            TemplateBody=str(jsonO),
            UsePreviousTemplate=False,
            Tags=[
                {
                 'Key': 'Name',
                 'Value': name
                },
                ]
            )

        verify_creation(client, response["StackId"], type)
    except Exception as ex:
        print "-> ERROR:\n"+str(ex)+"\n"
        print "-> El Stack "+stackname+" no pudo ser actualizado"
        if "No updates are to be performed." in str(ex):
            print "-> El Stack "+stackname+" no contiene actualizaciones"
