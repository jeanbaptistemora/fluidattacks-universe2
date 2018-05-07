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

# gitlabCI
variable "ciIP" {}

#EC2 vars
variable "amiID" {}
variable "iType" {}
variable "kName" {}

# Net Vars
variable "cdir" {}
variable "vpcId" {}
variable "sgroupId" {}
variable "snetId" {}

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
