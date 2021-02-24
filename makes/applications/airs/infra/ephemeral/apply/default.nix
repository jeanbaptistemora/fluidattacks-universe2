{ airsPkgsTerraform
, terraformApply
, ...
}:
terraformApply airsPkgsTerraform {
  name = "airs-infra-ephemeral-apply";
  product = "airs";
  target = "airs/deploy/ephemeral/terraform";
  secretsPath = "airs/deploy/secret-management/production.yaml";
}
