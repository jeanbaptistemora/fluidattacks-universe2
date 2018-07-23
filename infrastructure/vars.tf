# AWS vars
variable "acc_key" {}
variable "sec_key" {}
variable "reg" {}
variable "sreg" {}
variable "dbreg" {}

# S3 vars
variable "bucket" {}
variable "webBucket" {}
variable "fiBucket" {}
variable "vaultBucket" {}

# gitlabCI
variable "ciIP" {}

#EC2 vars
variable "iType" {}

# Net Vars
variable "cidr" {}
variable "vpcId" {}

# DB Vars
variable "db_vpcId" {}
variable "storage_type" {}
variable "engine" {}
variable "engine_ver" {}
variable "instance_class" {}
variable "db_name" {}
variable "db_user" {}
variable "db_pass" {}
variable "db_id" {}

# EKS Vars
variable "clusterName" {}
variable "eksAmiId" {}
variable "eksSnetReg" {
  type = "list"
}
variable "rtbId" {}
