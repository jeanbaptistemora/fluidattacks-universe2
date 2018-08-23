# Region Vars
region = "us-east-1"
sNetRegion = "us-east-1b"
dbRegion = "us-east-1"

#EC2 Vars
clusterInstanceType = "t2.large"

# Network vars
cidr = "192.168.100.0/24"
vpcId = "vpc-53ea4637"

# DB Vars
dbVpcId = "vpc-98fd1fe1"
storageType = "gp2"
engine = "mysql"
instanceClass = "db.t2.small"

# EKS Vars
rtbId = "rtb-a74ad5c3"
clusterName = "FluidServes"
eksAmiId    = "ami-0b2ae3c6bda8b5c06"
eksSnetReg  = ["us-east-1d", "us-east-1e"]
