# Region Vars
reg = "us-east-1"
sreg = "us-east-1b"
dbreg = "us-east-1"

#EC2 Vars
amiID = "ami-49e5cb5e"
iType = "t2.xlarge"
kName = "FLUID_Serves"

# Network vars
cdir = "192.168.100.0/24"
vpcId = "vpc-53ea4637"
sgroupId = "sg-992bc3e4"
snetId = "subnet-6a606433"

# DB Vars
db_vpcId = "vpc-98fd1fe1"
storage_type = "gp2"
engine = "mysql"
instance_class = "db.t2.small"

# EKS Vars
rtbId = "rtb-a74ad5c3"
clusterName = "FluidServes"
eksSnetReg = ["us-east-1b", "us-east-1c"]