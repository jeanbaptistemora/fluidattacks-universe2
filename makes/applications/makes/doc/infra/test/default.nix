{ terraformTest
, ...
}:
terraformTest {
  name = "makes-doc-infra-test";
  product = "makes";
  target = "makes/applications/makes/doc/infra/terraform";
  secretsPath = "makes/applications/makes/secrets/src/development.yaml";
}
