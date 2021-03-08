{ ociDeploy
, packages
, ...
}:
ociDeploy {
  oci = packages.forces.oci-build;
  name = "forces-oci-deploy";
  tag = "fluidattacks/forces:new";
}
