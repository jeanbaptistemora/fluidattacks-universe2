data "aws_iam_policy_document" "okta-assume-role-policy-data" {
  statement {
    sid    = "OktaSAMLAccess"
    effect = "Allow"
    actions = [
      "sts:AssumeRoleWithSAML"
    ]
    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:saml-provider/okta-saml-provider"]
    }
    condition {
      test     = "StringEquals"
      variable = "SAML:aud"

      values = [
        "https://signin.aws.amazon.com/saml"
      ]
    }
  }
}

data "aws_iam_policy_document" "okta-saml-policy-data" {
  statement {
    sid    = "AllowListAliasesAndRoles"
    effect = "Allow"
    actions = [
      "iam:ListAccountAliases",
      "iam:ListRoles",
    ]
    resources = [
      "*",
    ]
  }
}

resource "aws_iam_user" "okta-access-user" {
  name = "okta-access-user"
  path = "/"

  tags = {
    "Name"               = "okta-access-user"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_access_key" "okta-access-user-key" {
  user = aws_iam_user.okta-access-user.name
}

resource "aws_iam_policy" "okta-saml-policy" {
  name        = "okta-access"
  path        = "/"
  description = "Policy for allowing okta to list account aliases and roles"
  policy      = data.aws_iam_policy_document.okta-saml-policy-data.json
}

resource "aws_iam_user_policy_attachment" "okta-access-user-attach-policy" {
  user       = aws_iam_user.okta-access-user.name
  policy_arn = aws_iam_policy.okta-saml-policy.arn
}

resource "aws_iam_saml_provider" "okta-saml-provider" {
  name                   = "okta-saml-provider"
  saml_metadata_document = <<-EOL
    <?xml version="1.0" encoding="UTF-8"?><md:EntityDescriptor entityID="http://www.okta.com/exk9ahz3reGbi064Y357" xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"><md:IDPSSODescriptor WantAuthnRequestsSigned="false" protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol"><md:KeyDescriptor use="signing"><ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:X509Data><ds:X509Certificate>MIIDqDCCApCgAwIBAgIGAW2yeIqDMA0GCSqGSIb3DQEBCwUAMIGUMQswCQYDVQQGEwJVUzETMBEG
    A1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2FuIEZyYW5jaXNjbzENMAsGA1UECgwET2t0YTEU
    MBIGA1UECwwLU1NPUHJvdmlkZXIxFTATBgNVBAMMDGZsdWlkYXR0YWNrczEcMBoGCSqGSIb3DQEJ
    ARYNaW5mb0Bva3RhLmNvbTAeFw0xOTEwMDkyMTQwNDdaFw0yOTEwMDkyMTQxNDdaMIGUMQswCQYD
    VQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2FuIEZyYW5jaXNjbzENMAsG
    A1UECgwET2t0YTEUMBIGA1UECwwLU1NPUHJvdmlkZXIxFTATBgNVBAMMDGZsdWlkYXR0YWNrczEc
    MBoGCSqGSIb3DQEJARYNaW5mb0Bva3RhLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoC
    ggEBAJZ2XfEX8jtFui4ll7MlUr8ByRQv2R3jaBcBliIh88JFO8PSscqeOCOAm083XO6CYW7FQnMf
    3ceDutnqIFbYemdILiUZXdD07yw+RwCN/WABs2gwpYLNR5ZEHnFrj0a6HMuzcN69l+UnLI6V9iDL
    Jcfz/+U9CoC0KCoW8+IKwrh2RIAMUIBLLBiQaF2kehFL6f+Pd8koa8mPzu3VQyaKDaXJf5GML7Vu
    Ew8MAxF2u8KgolH2MbbybkS4fqFJLDqzVT2RZXy9qUoII6qg0UqdX3do0yTRkLPhfNIIfABgkdre
    VyZXReUTYuLH+sWFq7G9REq45gA5wzNw4tynPyeerAECAwEAATANBgkqhkiG9w0BAQsFAAOCAQEA
    ULhbwMD6EOskawoayLezhPHeAtmzM8stYDaJdQWYzoirb2X+PM42zDVmCOiEQRYZxiUBnlmexPfZ
    Fd/p3ztmrhMCy/QqY901JaGvdUgtelPpVZ5uO9pXAhbY/rXK2jfZCWPu98oIxdWf4p8roTtIzdtw
    lVWI/jhY7rAHn95Vbjrh+OU7O7mTuyguVDXSXNkE3fSR7pp5YxFEw18Q2lJbduTtUDI/DxrXT+Yn
    J1ufkupsSdNt7VAVjA/sBE2qmnE9c4+uaWnR/nUYrRkLLRXRF7+Gdge5HqJ1H/XGPyt0RT9UaJsV
    5pBqdjpXGt+eZOKx4yze9tfx9rP+OUbzjZwBUw==</ds:X509Certificate></ds:X509Data></ds:KeyInfo></md:KeyDescriptor><md:NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress</md:NameIDFormat><md:NameIDFormat>urn:oasis:names:tc:SAML:2.0:nameid-format:unspecified</md:NameIDFormat><md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://fluidattacks.okta.com/app/amazon_aws/exk9ahz3reGbi064Y357/sso/saml"/><md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://fluidattacks.okta.com/app/amazon_aws/exk9ahz3reGbi064Y357/sso/saml"/></md:IDPSSODescriptor></md:EntityDescriptor>
  EOL

  tags = {
    "Name"               = "okta-saml-provider"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

output "okta-access-user-key" {
  sensitive = true
  value     = aws_iam_access_key.okta-access-user-key.secret
}
