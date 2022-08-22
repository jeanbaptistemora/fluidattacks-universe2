resource "aws_iam_openid_connect_provider" "main" {
  url            = "https://gitlab.com"
  client_id_list = ["https://gitlab.com"]

  # Gitlab Thumbprint. You can get it with
  # echo | openssl s_client -connect gitlab.com:443 2>&- | openssl x509 -fingerprint -noout | sed 's/://g' | awk -F= '{print tolower($2)}'
  thumbprint_list = ["578ebaf3348af92ca4ffd9b6e2b1f05f45216a15"]
}