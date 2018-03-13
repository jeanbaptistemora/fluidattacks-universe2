resource "aws_iam_saml_provider" "sso" {
  name                   = "OneLogin"
  saml_metadata_document = "${file("vars/SSO.xml")}"
}
