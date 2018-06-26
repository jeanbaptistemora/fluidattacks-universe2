variable "AWS_ACCESS_KEY_ID" {}
variable "AWS_SECRET_ACCESS_KEY" {}
variable "region" {}
variable "vpc_cidr" {}
variable "cluster_name" {}
variable "snet_regions" {
  type = "list"
}
variable "ami_id" {}
variable "instance_type" {}
