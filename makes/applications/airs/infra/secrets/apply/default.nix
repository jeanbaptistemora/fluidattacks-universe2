{ airsPkgsTerraform
, terraformApply
, ...
}:
terraformApply airsPkgsTerraform {
  name = "airs-infra-secrets-apply";
  product = "airs";
  target = "airs/deploy/secret-management/terraform";
}
