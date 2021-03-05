{ packages
, path
, nixpkgs
, ...
}:
let
  ociDeploy = import (path "/makes/utils/oci-deploy") path nixpkgs;
in
ociDeploy {
  oci = packages.skims.oci-build;
  name = "skims-oci-deploy";
  registry = "registry.gitlab.com";
  tag = "fluidattacks/product/skims";
}
