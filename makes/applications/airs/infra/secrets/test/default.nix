{ airsPkgsTerraform
, terraformTest
, ...
}:
terraformTest airsPkgsTerraform {
  name = "airs-infra-secrets-test";
  product = "airs";
  target = "airs/deploy/secret-management/terraform";
}
