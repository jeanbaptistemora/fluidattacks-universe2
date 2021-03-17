resource "aws_iam_saml_provider" "okta-saml-provider" {
  name                   = "okta-saml-provider"
  saml_metadata_document = file("saml-metadata.xml")
}
