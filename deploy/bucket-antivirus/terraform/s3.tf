module "antivirus" {
  source = "gchamon/bucket-antivirus/aws"
  version = "1.1.1"

  buckets-to-scan = [aws_s3_bucket.fi_resources_bucket]

  scanner-environment-variables = {
    AV_DELETE_INFECTED_FILES = "False"
  }
  
  allow-public-access = true
}
