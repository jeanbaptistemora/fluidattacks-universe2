{ ociDeploy
, packages
, ...
}:
ociDeploy {
  oci = packages.makes.oci;
  name = "makes-deploy-oci";
  registry = "registry.gitlab.com";
  tag = "fluidattacks/product/makes";
}
