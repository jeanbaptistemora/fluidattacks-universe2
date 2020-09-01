variable "region" {
  default = "us-east-1"
}

provider "aws" {
  region = var.region
}


module "s3" {
  source = "./s3"
}

module "users" {
  source = "./users"
}

module "instances" {
  source = "./instances"
  security_group_secure_app = module.shared.security_group_secure_app
  security_group_intranet = module.shared.security_group_intranet
}

module "shared" {
  source = "./shared"
}

module "lambda" {
  source = "./lambda"
  lambda_execution_policy = module.users.lambda_execution_policy
}
