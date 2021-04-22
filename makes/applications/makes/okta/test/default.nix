{ terraformTest
, ...
}:
terraformTest {
  name = "makes-okta-test";
  product = "makes";
  target = "makes/applications/makes/okta/src/terraform";
  secretsPath = "makes/applications/makes/okta/src/terraform/data.yaml";
}
