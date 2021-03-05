{ nixpkgs
, packages
, path
, ...
}:
let
  ociDeploy = import (path "/makes/utils/oci-deploy") path nixpkgs;
in
ociDeploy {
  oci = packages.forces.oci-build;
  name = "forces-oci-deploy";
  tag = "fluidattacks/forces:new";
}
