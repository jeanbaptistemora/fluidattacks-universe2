{ forcesPkgs
, packages
, path
, ...
} @ _:
let
  ociDeploy = import (path "/makes/utils/oci-deploy") path forcesPkgs;
in
ociDeploy {
  oci = packages.forces.oci-build;
  name = "forces-oci-deploy-ephemeral";
  tag = "fluidattacks/forces:$CI_COMMIT_REF_NAME";
}
