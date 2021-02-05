{ forcesPkgs
, packages
, path
, ...
} @ _:
let
  ociDeploy = import (path "/makes/utils/oci-deploy") path forcesPkgs;
in
ociDeploy {
  oci = packages."forces/oci-build-wrapper";
  name = "forces-oci-deploy-wrapper";
  tag = "fluidattacks/break-build";
}
