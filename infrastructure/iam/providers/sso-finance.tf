resource "aws_iam_saml_provider" "sso-finance" {
  name                   = "OneLoginFinance"
  saml_metadata_document = "${file("vars/SSOFinance.xml")}"
}
