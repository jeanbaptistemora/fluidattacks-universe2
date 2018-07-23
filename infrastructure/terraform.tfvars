# Region Vars
reg = "us-east-1"
sreg = "us-east-1b"
dbreg = "us-east-1"

#EC2 Vars
iType = "t2.xlarge"

# S3 Vars
vaultBucket = "vault.fluidattacks"

# Network vars
cidr = "192.168.100.0/24"
vpcId = "vpc-53ea4637"

# DB Vars
db_vpcId = "vpc-98fd1fe1"
storage_type = "gp2"
engine = "mysql"
instance_class = "db.t2.small"

# EKS Vars
rtbId = "rtb-a74ad5c3"
clusterName = "FluidServes"
eksAmiId    = "ami-dea4d5a1"
eksSnetReg  = ["us-east-1d", "us-east-1e"]
