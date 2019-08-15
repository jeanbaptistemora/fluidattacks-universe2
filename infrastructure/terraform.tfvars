# Region Vars
region     = "us-east-1"
sNetRegion = "us-east-1b"
dbRegion   = "us-east-1"

#EC2 Vars
clusterInstanceType = "m5.xlarge"

# Network vars
cidr             = "192.168.100.0/24"
vpcSecondaryCidr = "192.168.104.0/21"
vpcId            = "vpc-53ea4637"

# DB Vars
dbVpcId       = "vpc-98fd1fe1"
storageType   = "gp2"
engine        = "mysql"
instanceClass = "db.t2.micro"

# EKS Vars
rtbId           = "rtb-a74ad5c3"
clusterName     = "FluidServes"
eksAmiId        = "ami-0abcb9f9190e867ab"
nodeStorageSize = "50"
eksSnetReg      = [
  "us-east-1d",
  "us-east-1e",
  "us-east-1a",
  "us-east-1b",
  "us-east-1d",
]

# ElastiCache Vars
cacheGroupId          = "tf-redis-cluster"
cacheGroupDescription = "Redis Cluster Cache"
cacheNodeType         = "cache.t2.medium"
cacheParamGroupName   = "default.redis5.0.cluster.on"

# Asserts vars
asserts-bucket = "asserts-logs"
