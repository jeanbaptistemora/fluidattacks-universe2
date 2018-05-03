import boto
ec2 = boto.connect_ec2()
key = ec2.create_key_pair('FLUID_Serves')
key.save('infrastructure/vars/')
