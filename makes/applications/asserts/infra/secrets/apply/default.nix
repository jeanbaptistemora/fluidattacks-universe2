{ assertsPkgsTerraform
, terraformApply
, ...
}:
terraformApply assertsPkgsTerraform {
  name = "asserts-infra-secrets-apply";
  product = "asserts";
  target = "asserts/deploy/secret-management/terraform";
}
