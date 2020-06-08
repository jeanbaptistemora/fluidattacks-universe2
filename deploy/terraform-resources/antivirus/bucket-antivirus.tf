variable "resources_bucket" {}

module "antivirus" {
  source = "gchamon/bucket-antivirus/aws"
  version = "1.1.2"

  buckets-to-scan = [var.resources_bucket]

  scanner-environment-variables = {
    AV_DELETE_INFECTED_FILES = "False"
  }
  
  allow-public-access = true
}
