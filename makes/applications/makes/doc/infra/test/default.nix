{ terraformTest
, ...
}:
terraformTest {
  name = "makes-doc-infra-test";
  product = "serves";
  target = "makes/applications/makes/doc/infra/terraform";
  secretsPath = "makes/applications/makes/secrets/src/development.yaml";
}
