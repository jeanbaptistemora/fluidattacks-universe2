# -*- coding: utf-8 -*-


"""Modulo para verificacion de emails y domains de Amazon con boto3"""

# standard imports
import time
import sys
# 3rd party imports

import boto3


# GLOBAL VARIABLES
REGION_NAME = 'us-east-1'
SESEMAIL_KEYS = []
SESDOMAIN_KEYS = []
EMAIL_KEY_FILE = '/tmp/email_key.txt'
DOMAIN_KEY_FILE = '/tmp/domain_key.txt'


class amazonSESCreator():

    def __init__(self):

        self.client = boto3.client('ses', region_name=REGION_NAME,)

    def send_email_verification(self, email):

        print "-> Verificando el email " + email
        try:

            self.client.verify_email_address(
                        EmailAddress=email
                        )

            print "-> Se ha enviado un correo a "+email+" para su verificacion"
        except:
            print "No se pudo enviar verificacion a " + email

    def send_domain_verification(self, domain):

        print "-> Verificando el dominio " + domain
        try:

            response = self.client.verify_domain_identity(
                Domain=domain
                )

            print "-> Se ha creado la key para "+domain+", se verificara"
            " al crear el registro en el DNS"

            with open(DOMAIN_KEY_FILE, 'a') as ip_fd:
                ip_fd.write("_amazonses." + domain+" " +
                            response["VerificationToken"] + "\n")

        except:
            print sys.exc_info()
            print "\nNo se pudo enviar verificacion a "+domain

    def verify_identity_creation(self, identity):

        print "-> Esperando a que se verifique "+identity+" ..."
        verified = False
        while not verified:
            response = self.client.get_identity_verification_attributes(
                        Identities=[
                                identity,
                                    ]
                    )
            s = response["VerificationAttributes"][identity]
            status = s["VerificationStatus"]

            if status != 'Pending':
                verified = True
            else:
                time.sleep(1)

    def get_dkim(self, identity):

            response = self.client.get_identity_dkim_attributes(
                    Identities=[
                                identity,
                                ]
                            )
            dkim = response["DkimAttributes"][identity]["DkimTokens"]
            domain = identity.split("@")

            for i in dkim:
                with open(EMAIL_KEY_FILE, 'a') as ip_fd:
                    ip_fd.write(i+"._domainkey."+domain[1]+" "+i+"\n")

    def setdkimenabled(self, identity, option):

        try:
            self.client.set_identity_dkim_enabled(
                Identity=identity,
                DkimEnabled=option)
        except:
            pass


def empty_files():
    with open(EMAIL_KEY_FILE, 'w') as ip_fd:
                    ip_fd.write("")

    with open(DOMAIN_KEY_FILE, 'w') as ip_fd:
        ip_fd.write("")


def main():

    domains = []

    lines = open("servers/host/vars/sesvars/domains.txt", "r")
    domains = lines.readlines()

    emails = []

    lines = open("servers/host/vars/sesvars/emails.txt", "r")
    emails = lines.readlines()

    sescreator = amazonSESCreator()
    empty_files()
    for i in domains:
        sescreator.send_domain_verification(i.split("\n")[0])
    for i in emails:
        email = i.split()
        print email
        sescreator.send_email_verification(email[0])
        sescreator.verify_identity_creation(email[0])
        if email[1] == '1':
            sescreator.get_dkim(email[0])
            sescreator.setdkimenabled(email[0], True)
        else:
            sescreator.setdkimenabled(email[0], False)


main()
