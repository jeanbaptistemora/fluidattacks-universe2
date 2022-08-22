resource "aws_iam_openid_connect_provider" "main" {
  url             = "https://gitlab.com"
  client_id_list  = ["https://gitlab.com"]
  thumbprint_list = []
}
