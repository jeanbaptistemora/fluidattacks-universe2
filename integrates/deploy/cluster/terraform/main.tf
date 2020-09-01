terraform {
  required_version = "~> 0.13.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 2.70.0"
    }
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "~> 1.11"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 2.1"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 1.2"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 2.1"
    }
    template = {
      source  = "hashicorp/template"
      version = "~> 2.1"
    }
  }

  backend "s3" {
    bucket  = "fluidattacks-terraform-states-prod"
    key     = "integrates-cluster.tfstate"
    region  = "us-east-1"
    encrypt = true
    dynamodb_table = "terraform_state_lock"
  }

}

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.region
}
provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
  token                  = data.aws_eks_cluster_auth.cluster.token
  load_config_file       = false
}
provider "random" {}
provider "local" {}
provider "null" {}
provider "template" {}
