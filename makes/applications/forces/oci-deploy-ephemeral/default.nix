{ ociDeploy
, packages
, ...
}:
ociDeploy {
  oci = packages.forces.oci-build;
  name = "forces-oci-deploy-ephemeral";
  tag = "fluidattacks/forces:$CI_COMMIT_REF_NAME";
}
