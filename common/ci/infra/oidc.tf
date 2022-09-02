resource "aws_iam_openid_connect_provider" "main" {
  url            = "https://gitlab.com"
  client_id_list = ["https://gitlab.com"]

  # Gitlab Thumbprint. You can get it with
  # echo | openssl s_client -connect gitlab.com:443 2>&- | openssl x509 -fingerprint -noout | sed 's/://g' | awk -F= '{print tolower($2)}'
  thumbprint_list = ["962828776ba4dc09a2a0a2b72ff9cd0bd8c33aee"]
}