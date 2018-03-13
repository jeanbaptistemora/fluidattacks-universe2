
output "sso" {
  value = "${aws_iam_saml_provider.sso.arn}"
}

output "ssofinance" {
  value = "${aws_iam_saml_provider.sso-finance.arn}"
}
