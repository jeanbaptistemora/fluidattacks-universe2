{ ociDeploy
, packages
, ...
}:
ociDeploy {
  oci = packages.asserts.oci.build;
  name = "asserts-oci-deploy";
  tag = "fluidattacks/asserts";
}
