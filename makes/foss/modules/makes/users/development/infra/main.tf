terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.53.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "2.25.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "user-provision-development.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }

}

module "aws" {
  source  = "../../modules/aws"
  name    = "development"
  type    = "production"
  product = "makes"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "s3Read"
        Effect = "Allow"
        Action = [
          "s3:List*",
          "s3:Get*",
        ]
        Resource = ["*"]
      },
    ]
  })
}

module "cloudflare" {
  source = "../../modules/cloudflare"
  name   = "development"

  policy = {
    accountZone = {
      effect = "allow"
      permission_groups = [
        data.cloudflare_api_token_permission_groups.all.permissions["DNS Read"],
        data.cloudflare_api_token_permission_groups.all.permissions["Workers Routes Read"],
        data.cloudflare_api_token_permission_groups.all.permissions["Page Rules Read"],
      ]
      resources = {
        "com.cloudflare.api.account.zone.*" = "*"
      }
    }
  }
}
