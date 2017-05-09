import paramiko

ip = open('/tmp/instance_ip.txt', "r").readlines()[0]
keyfile = '/tmp/FLUIDServes_Dynamic.pem'

print ip
k = paramiko.RSAKey.from_private_key_file(keyfile)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print "connecting"
c.connect(hostname=ip, username="core", pkey=k)
print "connected"

commands = ["sudo sh install_python.sh"]
for command in commands:
    print "Executing {}".format(command)
    stdin, stdout, stderr = c.exec_command(command)
    print stdout.read()
    print("Errors")
    print stderr.read()
c.close()
