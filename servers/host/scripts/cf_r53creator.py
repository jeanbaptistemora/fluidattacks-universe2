# -*- coding: utf-8 -*-


"""Modulo para creación de DNS con Route53 de AWS con Cloud Formation"""
# standard imports
import re

# 3rd party imports
from troposphere import Ref, Template
from troposphere.route53 import HostedZone, RecordSetType, \
    HostedZoneConfiguration
import cf_creator

# GLOBAL VARIABLES
KEYNAME = "FLUIDServes_Dynamic"
REGION_NAME = 'us-east-1'
SESEMAIL_KEYS = []
SESDOMAIN_KEYS = []
EMAIL_KEY_FILE = '/tmp/email_key.txt'
DOMAIN_KEY_FILE = '/tmp/domain_key.txt'
IP_ADDRESS_FILE = '/tmp/instance_ip.txt'
DOMAIN_FILE = "servers/host/vars/sesvars/domains.txt"


class CFr53Creator():

    def __init__(self):

        self.template = Template()
        self.ref_stack_id = Ref('AWS::StackId')
        self.records = 0

    def create_r53(self, name, dnsrecord):

        hostedzone = self.template.add_resource(
            HostedZone(
                       "DNS",
                       HostedZoneConfig=HostedZoneConfiguration(
                            Comment="FLUID Hosted Zone",
                            ),
                       Name=name,
                       ))

        for i in dnsrecord:
            iddns = "FLUIDdnsRecord"+str(self.records)
            self.records += 1
            self.template.add_resource(RecordSetType(
                iddns,
                HostedZoneName=name,
                Comment=Ref(hostedzone),
                Name=i[0],
                Type=i[1],
                TTL=i[2],
                ResourceRecords=i[3]
            ))


def dns_records(txtfile, domain):

    ips = []

    lines = open(txtfile, "r")
    ips = lines.readlines()
    kdomains = []

    lines = open(DOMAIN_KEY_FILE, "r")
    kdomains = lines.readlines()

    kemails = []

    lines = open(EMAIL_KEY_FILE, "r")
    kemails = lines.readlines()

    dnsrecord = []

    for i in kdomains:
        ipdomain = i.split()
        dnsrecord.append([ipdomain[0], "TXT", "1800", ['"'+ipdomain[1]+'"']])

    for i in kemails:
        email = i.split()
        dnsrecord.append([email[0], "CNAME", "1800", [email[1]]])

    # 1
    dnsrecord.append([domain, "A", "300", [ips[0]]])
    # 2
    dnsrecord.append([domain, "MX", "86400", ["5 ALT1.ASPMX.L.GOOGLE.COM",
                     "5 ALT2.ASPMX.L.GOOGLE.COM", "10 ALT3.ASPMX.L.GOOGLE.COM",
                      "1 ASPMX.L.GOOGLE.COM.", "10 ALT4.ASPMX.L.GOOGLE.COM"]])
    # 5
    dnsrecord.append([domain, "TXT", "300",
                      ["\"v=spf1 include:_spf.google.com include:servers." +
                       "mcsv.net include:amazonses.com ~all\""]])
    # 8
    a = "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A"
    b = "MIIBCgKCAQEAx+xoz9Br2pk6tPeDrPV/uj7SdMNw9JpxurqL6w"
    c = "1o2f24S4X+QBSR/JaVKoh2FnFj56b9U4R4vWD4aeYk/U5Mwm6A"
    d = "yeXFw/yMG1HwkHDRAna2/gII69ZcH2M+oSCWZwf0IkYT6oyZch"
    e = "7mpFDy5sU26cWWhi+p10mslmpp02eQbMs2fTM9WxlfOiA4kD9B"
    f = "ujFSafhW/yHcUpXVQKoVp+C26ZvmM7hNvK++HoWLxOFtVoxje6"
    g = "zfiE86G1SbXKCuufmcJnjva8K2nYW07qYZAgftBGXJUZTYLYkr"
    h = "MWYK4q4ghcsgJY9zBQpZmFfRcTvoLhZso8SZmt6Q7Rcvs/8isuzb7wIDAQAB"

    gkey = '"'+a+b+"\"\""+c+d+"\"\""+e+f+"\"\""+g+h+'"'

    dnsrecord.append(["google._domainkey."+domain, "TXT", "300",
                      [gkey]])
    # 9
    dnsrecord.append(["k1._domainkey."+domain,
                     "CNAME", "300",
                      ["dkim.mcsv.net"]])
    # 12
    dnsrecord.append(["blog."+domain,
                     "CNAME", "300",
                      ["fluidsignal.wordpress.com."]])
    # 13
    dnsrecord.append(["kb."+domain,
                     "CNAME", "300",
                      ["fluid.knowledgeowl.com"]])
    # 14
    dnsrecord.append(["mail."+domain,
                     "A", "300",
                      [ips[0]]])
    # 15
    dnsrecord.append(["noreply."+domain,
                     "MX", "300",
                      ["10 feedback-smtp.us-east-1.amazonses.com"]])
    # 16
    dnsrecord.append(["noreply."+domain,
                     "TXT", "300",
                      ["\"v=spf1 include:amazonses.com ~all\""]])
    # 17
    dnsrecord.append(["www."+domain,
                     "CNAME", "300",
                      ["unbouncepages.com"]])

    return dnsrecord


def main():

    lines = open("servers/host/vars/sesvars/domains.txt", "r")
    domains = lines.readlines()

    for i in domains:
        domain = i.split("\n")[0]+"."
        dnsrecord = dns_records(IP_ADDRESS_FILE, domain)
        # Crea Stack de Route 53
        r53 = CFr53Creator()
        r53.create_r53(domain, dnsrecord)
        stackname = "FLUIDR53" + re.sub('[.]', '', domain)
        cf_creator.deploy_cloudformation(r53.template.to_json(), stackname,
                                         "FLUID R53", 1)


main()
