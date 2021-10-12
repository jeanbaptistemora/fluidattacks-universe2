terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.49.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 2.20.0"
    }
    cloudinit = {
      source  = "hashicorp/cloudinit"
      version = "~> 2.2.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 1.11.1"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.2.0"
    }
    http = {
      source  = "hashicorp/http"
      version = "~> 2.1.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "makes-k8s.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }

}

provider "aws" {}

provider "cloudflare" {
  email   = var.cloudflareEmail
  api_key = var.cloudflareApiKey
}

provider "kubernetes" {
  config_path            = split(":", var.kubeConfig)[0]
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
  token                  = data.aws_eks_cluster_auth.cluster.token
  load_config_file       = false
}

provider "helm" {
  kubernetes {
    config_path = split(":", var.kubeConfig)[0]
  }
}
