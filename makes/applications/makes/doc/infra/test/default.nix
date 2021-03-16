{ terraformTest
, ...
}:
terraformTest {
  name = "makes-doc-infra-test";
  product = "serves";
  target = "makes/applications/makes/doc/infra/terraform";
  secretsPath = "makes/applications/serves/secrets/src/development.yaml";
}
