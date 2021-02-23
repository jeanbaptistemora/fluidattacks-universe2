{ assertsPkgs
, ociDeploy
, packages
, ...
}:
ociDeploy assertsPkgs {
  oci = packages.asserts.oci.build;
  name = "asserts-oci-deploy";
  tag = "fluidattacks/asserts";
}
