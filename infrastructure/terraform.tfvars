# Region Vars
region     = "us-east-1"
sNetRegion = "us-east-1b"

#EC2 Vars
clusterInstanceType = "m5a.large"

# S3 vars
fsBucket    = "servestf"
fwBucket    = "web.fluidattacks.com"
vaultBucket = "vault.fluidattacks"

# Network vars
cidr             = "192.168.100.0/24"
vpcSecondaryCidr = "192.168.104.0/21"
vpcId            = "vpc-53ea4637"

# EKS Vars
rtbId           = "rtb-a74ad5c3"
clusterName     = "FluidServes"
eksAmiId        = "ami-0abcb9f9190e867ab"
nodeStorageSize = "200"
eksSnetReg = [
  "us-east-1d",
  "us-east-1e",
]
eksSnetRegSecondary = [
  "us-east-1a",
  "us-east-1b",
]
