{ forcesPkgs
, outputs
, path
, ...
} @ _:
let
  ociDeploy = import (path "/makes/utils/oci-deploy") path forcesPkgs;
in
ociDeploy {
  oci = outputs.packages."forces/oci-build";
  name = "forces-oci-deploy";
  tag = "fluidattacks/forces:new";
}
