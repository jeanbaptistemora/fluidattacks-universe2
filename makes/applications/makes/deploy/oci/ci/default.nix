{ ociDeploy
, packages
, ...
}:
ociDeploy {
  oci = packages.makes.oci.ci;
  name = "makes-deploy-oci-ci";
  registry = "registry.gitlab.com";
  tag = "fluidattacks/product/makes:ci2";
}
