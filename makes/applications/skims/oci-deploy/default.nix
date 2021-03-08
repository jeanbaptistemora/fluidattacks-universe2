{ ociDeploy
, packages
, ...
}:
ociDeploy {
  oci = packages.skims.oci-build;
  name = "skims-oci-deploy";
  registry = "registry.gitlab.com";
  tag = "fluidattacks/product/skims";
}
