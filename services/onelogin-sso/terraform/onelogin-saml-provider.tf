resource "aws_iam_saml_provider" "onelogin-saml-provider" {
  name                   = "onelogin-saml-provider"
  saml_metadata_document = file("onelogin-saml-provider-metadata.xml")
}
