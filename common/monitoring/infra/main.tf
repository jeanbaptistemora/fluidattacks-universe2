terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.50.0"
    }
    grafana = {
      source  = "grafana/grafana"
      version = "~> 1.33.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.8.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.3.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.16.1"
    }
    okta = {
      source  = "okta/okta"
      version = "~> 3.22.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "monitoring.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }
}

provider "aws" {
  region = "us-east-1"
}

provider "grafana" {
  url  = "https://${aws_grafana_workspace.monitoring.endpoint}"
  auth = aws_grafana_workspace_api_key.monitoring.key
}

provider "helm" {
  kubernetes {
    host                   = data.aws_eks_cluster.k8s_cluster.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.k8s_cluster.certificate_authority[0].data)

    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      command     = "aws"
      args        = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.k8s_cluster.name]
    }
  }
}
provider "kubernetes" {
  host                   = data.aws_eks_cluster.k8s_cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.k8s_cluster.certificate_authority[0].data)

  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.k8s_cluster.name]
  }
}

provider "okta" {
  org_name  = "fluidattacks"
  base_url  = "okta.com"
  api_token = var.oktaApiToken
}
