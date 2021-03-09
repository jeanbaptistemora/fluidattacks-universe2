{ ociDeploy
, packages
, ...
}:
ociDeploy {
  oci = packages.makes.oci.batch;
  name = "makes-deploy-oci-batch";
  registry = "registry.gitlab.com";
  tag = "fluidattacks/product/makes:batch";
}
